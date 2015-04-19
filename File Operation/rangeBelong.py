import bisect

# judge which range is n belongs to
n = 101 # (101, 300), if n = 100, print (1, 100),
# which means [1,101,301,1000] create ranges : 1 <= n <= 100, 101 <= n <= 300, 301 <= n <= 999
r = bisect.bisect([1,101,301,1000], n)

if r == 1:
    print "(1, 100)"
elif r == 2:
    print "(101, 300)"
elif r == 3:
    print "(301, 999)"
else :
	print ">= 1000"