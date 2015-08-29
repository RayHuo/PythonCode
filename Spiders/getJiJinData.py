# -*- coding: utf-8 -*-
# 上面那句是必须的，这样这个py文件中才能出现中文

import urllib2
import math
import string
import json
import xlrd


url = "http://simu.howbuy.com/zexi/P00511/"

req = urllib2.Request(url=url)
html_str = urllib2.urlopen(req).read()

output = open('JiJinData.txt', 'w')

smhb_key = "smhb_"
smydhc_key = "smydhc_"

smhb_firstIndex = html_str.find("smhb_", 0)
smhb_startIndex = html_str.find('src=\"', smhb_firstIndex - 100)	# 假设每个url的长度都没有超过100
smhb_endIndex = html_str.find('\"', smhb_startIndex + 5)
smhb_url = html_str[smhb_startIndex + 5 : smhb_endIndex]

smydhc_firstIndex = html_str.find("smydhc_", smhb_firstIndex)
smydhc_startIndex = html_str.find('src=\"', smydhc_firstIndex - 100)
smydhc_endIndex = html_str.find('\"', smydhc_startIndex + 5)
smydhc_url = html_str[smydhc_startIndex + 5 : smydhc_endIndex]

print smhb_url
print smydhc_url

# 获取“收益走势图”的数据
smhb_req = urllib2.Request(url=smhb_url)
smhb_data = urllib2.urlopen(smhb_req).read()
# output.write(smhb_data)

# 从'navList:['开始，就一直查找“[ ]”即可，里边的是空的，就直接加上空也不会影响结果。
smhb_data_key = ['navList:[', 'navStrListOneYear:[', 'navStrListTwoYears:[', 'navStrListThreeYears:[', 'navStrListFiveYears:[', 'navStrListJnylDay:[']

smhb_data_firstStartIndex = smhb_data.find('navList:[', 0)
smhb_data_firstEndIndex = smhb_data.find(']', smhb_data_firstStartIndex)
smhb_data_list_string = smhb_data[smhb_data_firstStartIndex + 9 : smhb_data_firstEndIndex]



# output.write(smhb_data_list_string)



# 获取“回撤走势图”的数据
# smydhc_req = urllib2.Request(url=smydhc_url)
# smydhc_data = urllib2.urlopen(smydhc_req).read()



output.close()