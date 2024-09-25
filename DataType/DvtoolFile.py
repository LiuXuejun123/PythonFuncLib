class DvtoolFile:
    FusionFileName = ""
    FusionFilePath = ""
    def __init__(self,FilePath,FileName):
        self.FusionFilePath = FilePath
        self.FusionFileName = FileName
    def GetFileNamepix(self):
        index = self.FusionFileName.find('_dbg_')
        return self.FusionFileName[0:index+5]
    def GetFileNamePixFixForExport(self):
        index = self.FusionFileName.find('_dbg_')
        return self.FusionFileName[0:index+4]
    def GetDvtoolFileName(self,DataName):
        str1  = self.GetFileNamepix()
        if DataName == 'Road':
            str1 = str1 + 'Time_FusionOutput_' + DataName + ".csv"
        else:
            str1  = str1 +'FusionOutput_'+ DataName+".csv"
        return str1
    def GetDvtoolFileNamePath(self,DataName):
        str1 = self.GetDvtoolFileName(DataName)
        str2 = self.FusionFilePath + '/' +str1
        return str2
