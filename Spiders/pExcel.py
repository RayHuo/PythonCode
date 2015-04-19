import xlrd

urls = xlrd.open_workbook('tbComment.xls')
table = urls.sheets()[0]	# get sheet1 in the excel file

output = open('excel.txt', 'w')
rowSize = table.nrows
for i in range(0, rowSize):
	fileName = table.row(i)[0].value
	url = table.row(i)[1].value
	output.write("File : "+fileName+" , URL : "+url+"\n")
output.close()
# urls.close()