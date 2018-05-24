# from datetime import datetime, timedelta
# import time


# print(dir(datetime))

# a = datetime.now()
# time.sleep(5)
# b = datetime.now()

# x = a - b

# print("td=",x)

# c = datetime.datetime.now()
# print(c)

import datetime
from datetime import datetime as d, timedelta

Y = datetime.datetime.now()

dt2 = datetime.datetime(2018,10,21,16,29,0)
dt = datetime.datetime(2018,10,21,19,30,0)

# x = datetime.timedelta(dt-dt2)
x = datetime.timedelta(days=dt.day)

print(dt2)
print(type(dt2-x))
print(type(x))
print(type(dt.day))
print(type(dt))

s = 13420
hours, remainder = divmod(s, 3600)
minutes, seconds = divmod(remainder, 60)

x = "{}:{}:{}".format(hours,minutes,seconds)

print(x)
y = x.split(":")
print(y[0])

minutes = divmod(s,60)
me = minutes[0] + minutes[1]
print(minutes," ",me)

print(round(53.45,0))
