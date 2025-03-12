import openpyxl
def read_Xlsx(ExcelPath):
    """
    读取xlsx文件
    :param ExcelPath: xlsx文件地址
    :return: xlsx对象，sheet 对象
    """
    workbook = openpyxl.load_workbook(ExcelPath)
    # 选择工作表
    sheet = workbook.active
    return workbook, sheet