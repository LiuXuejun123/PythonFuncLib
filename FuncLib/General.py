import os
from tkinter import *
from tkinter import filedialog
import pandas as pd
import DataType.Enumeration as EM
import numpy as np
from scipy.io import savemat
from pathlib import Path
from datetime import datetime, timedelta
import re
def CsvFileSelect():
    """
    :return:
    """
    root = Tk()
    root.withdraw()
    FilePath = filedialog.askopenfilename(title='Select The CSV file',
                                          filetypes=[('CSV files', '*.csv')],
                                          initialdir=os.getcwd())
    if FilePath == '':
        return ""
    else:
        return FilePath

def XlsxFileSelect():
    """
    :return:
    """
    root = Tk()
    root.withdraw()
    FilePath = filedialog.askopenfilename(title='Select The Xlsx file',
                                          filetypes=[('Xlsx files', '*.xlsx')],
                                          initialdir=os.getcwd())
    if FilePath == '':
        return ""
    else:
        return FilePath

def FolderSelect():
    root = Tk()
    root.withdraw()  # 隐藏根窗口
    # 打开文件夹选择对话框
    folder_path = filedialog.askdirectory()
    if folder_path == '':
        return ""
    else:
        return folder_path
def CanRecbinFileSelect():
    root = Tk()
    root.withdraw()
    FilePath = filedialog.askopenfilename(title='Select The Recbin file',
                                          filetypes=[('recbin files', '*.recbin')],
                                          initialdir=os.getcwd())
    if FilePath == '':
        return ""
        pass
    else:
        return FilePath
def DBCFileSelect():
    root = Tk()
    root.withdraw()
    FilePath = filedialog.askopenfilename(title='Select The dbc file',
                                          filetypes=[('dbc files', '*.dbc')],
                                          initialdir=os.getcwd())
    if FilePath == '':
        return ""
        pass
    else:
        return FilePath
def isinstr(Str1, SearchStr):
    """
    判断Str1中是否存在SearchStr
    :param Str1:
    :param SearchStr:
    :return:
    """
    try:
        Str1.index(SearchStr)
        return True
    except ValueError:
        return False
def LoadCsvFile(Dvtool,Platfrom):
    if EM.Platfrom.FVC3 == Platfrom:
        LaneMarkerDataPath = Dvtool.GetDvtoolFileNamePath('LaneMark')
        ObjectDataPath = Dvtool.GetDvtoolFileNamePath('Object')
        RoadEdgePath = Dvtool.GetDvtoolFileNamePath('RoadEdge')
        VehSelfPath = Dvtool.GetDvtoolFileNamePath('VehicleData')
        PahHistDataPath = Dvtool.GetDvtoolFileNamePath('PahHist')
    elif EM.Platfrom.FVC2_8 == Platfrom:
        LaneMarkerDataPath = Dvtool.GetDvtoolFileNamePath('Lane')
        ObjectDataPath = Dvtool.GetDvtoolFileNamePath('Objects')
        VehSelfPath = Dvtool.GetDvtoolFileNamePath('VehSelf')
        PahHistDataPath = Dvtool.GetDvtoolFileNamePath('PahHist')
        RoadEdgePath = Dvtool.GetDvtoolFileNamePath('RoadEdge')

    df_Lane = pd.read_csv(LaneMarkerDataPath)
    df_Path = pd.read_csv(PahHistDataPath)
    df_Object = pd.read_csv(ObjectDataPath)
    df_Vehicle = pd.read_csv(VehSelfPath)

    if EM.Platfrom.FVC3 == Platfrom:
        coldata1 = df_Lane['ClsLe.Estimn.ConstCoeff'].tolist()
        coldata2 = df_Path['PahHistEle[0].PosnLgt[0]'].tolist()
        coldata3 = df_Object['Obj[0].Estimn.PosnLgt'].tolist()
        coldata4 = df_Vehicle['VLgt'].tolist()
    elif EM.Platfrom.FVC2_8 == Platfrom:
        coldata1 = df_Lane['ClsLe.Estimn.PolyCoeff.constCoeff'].tolist()
        coldata2 = df_Path['pahHistEle[0].PosnLgt[0]'].tolist()
        coldata3 = df_Object['obj[0].Estimn.PosnLgt'].tolist()
        coldata4 = df_Vehicle['VLgt'].tolist()
    FrameMaxSize = min(len(coldata1), len(coldata2), len(coldata3), len(coldata4))  # get the data size
    return df_Lane,df_Path,df_Object,df_Vehicle,FrameMaxSize

