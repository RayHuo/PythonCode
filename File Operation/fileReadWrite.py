import random

# mInput = open('./test/input.txt', 'r')
# mOutput = open('./test/output.txt', 'w')
# for line in mInput.readlines() :
#     mOutput.write(line)
# mInput.close()
# mOutput.close()


# create my sql command
mSQL = open('./test/sql.txt', 'w')

# speed = [20, 50]
# fontsize = ['20px', '22px', '25px']
# lineheight = [1, 1.3, 1.6]

sql = 'INSERT INTO nv_video (id, type, picture, nicovideo, question, answer) VALUES '
type = 'douban'
picture = 'Public/doubanScreen/db' # Public/doubanScreen/db001.png
nicovideo = 'Public/doubanText/db' # db001.txt
question = 'question' # question1
# answer random for 1, 2 or 3

# for id in range(1, 37) : 
for id in range(36, 51) :
    value = ''
    answer = random.randint(1, 3)   # random 1, 2, 3
    value += '(' + `id` + ', \"' + type + '\", \"' + picture + ("%03d" % id) + '.png\", \"' + nicovideo + ("%03d" % id) + '.txt\", \"' + question + `id` + '\", ' + `answer` + ')'
    sql += value + ', '
    


sql = sql[0:len(sql)-2:] + ';'
mSQL.write(sql)
mSQL.close()