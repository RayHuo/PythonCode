# -*- coding: utf-8 -*-
# 上面那句是必须的，这样这个py文件中才能出现中文
import json
import xml.dom.minidom
import bisect
import os

# 目的是把两个文件夹下的json文件和xml文件分别都提取内容，转成txt

id = 1

# JSON
rootDir = './Input/AZhan'
for root, dirs, files in os.walk(rootDir) :
    for filepath in files :
        outputFile = './Output/db/db' + ("%03d" % id) + '.txt'
        mOutput = open(outputFile, 'w')
        filename = './Input/AZhan/' + filepath
        mjson = json.load(file(filename), encoding="utf-8")

        for data in mjson :
        	mOutput.write("%s\n" % data['m']);
        mOutput.close()

        id += 1

# xml
rootDir = './Input/BZhan'
for root, dirs, files in os.walk(rootDir) :
    for filepath in files :
        outputFile = './Output/db/db' + ("%03d" % id) + '.txt'
        mOutput = open(outputFile, 'w')
        filename = './Input/BZhan/' + filepath
        xmlDom = xml.dom.minidom.parse(filename)
        root = xmlDom.documentElement
        comments = root.getElementsByTagName('d')   # all comments in a file

        for c in comments :
        	mOutput.write("%s\n" % c.firstChild.data)
        mOutput.close()
        id += 1