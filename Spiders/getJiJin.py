# -*- coding: utf-8 -*-
# 上面那句是必须的，这样这个py文件中才能出现中文

import urllib2
import math
import string
import json
import xlrd


url = "http://simu.howbuy.com/mlboard.htm"

req = urllib2.Request(url=url)
html_str = urllib2.urlopen(req).read()

tmp_hold = open('JiJin.txt', 'w')
startSite = 0
for i in range(0, 20) :
	startIndex = html_str.find('tdlt', startSite)
	startIndex = html_str.find('href="', startIndex)
	endIndex = html_str.find('"', startIndex+6)
	jijin_url = html_str[startIndex+6 : endIndex]
	startSite = endIndex
	tmp_hold.write(jijin_url + '\n')

tmp_hold.close()


