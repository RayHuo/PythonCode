# -*- coding:utf-8 -*-

import xlrd

inputs = xlrd.open_workbook('input.xls')
# outputs = xlrd.open_workbook('output.xlsx')

table = inputs.sheets()[0]	# get sheet1 in the excel file

output = open('output.txt', 'w')
rowSize = table.nrows
# 每一行地读
for i in range(0, rowSize):
    count = 1
    # print table.row[i][0].value
    while count <= len(table.row(i)) :
        output.write("%d\t" % table.row(i)[count-1].value)
        if count % 5 == 0 :
            output.write("\n")
        count += 1

	# fileName = table.row(i)[0].value
	# url = table.row(i)[1].value
	# output.write("File : "+fileName+" , URL : "+url+"\n")
output.close()
# urls.close()