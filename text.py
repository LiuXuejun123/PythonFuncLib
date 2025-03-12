import os
import json
import numpy as np
from scipy.io import savemat

# 加载接口定义
with open('interface_config.json', 'r') as f:
    config = json.load(f)

# 时间序列参数
duration = config['time_config']['duration']
sample_interval = config['time_config']['sample_interval']
time_points = np.arange(0, duration + sample_interval, sample_interval)
num_samples = len(time_points)


# 类型处理函数
def get_type_info(type_name, types_config):
    type_def = types_config[type_name]
    if type_name.startswith("Enum:"):
        return {"is_enum": True, "values": type_def["values"]}
    elif type_name == "single":
        return {"is_enum": False, "numpy_type": type_def["numpy_type"]}
    else:
        raise ValueError(f"Unsupported type: {type_name}")


# 生成单个成员的测试序列
def generate_member_sequence(member, num_samples, test_case_type):
    type_info = get_type_info(member["type"], config["types"])
    if type_info["is_enum"]:
        enum_values = list(type_info["values"].values())
        if test_case_type == "default":
            return np.full(num_samples, member["default"], dtype=np.int32)
        elif test_case_type == "max":
            return np.full(num_samples, max(enum_values), dtype=np.int32)
        elif test_case_type == "step":
            return np.where(time_points < duration / 2, min(enum_values), max(enum_values)).astype(np.int32)
    else:  # single
        range_min, range_max = member.get("range", [0.0, 1.0])
        if test_case_type == "default":
            return np.full(num_samples, member["default"], dtype=np.float32)
        elif test_case_type == "max":
            return np.full(num_samples, range_max, dtype=np.float32)
        elif test_case_type == "step":
            return np.linspace(range_min, range_max, num_samples, dtype=np.float32)
    return None


# 生成测试用例
def generate_test_cases(interface):
    test_cases = []
    test_types = ["default", "max", "step"]  # 可扩展更多类型

    for test_type in test_types:
        test_case = {}
        for member in interface["members"]:
            test_case[member["name"]] = generate_member_sequence(member, num_samples, test_type)
        test_cases.append(test_case)

    return test_cases


# 主逻辑：为每个接口生成测试用例
base_dir = 'TestCases'
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

for interface in config["interfaces"]:
    interface_name = interface["name"]
    test_cases = generate_test_cases(interface)

    # 为每个测试用例创建文件夹并保存
    for i, test_case in enumerate(test_cases, 1):
        folder_name = os.path.join(base_dir, f'{interface_name}_TestCase_{i}')
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Bus 类型数据结构
        bus_data = {
            interface_name: {
                'time': time_points,
                'signals': {
                    'values': test_case
                }
            }
        }

        # 保存为 .mat 文件
        file_name = os.path.join(folder_name, f'{interface_name}.mat')
        savemat(file_name, bus_data)
        print(f'Generated {interface_name} Test Case {i} in folder: {folder_name}')

# 可选：验证
from scipy.io import loadmat

sample_file = os.path.join(base_dir, 'AccrPedlPsd0_TestCase_1', 'AccrPedlPsd0.mat')
loaded_data = loadmat(sample_file)
print("Sample time shape:", loaded_data['AccrPedlPsd0']['time'][0, 0].shape)