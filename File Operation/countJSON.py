# -*- coding: utf-8 -*-
import json
import os
import bisect

lengthSum = 0
totalnums = 0
rootDir = './Inputs/'
for root, dirs, files in os.walk(rootDir) :
    for filepath in files :
        # print filepath
        f = file("./Inputs/" + filepath)
        mInput = "./Inputs/" + filepath
        print mInput
        mjson = json.load(f)
        mOutput = open('./Outputs/'+filepath, 'w')
        mjsonData = set()
        for data in mjson :
            mjsonData.add(data['content'])
            # mOutput.write("%s\n" % data['content'])
        
        # for data in mjsonData :
        #     content = data.strip()
        #     content = content.strip('\n')
        #     if not (content == None or len(content) == 0) :
        #         lengthSum += len(content)
        #         totalnums += 1
        #         mOutput.write("%s\n" % content)
        mOutput.close()


print lengthSum
print totalnums
print float(lengthSum) / float(totalnums)