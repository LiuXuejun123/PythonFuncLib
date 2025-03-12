class EnumType:
    EnumName = ""
    Pair ={}
    def __init__(self):
        self.EnumName = ""
        self.Pair = {}
    def GetValue(self,value):
        return self.EnumName + "." + self.Pair[value]
    def display(self):
        print(self.EnumName)
        print(self.Pair)
def isinstr( Str1, SearchStr):
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

def isStrNumber(str1):
    """
    判断字符串是否是一个数字
    :param str1:
    :return:
    """
    try:
        a = int(str1)
        return True
    except ValueError:
        return False
def GetEnumMap(list):
    Pair = {}
    startflag = 0
    list = list.split('\r')
    for i in range(0,len(list)):
        message = list[i]
        if message == 'Description':
            startflag = 1
            continue
        if startflag:
            if isStrNumber(message):
                Pair[message] = list[i+1]
    return Pair

def GetSysEnumDefine(sheet,num_rows,EnumDefineCol,DescriptionCol):
    DataTypeMap = {}
    for i in range(2,num_rows+1):
        Datatype = str(sheet.cell(i, EnumDefineCol).value)
        if isinstr(Datatype,"Enum:"):
            Description = str(sheet.cell(i, DescriptionCol).value)
            Datatype = Datatype.split(":")[1]
            Datatype = Datatype.replace(" ","")

            DescriptionList = Description.replace("_x000D_",",")
            DescriptionList = DescriptionList.split(",")
            DescriptionList = [item.replace("\n","") for item in DescriptionList]
            if Datatype in DataTypeMap:
                continue
            else:
                TempData = EnumType()
                TempData.EnumName = Datatype
                TempData.Pair = GetEnumMap(DescriptionList)
                DataTypeMap[Datatype] = TempData
def GetInterfaceJson(sheet):
    print(1)
