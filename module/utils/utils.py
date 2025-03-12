import os
from tkinter import *
from tkinter import filedialog
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

### operation
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