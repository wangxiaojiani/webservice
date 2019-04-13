# -*- coding: utf-8 -*-
# Created by xj on 2019/4/9
from configparser import ConfigParser
from api_project.common.real_path import test_conf_path
class MyConfig:
    '建立一个配置类'
    def __init__(self):#注意这里是将配置文件写死了
        self.c=ConfigParser() #创建对象,将对象作为另外一个类的属性方便取调用下边的方法
        self.c.read(test_conf_path,encoding='utf-8') #打开配置文件

    def get_str(self,option,section):#获取字符串类型
        return self.c.get(option,section)
    def get_int(self,option,section):#获取整型
        return self.c.getint(option,section)
    def get_float(self,option,section):#获取浮点型数据
        return self.c.getfloat(option,section)
    def get_list(self,option,section): #获取列表，字典，元组
        return eval(self.get_str(option,section))
if __name__ == '__main__':
    s=MyConfig().get_list('USERREGISTER','button')
    print(type(s))
