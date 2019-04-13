# -*- coding: utf-8 -*-
# Created by xj on 2019/4/9
import re
import time
import random
from api_project.common.my_config import MyConfig
from api_project.common.do_mysql import DoMysql
def get_db_mobile():
    '获取sendMcode库中的手机号'
    new_mobile_list=[]
    old_mobile=DoMysql().do_mysql('SELECT Fmobile_no FROM sms_db_69.t_mvcode_info_5',flag=1)
    for i in old_mobile:
        new_mobile_list.append(i[0])
    return new_mobile_list
def creat_phone():
    '创建一个随机的手机号 后三位为569'
    #(13\d|14[579]|15[^4\D]|17[^49\D]|18\d)\d{8}
    #第二位数字
    second=[3,4,5,7,8][random.randint(0,4)]
    #第三位数字
    third={3:random.randint(0,9),
           4:[5,7,9][random.randint(0,2)],
           5:[i for i in range(10) if i !=4][random.randint(0,8)],
           7:[i for i in range(10) if i not in [4,9]][random.randint(0,7)],
           8:random.randint(0,9)}[second]
    #中间5位
    suffix=random.randint(00000,99999)
    random_mobile = "1{}{}{}569".format(second, third, suffix)
    return random_mobile
def final_mobile():
    '判断手机号是否在sendMcode中'
    c=creat_phone()
    d=get_db_mobile()
    while c in d:
        c=creat_phone()
    return c
def get_db_userid():
    '获取注册表中所有的useid'
    new_userid_list=[]
    old_userid=DoMysql().do_mysql('SELECT Fuser_id FROM user_db.t_user_info',flag=1)
    for i in old_userid:
        new_userid_list.append(i[0])
    return new_userid_list
def creat_user_id():
    '随机生成userid'
    s=random.sample('abcdef1234567890',6) #返回列表  包含6位元素
    t="".join(s) #将列表转换成字符串
    return t #生成新的字符串
def final_user_id():
    '判断userid是否在注册表中存在'
    a=creat_user_id()
    b=get_db_userid()
    while a in b:
        a=creat_user_id()
    return a
def rechage_time(s):#s必须为2018-09-02 09:09:43这种格式传递
    v=time.strptime(s,'%Y-%m-%d %H:%M:%S') #先转换成时间数组，s必须时字符串格式
    r=time.mktime(v) #将时间数组转换为时间戳
    return r
def creat_cardid():
    '随机生成银行卡号'
    v=random.sample('1234567890123453',10)
    t="".join(v)
    cardid='621226'+t
    return cardid

class GetData:
    '创建一个反射类'
    # mobile=MyConfig().get_str('USERREGISTER','mobile') #先注释掉从配置文件中设置注册手机号码这种方式
    mobile=final_mobile() #对于注册接口生成随机号码
    mobile_send=creat_phone()
    userid=final_user_id() #对于注册接口生成随机userid
    v_mobile=final_mobile()#对于验证接口生成随机手机号
    v_userid=final_user_id()#对于验证接口中生成随机的v_userid
    b_mobile=final_mobile()#对于绑定银行卡接口生成随机手机号
    b_userid=final_user_id()#对于绑定银行卡接口生成随机的b_userid
    cardid=creat_cardid()#对于绑定的银行卡接口生成随机银行卡号
def my_replace(p,target):
    '创建一个利用正则方式进行字符串替换的函数'
    while re.search(p,target):
        v=re.search(p,target) #返回匹配对象
        key=v.group(1) #返回匹配到的组信息
        value=getattr(GetData,key) #反射获取属性值
        target=re.sub(p,value,target,count=1)#p表示匹配模式，value代表被替换后的字符串，target目标字符串，count每次之替换一个
    return target #返回被替换后的字符串

if __name__ == '__main__':
    s=get_db_userid()
    print(s)
    v=creat_cardid()
    print(v)