def MatchTime(RecordTime):
    match = re.search(r'(\d{8})_(\d{6})', RecordTime)
    if match:
        date = match.group(1)
        time = match.group(2)
    else:
        print("未找到匹配的日期和时间信息")
    return date,time
def time_string_to_timedelta(time_str):
    """将HHMMSS格式的字符串转换为timedelta对象"""
    hours = int(time_str[:2])
    minutes = int(time_str[2:4])
    seconds = int(time_str[4:6])
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

def MatchFileRecordTime(FileName):
    file_path, file_name = os.path.split(FileName)
    date,time = MatchTime(file_name)
    Timedata = time_string_to_timedelta(time)
    return Timedata

def DBGFile2df(Dvtool,Platfrom):
    if EM.Platfrom.FVC3 == Platfrom:
        DiagDataPath = Dvtool.GetDvtoolFileNamePath('Diag')
        LaneMarkerDataPath = Dvtool.GetDvtoolFileNamePath('LaneMark')
        ObjectDataPath = Dvtool.GetDvtoolFileNamePath('Object')
        RoadEdgePath = Dvtool.GetDvtoolFileNamePath('RoadEdge')
        VehSelfPath = Dvtool.GetDvtoolFileNamePath('VehicleData')
        PahHistDataPath = Dvtool.GetDvtoolFileNamePath('PahHist')
        FreeSapceDataPath = Dvtool.GetDvtoolFileNamePath('FreeSpace')
        ObstacleDataPath = Dvtool.GetDvtoolFileNamePath('Obstacle')
        RoadDataPath = Dvtool.GetDvtoolFileNamePath('RoadEdge')
        RoadPropertyDataPath = Dvtool.GetDvtoolFileNamePath('RoadProperty')
        RoadSignDataPath = Dvtool.GetDvtoolFileNamePath('RoadSign')
        try:
            df_Diag = pd.read_csv(DiagDataPath)
            df_Lane = pd.read_csv(LaneMarkerDataPath)
            df_Path = pd.read_csv(PahHistDataPath)
            df_Object = pd.read_csv(ObjectDataPath)
            df_Vehicle = pd.read_csv(VehSelfPath)
            df_RoadEdge = pd.read_csv(RoadEdgePath)
            df_FreeSpace = pd.read_csv(FreeSapceDataPath)
            df_Obstacle =pd.read_csv(ObstacleDataPath)
            df_Road = pd.read_csv(RoadDataPath)
            df_RoadProperty = pd.read_csv(RoadPropertyDataPath)
            df_RoadSign = pd.read_csv(RoadSignDataPath)

        except Exception as e:
            print(f"文件无法找到:{e}")
            pass

        data_array_Lane = df_Lane.values.astype(np.double)
        data_array_Path = df_Path.values.astype(np.double)
        data_array_Object = df_Object.values.astype(np.double)
        data_array_Vehicle = df_Vehicle.values.astype(np.double)
        data_array_RoadEdge = df_RoadEdge.values.astype(np.double)
        data_array_Diag = df_Diag.values.astype(np.double)
        data_array_FreeSpace = df_FreeSpace.values.astype(np.double)
        data_array_Obstacle = df_Obstacle.values.astype(np.double)
        data_array_Road = df_Road.values.astype(np.double)
        data_array_RoadProperty = df_RoadProperty.values.astype(np.double)
        data_array_RoadSign = df_RoadSign.values.astype(np.double)

        return data_array_Lane,data_array_Path,data_array_Object,data_array_Vehicle\
                ,data_array_RoadEdge,data_array_Diag,data_array_FreeSpace,data_array_Obstacle,data_array_Road,data_array_RoadProperty\
                ,data_array_RoadSign


    elif EM.Platfrom.FVC2_8 == Platfrom:
        LaneMarkerDataPath = Dvtool.GetDvtoolFileNamePath('Lane')
        ObjectDataPath = Dvtool.GetDvtoolFileNamePath('Objects')
        VehSelfPath = Dvtool.GetDvtoolFileNamePath('VehSelf')
        PahHistDataPath = Dvtool.GetDvtoolFileNamePath('PahHist')
        RoadEdgePath = Dvtool.GetDvtoolFileNamePath('RoadEdge')

        try:
            df_Lane = pd.read_csv(LaneMarkerDataPath)
            df_Path = pd.read_csv(PahHistDataPath)
            df_Object = pd.read_csv(ObjectDataPath)
            df_Vehicle = pd.read_csv(VehSelfPath)
            df_RoadEdge = pd.read_csv(RoadEdgePath)
            data_array_Diag = 0
            data_array_FreeSpace = 0
            data_array_Obstacle = 0
            data_array_Road = 0
            data_array_RoadProperty = 0
            data_array_RoadSign =0
        except Exception as e:
            print(f"文件无法找到:{e}")
            pass

        data_array_Lane = df_Lane.values.astype(np.double)
        data_array_Path = df_Path.values.astype(np.double)
        data_array_Object = df_Object.values.astype(np.double)
        data_array_Vehicle = df_Vehicle.values.astype(np.double)
        data_array_RoadEdge = df_RoadEdge.values.astype(np.double)

        return data_array_Lane,data_array_Path,data_array_Object,data_array_Vehicle,data_array_RoadEdge,data_array_Diag,data_array_FreeSpace,data_array_Obstacle,data_array_Road,data_array_RoadProperty,data_array_RoadSign

