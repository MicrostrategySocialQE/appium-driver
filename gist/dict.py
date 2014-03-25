__author__ = 'Zhenyu'


import types


class test:
    a = "aaa"
    b = "bbb"


t = {a:getattr(test, a) for a in dir(test)}
print t