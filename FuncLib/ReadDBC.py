import cantools
from tkinter import *
from tkinter import filedialog
import os
class CanMessagedefine:
    message_name = ""
    frame_id = 0
    signal_name = ""
    bit_length = 0
    start_bit = 0
    scale_factor = 0.0
    offset = 0
    min_physical_value = 0
    max_physical_value = 0
    unit = ""
    flc = ""
    def __init__(self):
        self.message_name = ""
        self.frame_id = 0
        self.signal_name = ""
        self.bit_length = 0
        self.start_bit = 0
        self.scale_factor = 0.0
        self.offset = 0
        self.min_physical_value = 0
        self.max_physical_value = 0
        self.unit = ""
        self.flc = ""
    def display(self):
        print("messagename: ",self.message_name,"FrameId:",self.frame_id,"name: ",self.signal_name,"startbit: ",self.start_bit,"bitLength: ",self.bit_length)
def SearchFilePath_dbc():
    """
    选择DBC文件
    :return:
    """
    root = Tk()
    root.withdraw()
    FilePath = filedialog.askopenfilename(title='Select The dbc file', filetypes=[('dbc files', '*.dbc')],
    initialdir=os.getcwd())
    file_path, file_name = os.path.split(FilePath)
    os.chdir(file_path)
    return FilePath
def ReadDBC(filepath):
    db = cantools.database.load_file(filepath)
    return db
def DBCDataProcess(db):
    Messages = db.messages
    SignalDatadict = {}
    for i in range(0,len(Messages)):
        message_t = Messages[i]
        frame_id = message_t.frame_id
        message_name = message_t.name
        signals = message_t.signals

        for j in range(0,len(signals)):
            TempValue = CanMessagedefine()
            signal_t = signals[j]
            TempValue.message_name = message_name
            TempValue.frame_id = frame_id
            TempValue.signal_name = signal_t.name
            TempValue.bit_length = signal_t.length
            TempValue.start_bit =  signal_t.start
            TempValue.scale_factor = signal_t.scale
            TempValue.offset = signal_t.offset
            TempValue.min_physical_value = signal_t.minimum
            TempValue.max_physical_value = signal_t.maximum
            TempValue.unit = signal_t.unit
            TempValue.flc = ""
            SignalDatadict[signal_t.name] = TempValue
    return SignalDatadict
def MessageDecode(DBC_DataBase,Raw_Data,MessageName,SignalName):
    message = DBC_DataBase.get_message_by_name(MessageName)
    decodeSignal = message.decode(Raw_Data)
    try:
        PhyValue = decodeSignal[SignalName].value
    except AttributeError:
        PhyValue = decodeSignal[SignalName]
    return float(PhyValue)
