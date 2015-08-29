import xlrd
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

urls = xlrd.open_workbook('temp.xls')
table = urls.sheets()[0]	# get sheet1 in the excel file

index = 0

output = open('excel.txt', 'w')
rowSize = table.nrows
for i in range(0, rowSize):
	url = table.row(i)[0].value.decode('utf-8')
	fileName = table.row(i)[1].value.decode('utf-8')
#	output.write(fileName + "\t" + url + "\n")
	print (fileName + "\t" + url + "\n")
	if index >= 10 : 
		break;
	index += 1
output.close()
# urls.close()