# -*- coding: utf-8 -*-
# �����Ǿ��Ǳ���ģ��������py�ļ��в��ܳ�������

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
 �������header����Ϣ����ֱ�Ӵ�chrome���ҵ���
 �󲿷�������ִ��ʱ�����ں鷶���ʣ��ᱻ�Է���������ֹ���ʡ���ʱ������������Ǹ����ʼ���һ��header��
 ���header�Ĺ��ܾ���Ϊ��αװ��ǰ��������������еģ�����������ķ��ʣ��Է�ֹ����ֹ����
 ���һ�䣺ֻҪ������ܷ��ʸ���ַ�������벻�У���϶��Ǵ������⡣��Ϊ������ܷ��ʣ�����ipû�б�������
 ֻ�Ƿ��ʷ���ȥ�ġ���ͷ����ͬ����������İ�ͷ�Ϳ���αװ������������İ���

 ���⣬һ������ httperror 403 forbidden �������������������з���һ�¸���ַ��Ȼ�������������̨��network���ҵ�
 ��η�����header�ľ������ݣ������µ�cookie�滻�������cookie����

 ���⣬�����������ͻȻ�����ˣ������Ǳ�host�ķ�������Ϊ�ǻ������ʣ���Ҫ����ʧ�ܵ��Ǹ���ַ��
 Ȼ�����Ҫ��������֤��ȷ������Ϊ���ʡ�
"""
m_header = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        # "Accept-Encoding":"gzip,deflate,sdch",    # ����ᵼ�·���16�����룬��Ҫɾ��
        "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        "Host" : "taobao.com",
        "Cookie" : '�Լ����������',
        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36" }


for rowIndex in range(0, rowSize) :
    fileName = "./outputs/" + table.row(rowIndex)[0].value + ".txt"     # ��ǰ���еĵ�һ��ֵ���ļ���
    original_url = table.row(rowIndex)[1].value         # ��ǰ���еĵڶ���ֵ��url 

    question_mark = original_url.find('?')
    if question_mark != -1 :
        original_url = original_url[0 : question_mark]
    url = original_url + comment_tail

    print "File : %s\n" % fileName

    getHTTP = open(fileName, 'a+')        # aΪ׷��д�ļ���+Ϊ�ļ��������򴴽�
    getHTTP.truncate()                    # ÿ���ܶ����һ���ļ�

    # getHTTP = open('hold.txt', 'a+')    # aΪ׷��д�ļ���+Ϊ�ļ��������򴴽�
    # getHTTP.truncate()                  # ÿ���ܶ����һ���ļ�
    # httphold = open('httphold.txt', 'w')

    next_url_pre = url[0:url.find('?')]

    # tmp_hold = open('tmp_hold.txt', 'w')
    print "Open url : %s\n" % url
    req = urllib2.Request(url=url, headers=m_header)
    html_str = urllib2.urlopen(req).read()
    # tmp_hold.write(html_str)
    # tmp_hold.close()

    total_site = '<span class="total">(�� '
    total_comment = ''
    total_comment_start = html_str.find(total_site)

    # �ض������ҳ�ˣ���ʱ�������site��������һ��
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

    total_page_index = 100 # ÿҳ20����100ҳΪ2000��

    if total_page < total_page_index : 
        total_page_index = total_page


    # ��ʼץȡ
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
            
            # ����Ϊ�˱����ֻ��û���������ʱ��ҳ�Ĳ��淶
            phone_comment = html_str.find('<a class="source-icon"', start_index, end_index)
            if phone_comment != -1 :
                comment = html_str[start_index+12 : phone_comment-1]
                space_index = comment.find(' ')
                comment = comment[:space_index]
            else : 
                comment = html_str[start_index+12 : end_index-8]
            getHTTP.write(comment)


        next_url_end = html_str.find('" data-page="" class="next">��һҳ', end_index + 1)
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