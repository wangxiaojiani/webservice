# -*- coding: utf-8 -*-
# Created by xj on 2019/4/8
"""测试验证码用例，利用ddt"""
import unittest
from api_project.common.do_excel import DoExcel #导入Doexcel类用来读取测试数据
from api_project.common.real_path import test_data_path #导入测试数据路径
from ddt import ddt,data #导入ddt框架
from api_project.common.web_http import Webhttp #导入测试的接口类
from api_project.common.api_log import Mylog #导入日志类
from api_project.common.my_config import MyConfig
from api_project.common.get_data import creat_phone
from api_project.common.get_data import my_replace,rechage_time
import re
host=MyConfig().get_str('SENDMCODE','host') #从配置文件中获取host主机地址
test_data=DoExcel(test_data_path,"sendMCode").do_excel('SENDMCODE') #读取测试数据
mylog=Mylog()#创建一个日志对象
@ddt
class SendMCodeTest(unittest.TestCase):
    '定义一个测试验证码的测试类'
    def setUp(self):
        mylog.info("开始执行用例啦")
        self.t=DoExcel(test_data_path,"sendMCode")
    def tearDown(self):
        mylog.info("用例执行结束了")
    @data(*test_data)
    def test_sendMCode(self,case):
        url=host + case['Url']
        params=my_replace('#(.*?)#',case['Params']) #替换用例中的手机号并且把值赋给case对象，因为下面会打印case
        mylog.info("开始执行第{}条用例，用例的标题是{}".format(case['Case_id'],case['Title']))
        mylog.info('测试数据为{}'.format(case))
        res =Webhttp(url,eval(params)).web_sendMCode()
        try:
            self.assertEqual(eval(case['Expect_Result']),res) #得到的case  res是列表类型的
            test_result='Pass'
        except Exception as e:
            mylog.error("断言出错了，错误是{}".format(e))
            test_result ='Failed'
            raise e
        finally:
            self.t.write_back(case['Case_id']+1,8,str(res))
            self.t.write_back(case['Case_id']+1,9,test_result)



