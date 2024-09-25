# This Python file uses the following encoding: utf-8
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import binascii
import os.path
import struct
import time
import datetime
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from collections import namedtuple
import FuncLib.ReadDBC as DBC
from scipy.io import savemat
from pathlib import Path
class Config:
    HeaderSize_Pos = 14
    big_endian = 1  # 0:Intel 1: Motorola
    saveflag = "y"
    recbinheader = b'BINARY'
    canFileSuffix = "_can_CHASIS.recbin"
    MsgSizeByte_bit=[0,4]
    SysTimeStamp_bit = [4,12]
    MsgIDbit_bit = [12,14]
    MsgType_bit = 16
    DLC_bit = 17
    MsgDataBody = [18,82]
    def __init__(self,Platform):
        if Platform == "FVC3":
            self.HeaderSize_Pos = 14
            self.big_endian = 1  # 0:Intel 1: Motorola
            self.saveflag = "y"
            self.recbinheader = b'BINARY'
            self.canFileSuffix = "_can_CHASIS.recbin"
            self.MsgSizeByte_bit = [0, 4]
            self.SysTimeStamp_bit = [4, 12]
            self.MsgIDbit_bit = [12, 14]
            self.MsgType_bit = 16
            self.DLC_bit = 17
            self.MsgDataBody = [18, 82]
        else:
            self.HeaderSize_Pos = 14
            self.big_endian = 1  # 0:Intel 1: Motorola
            self.saveflag = "y"
            self.recbinheader = b'BINARY'
            self.canFileSuffix = "_can_CHASIS.recbin"
            self.MsgSizeByte_bit = [0, 4]
            self.SysTimeStamp_bit = [4, 12]
            self.MsgIDbit_bit = [12, 14]
            self.MsgType_bit = 16
            self.DLC_bit = 17
            self.MsgDataBody = [18, 82]

def big_small_end_convert(data):
    """
    大小端转换
    :param data:
    :return:
    """
    data = bytes(data,encoding = "utf8")
    return binascii.hexlify(binascii.unhexlify(data)[::-1])

def hex_to_double(f):
    """
    HEX转数据
    :param f:
    :return:
    """
    return struct.unpack('!d', bytes.fromhex(f))[0]

def HexFileRead(currentPath):
    """

    :param currentPath:
    :return:
    """
    print(currentPath)
    try:
        f = open(currentPath, "rb")  # 打开要读取的十六进制文件
        byte_list = f.read()
    except (Exception, BaseException):
        byte_list = []
    return byte_list

def DLC_Calculate(dlcFlag):
    """

    :param dlcFlag:
    :return:
    """
    # DLC caculate
    if int(dlcFlag, 16) <= 8:
        dlc = int(dlcFlag, 16)
    elif dlcFlag == '0x9':
        dlc = 12
    elif dlcFlag == '0xa':
        dlc = 16
    elif dlcFlag == '0xb':
        dlc = 20
    elif dlcFlag == '0xc':
        dlc = 24
    elif dlcFlag == '0xd':
        dlc = 32
    elif dlcFlag == '0xe':
        dlc = 48
    elif dlcFlag == '0xf':
        dlc = 64
    else:
        dlc = -1
    return dlc
def SearchFilePath_recbin():
    """
    :return:
    """
    root = Tk()
    root.withdraw()
    FilePath = filedialog.askopenfilename(title='Select The recbin file', filetypes=[('recbin files', '*.recbin')],
    initialdir=os.getcwd())
    file_path, file_name = os.path.split(FilePath)
    os.chdir(file_path)
    return FilePath
def Int2Hexstr(intValue):
    bytelength = 2
    byteresult = intValue.to_bytes(bytelength, "big").hex()
    return byteresult

