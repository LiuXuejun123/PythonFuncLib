import cantools
import can
from tkinter import *
from tkinter import filedialog
import os
def SearchFilePath_blf():
    """
    选择blf文件
    :return:
    """
    root = Tk()
    root.withdraw()
    FilePath = filedialog.askopenfilename(title='Select The blf file', filetypes=[('blf files', '*.blf')],
    initialdir=os.getcwd())
    file_path, file_name = os.path.split(FilePath)
    os.chdir(file_path)
    return FilePath
def ReadBlfFile(FilePath):
    blf_data = can.BLFReader(FilePath)

    return blf_data
