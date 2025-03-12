import module.utils.utils as utils
import module.xlsx.xlsx as xlsx
import module.Interface.Interface as Interface

filename  = utils.XlsxFileSelect()
workbook,sheet = xlsx.read_Xlsx(filename)
EnumDataType = Interface.GetSysEnumDefine(sheet,sheet.max_row,17,14)
print(1)