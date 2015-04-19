# -*- coding: utf-8 -*-
# 上面那句是必须的，这样这个py文件中才能出现中文

import urllib2
import math
import string
import json
import xlrd


urls = xlrd.open_workbook('Comment.xls')
table = urls.sheets()[0]    # get sheet1

rowSize = table.nrows       # get row size

comment_tail = "comments?sort=new_score"

"""
 以下这个header的信息都是直接从chrome里找到的
 大部分爬虫在执行时，由于洪范访问，会被对方服务器禁止访问。这时，解决方案就是给访问加上一个header，
 这个header的功能就是为了伪装当前访问是浏览器进行的，是正常合理的访问，以防止被禁止掉。
 外加一句：只要浏览器能访问该网址，而代码不行，则肯定是代码问题。因为浏览器能访问，所以ip没有被禁掉，
 只是访问发过去的“包头”不同，加了下面的包头就可以伪装成事浏览器发的包。

 另外，一旦出现 httperror 403 forbidden 的情况，可以在浏览器中访问一下该网址，然后在浏览器控制台的network里找到
 这次发包的header的具体内容，把最新的cookie替换掉这里的cookie即可

 另外，如果是运行着突然不行了，可能是被host的服务器认为是机器访问，需要访问失败的那个网址，
 然后根据要求输入验证码确认是人为访问。
"""
m_header = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        # "Accept-Encoding":"gzip,deflate,sdch",    # 这个会导致返回16进制码，需要删掉
        "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        "Host" : "taobao.com",
        "Cookie" : '自己在浏览器看',
        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36" }


for rowIndex in range(0, rowSize) :
    fileName = "./outputs/" + table.row(rowIndex)[0].value + ".txt"     # 当前行中的第一个值，文件名
    original_url = table.row(rowIndex)[1].value         # 当前行中的第二个值，url 

    question_mark = original_url.find('?')
    if question_mark != -1 :
        original_url = original_url[0 : question_mark]
    url = original_url + comment_tail

    print "File : %s\n" % fileName

    getHTTP = open(fileName, 'a+')        # a为追加写文件，+为文件不存在则创建
    getHTTP.truncate()                    # 每次跑都清空一下文件

    # getHTTP = open('hold.txt', 'a+')    # a为追加写文件，+为文件不存在则创建
    # getHTTP.truncate()                  # 每次跑都情况一下文件
    # httphold = open('httphold.txt', 'w')

    next_url_pre = url[0:url.find('?')]

    # tmp_hold = open('tmp_hold.txt', 'w')
    print "Open url : %s\n" % url
    req = urllib2.Request(url=url, headers=m_header)
    html_str = urllib2.urlopen(req).read()
    # tmp_hold.write(html_str)
    # tmp_hold.close()

    total_site = '<span class="total">(共 '
    total_comment = ''
    total_comment_start = html_str.find(total_site)

    # 重定向回主页了，暂时不管这个site，尝试下一个
    if total_comment_start == -1 :
        continue

    total_comment_end = total_comment_start + len(total_site)
    while True :
        if html_str[total_comment_end] == ' ' :
            break
        total_comment += html_str[total_comment_end]
        total_comment_end += 1   
    print total_comment

    total_page = string.atoi(total_comment, 10) / 20

    total_page_index = 100 # 每页20条，100页为2000条

    if total_page < total_page_index : 
        total_page_index = total_page


    # 开始抓取
    for i in range(0, total_page_index) : 
        
        # html_str = urllib2.urlopen(url).read()
        req = urllib2.Request(url=url, headers=m_header)
        html_str = urllib2.urlopen(req).read()
        # httphold.write(html_str)
        # httphold.close()

        print "Page%d  URL %s\n" % (i, url)

        start_index = 0
        end_index = 0
        comment = ''

        while True :
            start_tmp = html_str.find('<p class=""> ', start_index)
            if start_tmp == -1 :
                break

            start_index = start_tmp + 1
            end_index = html_str.find('</p>', start_index)
            if end_index == -1 :
                break
            
            # 这是为了避免手机用户发送评论时网页的不规范
            phone_comment = html_str.find('<a class="source-icon"', start_index, end_index)
            if phone_comment != -1 :
                comment = html_str[start_index+12 : phone_comment-1]
                space_index = comment.find(' ')
                comment = comment[:space_index]
            else : 
                comment = html_str[start_index+12 : end_index-8]
            getHTTP.write(comment)


        next_url_end = html_str.find('" data-page="" class="next">后一页', end_index + 1)
        next_url_start = next_url_end - 1
        next_url = ''
        if next_url_end != -1 : 
            while html_str[next_url_start] != '"' : 
                next_url_start -= 1
            next_url = next_url_pre + html_str[next_url_start + 1 : next_url_end]


        if len(next_url) == 0 :
            break
        else :
            url = next_url
    print "\n"

    getHTTP.close()