# -*- coding: utf-8 -*-
# 上面那句是必须的，这样这个py文件中才能出现中文

import urllib2
import math
import string
import json
import xlrd
from xlwt import * # 必须得这样引入
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

import re 
import codecs

# 截取返回数据的js地址，并发起请求，获得返回的数据
def getDataString(html_str, key) :

	key_firstIndex = html_str.find(key, 0)	# key = 'smhb_'
	key_startIndex = html_str.find('src=\"', key_firstIndex - 100)	# 假设每个url的长度都没有超过100
	key_endIndex = html_str.find('\"', key_startIndex + 5)
	key_url = html_str[key_startIndex + 5 : key_endIndex]

	# print key_url

	# 获取“收益走势图”的数据
	key_req = urllib2.Request(url=key_url)
	return urllib2.urlopen(key_req).read()

	# 从'navList:['开始，就一直查找“[ ]”即可，里边的是空的，就直接加上空也不会影响结果。
	# smhb_data_key = ['navList:[', 'navStrListOneYear:[', 'navStrListTwoYears:[', 'navStrListThreeYears:[', 'navStrListFiveYears:[', 'navStrListJnylDay:[']

	# key_data_firstStartIndex = key_data.find('navList:[', 0)
	# key_data_firstEndIndex = key_data.find(']', key_data_firstStartIndex)
	# key_data_list_string = key_data[key_data_firstStartIndex + 9 : key_data_firstEndIndex]

	# return key_data_list_string


# 提取data的函数
def getData(s_data) : 
	# 从'navList:['开始，就一直查找“[ ]”即可，里边的是空的，就直接加上空也不会影响结果。
	s_data_firstStartIndex = s_data.find('navList:[', 0)
	s_data_firstEndIndex = s_data.find(']', s_data_firstStartIndex)
	s_data_list_string = s_data[s_data_firstStartIndex + 9 : s_data_firstEndIndex]

	tmp = s_data_firstEndIndex
	while True:
		s_data_bracketStart = s_data.find('[', tmp)
		if s_data_bracketStart == -1 :	# 已经没有'['时，跳出循环
			break;
		s_data_bracketEnd = s_data.find(']', s_data_bracketStart)
		s_data_inter = s_data[s_data_bracketStart + 1 : s_data_bracketEnd]
		if len(s_data_inter) > 0 :
			s_data_list_string = s_data_list_string + ',' + s_data_inter
		tmp = s_data_bracketEnd

	s_data_list = s_data_list_string.split('\',')
	length = len(s_data_list)
	for i in range(0, length) :
		s_data_list[i] = s_data_list[i][1 : len(s_data_list[i])]
	s_data_list[length - 1] = s_data_list[length - 1][0 : len(s_data_list[length - 1]) - 1]

	return s_data_list


