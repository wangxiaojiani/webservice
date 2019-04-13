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
from api_project.common.get_data import GetData,rechage_time

host=MyConfig().get_str('USERREGISTER','host') #从配置文件中获取host主机地址
test_data=DoExcel(test_data_path,"userRegister").do_excel('USERREGISTER') #读取测试数据
mylog=Mylog()#创建一个日志对象
@ddt
class UserRegisterTest(unittest.TestCase):
    '定义一个注册接口的测试类'
    def setUp(self):
        mylog.info("开始执行用例啦")
        self.t=DoExcel(test_data_path,"userRegister")
    def tearDown(self):
        mylog.info("用例执行结束了")
    @data(*test_data)
    def test_userRegister(self,case):
        mylog.info("开始执行第{}条用例，用例的标题是{}".format(case['Case_id'], case['Title']))
        mylog.info('测试数据为{}'.format(case))
        url=host + case['Url']
        params=my_replace('#(.*?)#',case['Params']) #生成随机手机号将用例中的mobile进行替换
        if case['Sql'] !=None:
            case['Sql']=my_replace('#(.*?)#',case['Sql']) #替换sql中的手机号和userid
            sql=case['Sql']
        if case['Case_id']==1:
            res =Webhttp(url,eval(params)).web_sendMCode() #发起发送验证码请求
            verity_code = DoMysql().do_mysql(eval(sql)['sql']) #获取验证码，并将其反射
            setattr(GetData, 'CODE',str(verity_code[0]))
            experid_time_test =DoMysql().do_mysql(eval(sql)['sql_1'],flag=2)[0] #获取过期验证码过期时间
            experid_time=rechage_time(str(experid_time_test)) #发射过期时间戳  从数据库中获得的时间为datatime类型 必须要转为str
            setattr(GetData,'experid_time',experid_time) #反射
        else:
            res=Webhttp(url,eval(params)).web_userRegister() #发起注册请求

        now_time_1=str(DoMysql().do_mysql('SELECT NOW()',flag=2)[0])
        now_time=rechage_time(now_time_1) #获得数据库的当前时间

        try:
            if getattr(GetData,'experid_time') - now_time >0 and case['Case_id'] != 12:
                if case['Sql'] != None and case['Sql'].find('sql_2') != -1: #去判定哪个用例时成功注册的用例
                    count_first = DoMysql().do_mysql(eval(sql)['sql_2'])[0]  # 成功注册之后查询影响行数
                    self.assertEqual(1,count_first) #断言影响行数是否为1
                    md_pwd=DoMysql().do_mysql(eval(sql)['sql_3'])[0]
                    md_mobile=DoMysql().do_mysql(eval(sql)['sql_3'])[1]
                    self.assertNotEqual(md_mobile,eval(params)['mobile']) #断言手机号与数据库中不相等
                    self.assertNotEqual(md_pwd,eval(params)['pwd']) #断言密码与数据库中不相等
                self.assertEqual(eval(case['Expect_Result']), res)  # 得到的case  res是列表类型的
            elif getattr(GetData,'experid_time') - now_time <0 and case['Case_id'] ==12:
                self.assertEqual(eval(case['Expect_Result']),res) #得到的case  res是列表类型的
            test_result='Pass'
        except Exception as e:
            mylog.error("断言出错了，错误是{}".format(e))
            test_result ='Failed'
            raise e
        finally:
            self.t.write_back(case['Case_id']+1,8,str(res))
            self.t.write_back(case['Case_id']+1,9,test_result)
            mylog.info("第{}条用例执行后的实际结果是{}".format(case['Case_id'],res))
            mylog.info("第{}条用例测试后的执行结果是{}".format(case['Case_id'],test_result))


