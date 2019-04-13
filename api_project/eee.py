# -*- coding: utf-8 -*-
# Created by xj on 2019/4/10
import random

# s=random.sample('abcdef123455',6)
# print(s)
# print(type(s))
# t="".join(s)
# print(t)
# print(type(t))
# s=['oojian', 'xiaojian']
def creat_user_id():
    s=random.sample('abcdefkkeqeq',6) #返回列表  包含6位元素
    t="".join(s) #将列表转换成字符串
    return t #生成新的字符串
s=creat_user_id()
print(s)