def CanRecbin2df(CanRecbin,Platfrom):
    """

    :param CanRecbin:
    :param Platfrom:
    :return:
    """
    # if EM.Platfrom.FVC3 == Platfrom:
    #
    # elif EM.Platfrom.FVC2_8 == Platfrom:


def SaveMatData(data_array_Lane, data_array_Path, data_array_Object, data_array_Vehicle,
                        data_array_RoadEdge,data_array_Diag,data_array_FreeSpace,
                        data_array_Obstacle,data_array_Road,data_array_RoadProperty,data_array_RoadSign,folder_path,SysRepalyMode):
    if EM.Platfrom.FVC3 == SysRepalyMode:
        folder_path = folder_path
        Path(folder_path).mkdir(parents=True,exist_ok=True)
        savemat(folder_path+'/Data_Lane.mat', {'data': data_array_Lane})
        savemat(folder_path+'/Data_Path.mat', {'data': data_array_Path})
        savemat(folder_path+'/Data_Object.mat', {'data': data_array_Object})
        savemat(folder_path+'/Data_Vehicle.mat', {'data': data_array_Vehicle})
        savemat(folder_path+'/Data_RoadEdge.mat', {'data': data_array_RoadEdge})

        savemat(folder_path+'/Data_Diag.mat', {'data': data_array_Diag})
        savemat(folder_path+'/Data_FreeSpace.mat', {'data': data_array_FreeSpace})
        savemat(folder_path+'/Data_Obstacle.mat', {'data': data_array_Obstacle})
        savemat(folder_path+'/Data_Road.mat', {'data': data_array_Road})
        savemat(folder_path+'/Data_RoadProperty.mat', {'data': data_array_RoadProperty})
        savemat(folder_path+'/Data_RoadSign.mat', {'data': data_array_RoadSign})

    elif EM.Platfrom.FVC2_8 == SysRepalyMode:
        savemat(folder_path+'/Data_Lane.mat', {'data': data_array_Lane})
        savemat(folder_path+'/Data_Path.mat', {'data': data_array_Path})
        savemat(folder_path+'/Data_Object.mat', {'data': data_array_Object})
        savemat(folder_path+'/Data_Vehicle.mat', {'data': data_array_Vehicle})
        savemat(folder_path+'/Data_RoadEdge.mat', {'data': data_array_RoadEdge})
def CheckRocordContinue(Record1,Record2,StrIntervalTime):
    ## 获取Record1记录时间
    Record1Time = MatchFileRecordTime(Record1)
    ## 获取Record2记录时间
    Record2Time = MatchFileRecordTime(Record2)
    ## 间隔时间确定
    intervaltime = time_string_to_timedelta(StrIntervalTime)
    ## 校验时间
    DeltaTime = Record2Time - Record1Time
    if DeltaTime == intervaltime:
        return True
    else:
        return False
