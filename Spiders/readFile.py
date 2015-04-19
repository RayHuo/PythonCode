import urllib2

input = open('urls.txt', 'r')
output = open('outs.txt', 'w')
while 1 :
	url = input.readline()
	if not url:
		break
	print url
	strr = urllib2.urlopen(url).read()
	output.write(strr)
input.close()
output.close()