# 爬取数据并保存到excel中
def getDataFromURL(url_file_name, url, index) :
	# url = "http://simu.howbuy.com/zexi/P00511/"
	req = urllib2.Request(url=url)
	html_str = urllib2.urlopen(req).read()

	smhb_data = getDataString(html_str, "smhb_")
	smydhc_data = getDataString(html_str, "smydhc_")

	smhb_data_list = getData(smhb_data)
	smydhc_data_list = getData(smydhc_data)

	# print len(smhb_data_list)
	if(len(smhb_data_list) <= 1 or len(smydhc_data_list) <= 1) :
		return

	print smhb_data_list[0]
	# print smhb_data_list[1]
	print smhb_data_list[len(smhb_data_list)-1]

	# print len(smydhc_data_list)
	print smydhc_data_list[0]
	# print smydhc_data_list[1]
	print smydhc_data_list[len(smydhc_data_list)-1]

	# 创建一个excel文件并创建一个sheet
	excel_file = Workbook(encoding='utf-8')
	excel_smhb_sheet = excel_file.add_sheet('收益走势图')
	excel_smydhc_sheet = excel_file.add_sheet('回撤走势图')
	excel_rest_sheet = excel_file.add_sheet('同类排名')
	
	# 设置标题：时间，累计净值(%)，本基金，沪深300	
	excel_smhb_sheet.write(0, 0, "时间")
	excel_smhb_sheet.write(0, 1, "累计净值(%)")
	excel_smhb_sheet.write(0, 2, "本基金")
	excel_smhb_sheet.write(0, 3, "沪深300")
	excel_smhb_sheet.write(0, 4, "好买对冲指数")
	excel_smhb_sheet.write(0, 5, "不确定1")
	excel_smhb_sheet.write(0, 6, "不确定2")

	# 设置标题：时间，单位净值(%)，月回撤(%)
	excel_smydhc_sheet.write(0, 0, "时间")
	excel_smydhc_sheet.write(0, 1, "单位净值(%)")
	excel_smydhc_sheet.write(0, 2, "月回撤(%)")

	# 设置标题：名称，近一年，近二年，近三年，近五年，成立以来
	excel_rest_sheet.write(0, 0, "今年以来")
	excel_rest_sheet.write(0, 1, "2014年")
	excel_rest_sheet.write(0, 2, "2013年")
	excel_rest_sheet.write(0, 3, "2012年")
	excel_rest_sheet.write(0, 4, "2011年")
	excel_rest_sheet.write(0, 5, "2010年")
	excel_rest_sheet.write(0, 6, "2009年")
	excel_rest_sheet.write(0, 7, "2008年")
	excel_rest_sheet.write(0, 8, "成立以来")

	# 写入数据
	row = 1
	column = 0
	# 收益走势图
	for data in smhb_data_list : 
		data_list = data.split(',')

		time =  data_list[0] + '-' + str((int(data_list[1])+1)).zfill(2) + '-' + data_list[2].zfill(2)	# 时间，自动补零
		excel_smhb_sheet.write(row, column, time)
		column += 1

		leiJiJingZhi = data_list[6]		# 累计净值
		excel_smhb_sheet.write(row, column, leiJiJingZhi)
		column += 1

		benJiJin = data_list[3]			# 本基金
		excel_smhb_sheet.write(row, column, benJiJin)
		column += 1

		hs300 = data_list[4]			# 沪深300
		excel_smhb_sheet.write(row, column, hs300)
		column += 1

		haoMai = data_list[5]		# 好买对冲指数
		excel_smhb_sheet.write(row, column, haoMai)
		column += 1

		uncertain1 = data_list[7]		# 不确定1
		excel_smhb_sheet.write(row, column, uncertain1)
		column += 1

		uncertain2 = data_list[8]		# 不确定2
		excel_smhb_sheet.write(row, column, uncertain2)

		column = 0
		row = row + 1


	row = 1
	column = 0
	# 回撤走势图
	for data in smydhc_data_list : 
		data_list = data.split(',')

		time = data_list[2] + '-' + data_list[3].zfill(2)
		excel_smydhc_sheet.write(row, column, time)
		column += 1

		danWeiJingZhi = data_list[0]
		excel_smydhc_sheet.write(row, column, danWeiJingZhi)
		column += 1

		yueHuiChe = data_list[1]
		excel_smydhc_sheet.write(row, column, yueHuiChe)
		column = 0
		row = row + 1


	row = 1
	column = 0
	# 年度业绩表--同类排名
	key_tlpm = "同类排名"	# 一共会出现两次，第二次才是需要的位置
	tlpm_firstIndex = html_str.find(key_tlpm, 0)
	tlpm_startIndex = html_str.find(key_tlpm, tlpm_firstIndex + 4)
	tlpm_endIndex = html_str.find('</tr>', tlpm_startIndex)

	# title_tlpm = "今年以来<"
	# title_tlpm_firstIndex = html_str.find(title_tlpm, 0)
	# title_tlpm_startIndex = html_str.find(title_tlpm, title_tlpm_firstIndex + 4)
	# title_tlpm_endIndex = html_str.find('</tr>', title_tlpm_startIndex)

	# 获取数据
	tlpm_searchIndex = tlpm_startIndex

	for i in range(0, 9) : 
		tmp_startIndex = html_str.find('"cBlack">', tlpm_searchIndex)
		tmp_endIndex = html_str.find('<', tmp_startIndex)
		pm = html_str[tmp_startIndex +  len('"cBlack">'): tmp_endIndex]
		# print pm
		tmp_startIndex = html_str.find('"cGray9">', tmp_endIndex)
		# 这里是为了判断是否到了最后一个
		if tmp_startIndex - tmp_endIndex < 100 : 
			tmp_endIndex = html_str.find('<', tmp_startIndex)
			pm += html_str[tmp_startIndex + len('"cGray9">') : tmp_endIndex]
		tlpm_searchIndex = tmp_endIndex
		# print pm
		excel_rest_sheet.write(row, column, pm)
		# print column
		column += 1

	# 保存excel文件
	# excel_file_name = url_file_name + str(index) + '.xls'
	# excel_file.save(excel_file_name)
	excel_file_name = "ExcelFiles\\" + str(index) + "_" + url_file_name + '.xls'
	excel_file.save(excel_file_name)


def main() :

	urls = xlrd.open_workbook('temp.xls')
	table = urls.sheets()[0]	# get sheet1 in the excel file

	index = 1

	rowSize = table.nrows
	for i in range(0, rowSize):

		# if index >= 7251 : 
		url = table.row(i)[0].value
		fileName = table.row(i)[1].value.decode('utf-8');
		print index, url, fileName

		getDataFromURL(fileName, url, index)

			# excel_file = Workbook(encoding='utf-8')
			# excel_smhb_sheet = excel_file.add_sheet('收益走势图')
			# excel_smydhc_sheet = excel_file.add_sheet('回撤走势图')
			# excel_rest_sheet = excel_file.add_sheet('同类排名')
			# excel_file_name = "ExcelFiles\\" + str(index) + "_" + fileName + '.xls'
			# excel_file.save(excel_file_name)

		index += 1
		# if index > 1000 :
		# 	break


# 执行主函数
if __name__=="__main__": 
	main()

