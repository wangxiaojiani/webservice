# -*- coding: utf-8 -*-
# Created by xj on 2019/4/9
"""测试验证码用例，利用ddt"""
import unittest
from api_project.common.do_excel import DoExcel #导入Doexcel类用来读取测试数据
from api_project.common.real_path import test_data_path #导入测试数据路径
from ddt import ddt,data #导入ddt框架
from api_project.common.web_http import Webhttp #导入测试的接口类
from api_project.common.api_log import Mylog #导入日志类
from api_project.common.my_config import MyConfig
from api_project.common.get_data import my_replace
from api_project.common.do_mysql import DoMysql
from api_project.common.get_data import GetData

host=MyConfig().get_str('VERIFYUSERAUTH','host') #从配置文件中获取host主机地址
test_data=DoExcel(test_data_path,"verifiedUserAuth").do_excel('VERIFYUSERAUTH') #读取测试数据
mylog=Mylog()#创建一个日志对象
@ddt
class verifyUserAuthTest(unittest.TestCase):
    '定义一个实名验证的测试类'
    def setUp(self):
        mylog.info("开始执行用例啦")
        self.t=DoExcel(test_data_path,"verifiedUserAuth")
    def tearDown(self):
        mylog.info("用例执行结束了")
    @data(*test_data)
    def test_verifyUserAuth(self,case):
        global sql
        mylog.info("开始执行第{}条用例，用例的标题是{}".format(case['Case_id'], case['Title']))
        mylog.info('测试数据为{}'.format(case))
        url=host + case['Url']
        params=my_replace('#(.*?)#',case['Params']) #生成随机手机号将用例中的v_mobile进行替换
        print(eval(params))
        if case['Sql'] !=None:
            sql=my_replace('#(.*?)#',case['Sql'])
        if case['Case_id'] ==1:
            res=Webhttp(url,eval(params)).web_sendMCode()
            verity_code = DoMysql().do_mysql(eval(sql)['sql']) #获取验证码，并将其反射
            setattr(GetData,'v_CODE',str(verity_code[0]))

        elif case['Case_id']==2:
            res=Webhttp(url,eval(params)).web_userRegister() #发起注册请求
            v_uid=DoMysql().do_mysql(eval(sql)['sql_4']) #获取uid并且将其反射
            setattr(GetData,'v_uid',str(v_uid[0]))
        else:
            print(eval(sql))
            print(eval(params))
            res=Webhttp(url,eval(params)).web_verifyUserAuth()#发起验证请求
        try:
            if case['Sql'] !=None and case['Sql'].find('sql_5') !=-1:
                count=DoMysql().do_mysql(eval(sql)['sql_4'])[0] #查找验证成功的行数
                md_mobile=DoMysql().do_mysql(eval(sql)['sql_5'])[0] #获取身份证中的手机号码
                md_creid=DoMysql().do_mysql(eval(sql)['sql_5'])[1] #获取数据库中的身份证号
                self.assertEqual(1,count) #断言影响行数
                self.assertNotEqual(md_mobile,getattr(GetData,'v_mobile'))
                self.assertNotEqual(md_creid,eval(params)['cre_id'])
            self.assertEqual(eval(case['Expect_Result']),res)
            test_result='Pass'
        except Exception as e:
            mylog.error("断言出错了，错误是{}".format(e))
            test_result='Failed'
            raise e
        finally:
            self.t.write_back(case['Case_id']+1,8,str(res))
            self.t.write_back(case['Case_id']+1,9,test_result)
            mylog.info("第{}条用例执行后的实际结果是{}".format(case['Case_id'], res))
            mylog.info("第{}条用例测试后的执行结果是{}".format(case['Case_id'], test_result))