def DataProcess(byte_list,ToolConfig,currentPath,Veh2FuncInterfaceDict,DBC_DataBase):
    """

    :param byte_list:
    :param ToolConfig:
    :param currentPath:
    :return:
    """
    print(currentPath)
    HeaderSize = byte_list[ToolConfig.HeaderSize_Pos] #头部数据所在位置
    msgData_bytes = byte_list[HeaderSize:]
    startpsn = 0
    firstmsgflag = 0
    while True:
        if startpsn < len(msgData_bytes):  # Length Check
            msgSize_bytes = big_small_end_convert(
                "".join(msgData_bytes[startpsn + ToolConfig.MsgSizeByte_bit[0]: startpsn + ToolConfig.MsgSizeByte_bit[1]].hex()))
            msgSize = int(msgSize_bytes, 16)
            msgTiStamp_bytes = big_small_end_convert(
                "".join(msgData_bytes[startpsn + ToolConfig.SysTimeStamp_bit[0]: startpsn + ToolConfig.SysTimeStamp_bit[1]].hex()))
            msgTiStamp = hex_to_double(msgTiStamp_bytes.decode('utf-8')) / 1000.0
            msgID = big_small_end_convert(
                "".join(msgData_bytes[startpsn + ToolConfig.MsgIDbit_bit[0]:startpsn + ToolConfig.MsgIDbit_bit[1]].hex()))
            msgType = msgData_bytes[startpsn + ToolConfig.MsgType_bit]
            dlcFlag = hex(msgData_bytes[startpsn + ToolConfig.DLC_bit])
            msgBody = msgData_bytes[startpsn + 18: startpsn + 18+64]
            dlc = DLC_Calculate(dlcFlag)
            if dlc == -1:
                print(
                    "invalid dlcflag:",
                    dlcFlag, "Startpos:", startpsn,
                    "currentPath:")

            if firstmsgflag == 0:
                firstmsgflag = 1
                firstmsgtimestamp = msgTiStamp
            ##### 数据检索 ####################################################################################
            msgIDstr = msgID.decode('ascii') #byte 2 ascii
            for key,Veh2FuncInterface  in Veh2FuncInterfaceDict.items():
                byteresult = Int2Hexstr(Veh2FuncInterface.CanDataMessage.frame_id)
                if msgIDstr == byteresult:
                    MessageName = Veh2FuncInterface.CanDataMessage.message_name
                    SignalName = Veh2FuncInterface.CanDataMessage.signal_name
                    PyhValue = DBC.MessageDecode(DBC_DataBase,msgBody,MessageName,SignalName)
                    Veh2FuncInterfaceDict[key].Sampletime.append(msgTiStamp - firstmsgtimestamp)
                    Veh2FuncInterfaceDict[key].Value.append(PyhValue)
            startpsn = startpsn + msgSize + 4
        else:
            break
    return Veh2FuncInterfaceDict
def SaveWithMat(Dict):
    SaveDict = {}
    for key,value in Dict.items():

        SaveData = list(zip(value.Sampletime,value.Value))
        SaveDict[key] = SaveData
    savemat('SWC_Veh2Func.mat', SaveDict)
    print("保存结束")
def CanSignalListen(byte_list,ToolConfig,currentPath,DBC_DataBase,Frame_id,MessageName,SignalName):
    """

    :param byte_list:
    :param ToolConfig:
    :param currentPath:
    :return:
    """
    print(currentPath)
    HeaderSize = byte_list[ToolConfig.HeaderSize_Pos] #头部数据所在位置
    msgData_bytes = byte_list[HeaderSize:]
    startpsn = 0
    firstmsgflag = 0
    data = []
    Sampletinme = []
    while True:
        if startpsn < len(msgData_bytes):  # Length Check
            msgSize_bytes = big_small_end_convert(
                "".join(msgData_bytes[startpsn + ToolConfig.MsgSizeByte_bit[0]: startpsn + ToolConfig.MsgSizeByte_bit[1]].hex()))
            msgSize = int(msgSize_bytes, 16)
            msgTiStamp_bytes = big_small_end_convert(
                "".join(msgData_bytes[startpsn + ToolConfig.SysTimeStamp_bit[0]: startpsn + ToolConfig.SysTimeStamp_bit[1]].hex()))
            msgTiStamp = hex_to_double(
                msgTiStamp_bytes.decode('utf-8')) / 1000.0
            msgID = big_small_end_convert(
                "".join(msgData_bytes[startpsn + ToolConfig.MsgIDbit_bit[0]:startpsn + ToolConfig.MsgIDbit_bit[1]].hex()))
            msgType = msgData_bytes[startpsn + ToolConfig.MsgType_bit]
            dlcFlag = hex(msgData_bytes[startpsn + ToolConfig.DLC_bit])
            msgBody = msgData_bytes[startpsn + 18: startpsn + 18+64]
            dlc = DLC_Calculate(dlcFlag)
            if dlc == -1:
                print(
                    "invalid dlcflag:",
                    dlcFlag, "Startpos:", startpsn,
                    "currentPath:")

            if firstmsgflag == 0:
                firstmsgflag = 1
                firstmsgtimestamp = msgTiStamp
            ##### 数据检索 ####################################################################################
            # m = 177
            # bytelength = 2
            # byteresult = m.to_bytes(bytelength, "big").hex()
            # if msgID == b"00b1":
            msgIDstr = msgID.decode('ascii') #byte 2 ascii
            print("接收到报文：",msgIDstr)
            byteresult = Int2Hexstr(Frame_id)
            if msgIDstr == byteresult:
                PyhValue = DBC.MessageDecode(DBC_DataBase,msgBody,MessageName,SignalName)
                Time = msgTiStamp - firstmsgtimestamp
                ##########################
                ## 监控event
                ##########################
            startpsn = startpsn + msgSize + 4
        else:
            break
