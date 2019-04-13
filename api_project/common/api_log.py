# -*- coding: utf-8 -*-
# Created by xj on 2019/4/9
import logging
from api_project.common.real_path import test_log_path
from api_project.common.my_config import MyConfig
formatter_log=MyConfig().get_str('LOG','formatter_log') #从配置文件中获取日志格式
ch_level=MyConfig().get_str('LOG','ch_level') #从配置文件中获取控制台渠道日志级别
fh_level=MyConfig().get_str('LOG','fh_level') #从配置文件中获取文件渠道日志级别
logger_level=MyConfig().get_str('LOG','logger_level') #从配置文件中获取日志收集器的级别
class Mylog:
    '定义一个日志类'
    def mylog(self,level,msg):
        logger=logging.getLogger('xiaojian') #设置日志收集器名称
        logger.setLevel(logger_level) #设置日志收集器级别
        if not logger.handlers: #如果日志收集器中没有渠道则运行下面代码进行新增
            #设置输出日志收集器的级别
            formatter=logging.Formatter(formatter_log)
            #创建控制台渠道
            ch=logging.StreamHandler() #默认输出到控制台渠道
            ch.setLevel(ch_level) #设置输出日志收集器的级别
            ch.setFormatter(formatter) #设置输出到控制台的日志级别
            #创建文件渠道
            fh=logging.FileHandler(test_log_path,encoding='utf-8') #创建文件渠道
            fh.setLevel(fh_level) #设置输出到日志文件中的日志级别
            fh.setFormatter(formatter)#设置输出到文件中的格式
            #日志收集器与渠道进行对接
            logger.addHandler(ch)
            logger.addHandler(fh)
        if level=='DEBUG': #如果日志级别等于debug，则打印debug信息msg
            logger.debug(msg)
        elif level=='INFO':
            logger.info(msg)
        elif level =='WARNING':
            logger.warning(msg)
        elif level=='ERROR':
            logger.error(msg)
        elif level=='CRITICAL':
            logger.critical(msg)
        else:
            print('你输入的日志级别level参数有误，请检查！')
    def debug(self,msg): #为什么要重新定义一个debug呢？是为了少传一个level参数，所以用来调用mylog方法
        self.mylog('DEBUG',msg) #这里需要注意一下，这里调用debug方法使用新设置的日志收集器来进行调用的
    def info(self,msg):
        self.mylog('INFO',msg)
    def warning(self,msg):
        self.mylog('WARNING',msg)
    def error(self,msg):
        self.mylog('ERROR',msg)
    def critical(self,msg):
        self.mylog('CRITICAL',msg)
if __name__ == '__main__':
    Mylog().error("NIAHO")