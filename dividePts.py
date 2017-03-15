# num = number of pts in half

# gap = space btw (in middle) [so gap5 would be obj + 4 more(.8, .6, .4, . 2)]

# firstSecond = num % gap (gap between first second)

# if num is even, then middle pt is two. . . 
# firstSecond = num % gap-1

# ORRRR. . . maybe better
# an imaginary full strength one for both middles, they get second-to-full and work down from there. . . so we're one short on the middle ones
# 1 .8.6.4.20 .2.4.6.81.8.6.4.2     .2.4.6.81
# # - - - - # - - - - # - - - - (#) - - - - # - - - - # - - - - #
# 0 .2.4.6.81.8.6.4.2 0.2.4.6.8    .8.6.4.2
# In this case, beginning/end is half-1 % gap-1


# TEST . . . 
# l = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y"]
# odd = True
# num = 5


# if len(l)%2 == 0:
#     odd = False
#     print "even"
#     frst, sec = l[:len(l)/2], l[len(l)/2:]
    

# else:
#     print "odd"
#     frst, sec = l[:len(l)/2], l[len(l)/2:]

# print len(frst), frst
# print len(sec), sec

# frstSec = len(frst) % (num)
# print "first:", frstSec
# secThird = frstSec + num
# print "second:", secThird

# grp = []
# grp.append(frst[0])
# for i in range(len(frst), frstSec, -5): # count from middle to third (first is custom, second is custom to first)
#     new = []
#     for j in range(num-1, -1, -1): # add lower values first, then value
#         new.append(l[i-j])
#     for j in range(1, num): # add higher values
#         new.append(l[i+j])
#     print "{0}: {1}".format(l[i], new)

# # second to third
# secondL = []
# y1 =  [l[a] for a in range(1, frstSec)] # first half of second
# y2 = [l[a] for a in range(frstSec, frstSec+num)] # second half of second
# for y in y1:
#     secondL.append(y)   
# for y in y2:
#     secondL.append(y)

# print secondL


    