def Veh2funcInterfaceSaveMat(Veh2FuncInterfaceDictProcessed,folder_path):
    folder_path =  folder_path
    Path(folder_path).mkdir(parents=True,exist_ok=True)

    for key,Value in Veh2FuncInterfaceDictProcessed.items():
        Name = key
        Times = Value.Sampletime
        Value = Value.Value
        DataDict = {
            'time' :Times,
            'value' :Value
        }
        filename = str(Name) +'.mat'
        savemat(folder_path+"/"+filename,DataDict)

def DLCValueCalc_FVC2(DLC):
    if DLC == "00000008":
        return 8
    elif DLC == "00000009":
        return 12
    elif DLC == "0000000a":
        return 16
    elif DLC == "0000000b":
        return 20
    elif DLC == "0000000c":
        return 24
    elif DLC == "0000000d":
        return 32
    elif DLC == "0000000e":
        return 48
    elif DLC == "0000000f":
        return 64
    else:
        return -1
def Int2Hexstr_FVC2(intValue,bytelength):
    byteresult = intValue.to_bytes(bytelength, "big").hex()
    return byteresult

def DataProcess_FVC2(byte_list,currentPath,Veh2FuncInterfaceDict,DBC_DataBase):
    index = 0
    i = 0
    firstflag = 1
    while True:
        if i+29 < len(byte_list):
            Head = "".join(byte_list[i + 0: i + 4].hex())
            ID = "".join(byte_list[i + 4: i + 8].hex())
            ZeroBit = "".join(byte_list[i + 8: i + 12].hex())
            Timeindex =  "".join(byte_list[i + 12: i + 20].hex())

            DLC = "".join(byte_list[i + 20: i + 24].hex())
            FFbit = "".join(byte_list[i + 24: i + 28].hex())
            Channel = (byte_list[i+28])
            DLCValue = DLCValueCalc_FVC2(DLC)
            Data = byte_list[i+29:i+29+DLCValue]
            i = i+29+DLCValue
        else:
            break
        if Head == "00000001" and ZeroBit == "00000000" and FFbit == "ffffffff":

            msgTiStamp = hex_to_double(Timeindex)
            if firstflag == 1:
                firstmsgtimestamp = msgTiStamp
                firstflag = 0
            ## 提取全部Can报文
            for key, Veh2FuncInterface in Veh2FuncInterfaceDict.items():
                byteresult = Int2Hexstr_FVC2(Veh2FuncInterface.CanDataMessage.frame_id,4)
                if ID == byteresult:
                    MessageName = Veh2FuncInterface.CanDataMessage.message_name
                    SignalName = Veh2FuncInterface.CanDataMessage.signal_name
                    PyhValue = DBC.MessageDecode(DBC_DataBase, Data, MessageName, SignalName)
                    Veh2FuncInterfaceDict[key].Sampletime.append(msgTiStamp - firstmsgtimestamp)
                    Veh2FuncInterfaceDict[key].Value.append(PyhValue)
    return Veh2FuncInterfaceDict
