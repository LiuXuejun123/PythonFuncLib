from asammdf import MDF
from tkinter import *
from tkinter import filedialog
import os
from scipy.io import savemat
def SearchFilePath_xcp():
    """
    选择DBC文件
    :return:
    """
    root = Tk()
    root.withdraw()
    FilePath = filedialog.askopenfilename(title='Select The Excel file',
                                            filetypes=[('MF4 files', '*.mf4'), ('Excel files', '*.mat'),
                                                       ('MDF files', '*.MDF')],
                                            initialdir=os.getcwd())
    file_path, file_name = os.path.split(FilePath)
    os.chdir(file_path)
    return FilePath
def ReadMF4(FilePath):
    mdf_data = MDF(FilePath)
    return mdf_data
def DataBase2Dict(mdf_database,SignalNameList):
    Dict= {}
    for SignalName in SignalNameList:
        value = mdf_database.get(SignalNameList).samples
        time = mdf_database.get(SignalNameList).timestamps
        TempDict = {}
        TempDict["Times"] = time
        TempDict["Value"] = value
        Dict[SignalName] = TempDict
def SaveWithMat(Dict):
    savemat('SWC_IO.mat',Dict)
