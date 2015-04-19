import urllib2
import math
import string
import json
import xlrd

urls = xlrd.open_workbook('temp.xls')
table = urls.sheets()[0]    # get sheet1

rowSize = table.nrows       # get row size

# input = open('urls.txt', 'r')
# while 1 :
#     url = input.readline()
#     if not url:
#         break
for rowIndex in range(0, rowSize):
    fileName = table.row(rowIndex)[0].value
    url = table.row(rowIndex)[1].value

    print "\nFile ", fileName
    # url = "http://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.8.4QyGuz&id=23702488904&user_id=747138261&is_b=1&cat_id=50025135&q=&rn=d25f9d18be21a6fd41ca0d0284c1b88a"
    strr = urllib2.urlopen(url).read()

    # get itemId from html page strr
    i1 = strr.find("&itemId=")
    # print i1
    if i1 == -1:
        i1 = strr.find("itemId:\"")
        i = i1 + 8
    else :
        i = i1 + 8
    itemId = ""
    
    while strr[i].isdigit() :
        itemId += strr[i]
        i += 1
    print "itemId : ", itemId, ", ", i

    # get spuId from html page strr
    # shopId is the same as spuid. And tmall gets both shopid and spuid, taobao only gets shopid
    i2 = strr.find("&spuId=")   
    # print i2
    if i2 == -1 : 
        i2 = strr.find("shopId:\"") 
        i = i2 + 8 
    else : 
        i = i2 + 7
    # i = i2 + 7
    spuId = ""
    while strr[i].isdigit() :
        spuId += strr[i]
        i += 1
    print "spuId : ", spuId, ", ", i

    # get spuId from html page strr
    i3 = strr.find("&sellerId=")
    # print i3
    i = i3 + 10
    sellerId = ""
    while strr[i].isdigit() :
        sellerId += strr[i]
        i += 1
    print "sellerId : ", sellerId, ", ", i

    # print i1, ", ", i2, ", ", i3

    getCommentPageNumURL = "http://rate.taobao.com/auction_feedbacks.htm?user_num_id=" + sellerId+ "&auction_num_id=" + itemId;
    commentNumResponse = urllib2.urlopen(getCommentPageNumURL).read()

    # find the second <em> index
    start = commentNumResponse.find("<em>")
    start = commentNumResponse.find("<em>", start + 1)

    # find the second </em> index

    end = commentNumResponse.find("</em>")
    end = commentNumResponse.find("</em>", end + 1)

    totalNum = ""
    if start == -1 :
        totalNum += '0'
    else :
        for i in range(start+4, end):
            totalNum += commentNumResponse[i]

    print "Total Comment number is ", totalNum

    # get total comment page num
    total = string.atoi(totalNum, 10)
    aver = 20.0
    pageNum = (int)(math.ceil(total / aver))
    print "Total Page number is ", pageNum


    # get comments
    output = open("outputs/" + fileName + ".txt", 'w')
    for pageIndex in range(1, pageNum+1) :
        getCommentURL = "http://rate.tmall.com/list_detail_rate.htm?callback=jsonp1356746512005&itemId=" + itemId +"&spuId=" + spuId + "&sellerId=" + sellerId + "&order=0&forShop=1&append=0&currentPage=" + str(pageIndex)
        comments = urllib2.urlopen(getCommentURL).read()
        index_ = comments.find('(')
        jsonComments = comments[index_+15 : len(comments)-2]
        jsonComments = jsonComments.decode('gbk', 'ignore').encode('utf-8')

        data = json.loads(jsonComments, encoding="utf-8")
        # print data['rateList'][0]['auctionSku']
       
        num = len(data['rateList'])
        for i in range(0, num):
            if data['rateList'][i]['appendComment'] != "" :
                if data['rateList'][i]['appendComment']['content'] != "" :
                    output.write(unicode.encode(data['rateList'][i]['appendComment']['content'], 'utf-8'))
                    output.write('\n')
            if data['rateList'][i]['rateContent'] != "" :
                output.write(unicode.encode(data['rateList'][i]['rateContent'], 'utf-8'))
                output.write('\n')

    # output.write(unicode.encode(data['rateList'][0]['auctionSku'], 'utf-8'))
    output.close()

# input.close()



# json load example
# th1 = '{"a":"what","b":"the","c":"hell"}'
# th2 = '[{"s":"helloworld","__module__":"jsontest","__class__":"MyObj"}]'
# data = json.loads(th1)


# write file example
# output = open('output.txt', 'w')
# output.write(jsonComments)
# output.close()