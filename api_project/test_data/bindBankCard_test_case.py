# -*- coding: utf-8 -*-
# Created by xj on 2019/4/13

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

host=MyConfig().get_str('BINDBANKCARD','host') #从配置文件中获取host主机地址
test_data=DoExcel(test_data_path,"bindBankCard").do_excel('BINDBANKCARD') #读取测试数据
mylog=Mylog()#创建一个日志对象
@ddt
class BindBankCaedTest(unittest.TestCase):
    '定义一个绑定接口请求的测试类'
    def setUp(self):
        mylog.info("开始执行用例啦")
        self.t=DoExcel(test_data_path,"bindBankCard")
    def tearDown(self):
        mylog.info("用例执行结束了")
    @data(*test_data)
    def test_bindBankCard(self,case):
        global sql
        mylog.info("开始执行第{}条用例，用例的标题是{}".format(case['Case_id'], case['Title']))
        mylog.info('测试数据为{}'.format(case))
        url=host + case['Url']
        params=my_replace('#(.*?)#',case['Params']) #生成随机手机号将用例中的v_mobile进行替换
        if case['Sql'] !=None:
            sql=my_replace('#(.*?)#',case['Sql'])
        if case['Case_id'] ==1:
            res=Webhttp(url,eval(params)).web_sendMCode()
            verity_code = DoMysql().do_mysql(eval(sql)['sql']) #获取验证码，并将其反射
            setattr(GetData,'b_CODE',str(verity_code[0]))
        elif case['Case_id']==2:
            res=Webhttp(url,eval(params)).web_userRegister() #发起注册请求
            b_uid=DoMysql().do_mysql(eval(sql)['sql_4']) #获取uid并且将其反射
            setattr(GetData,'b_uid',str(b_uid[0]))
            last_second=getattr(GetData,'b_uid')[-2:] #获取uid后两位数字
            last_third=getattr(GetData,'b_uid')[-3:-2] #获取uid后第三位数字
            setattr(GetData,'last_second',last_second) #将后两位进行反射
            setattr(GetData,'last_third',last_third)#将第三位进行反射
        elif case['Case_id']==3:
            res=Webhttp(url,eval(params)).web_verifyUserAuth()#发起验证请求
            setattr(GetData,"CRE_ID_NEW",eval(params)['cre_id']) #这里将身份证号反射  因为绑定银行卡要求手机号一直 之前每次调用都是+1
            name = DoMysql().do_mysql(eval(sql)['sql_8'])[0]  # 获取数据库中的truename
            cre_num_v =DoMysql().do_mysql(eval(sql)['sql_5'])[1] #获取数据数据库验证表中的身份证号
        else:
            res=Webhttp(url,eval(params)).web_bindBankCard()#发起绑定接口请求
            cre_num_b = DoMysql().do_mysql(eval(sql)['sql_6'])[0]  # 获取数库中的身份证号
            user_name = DoMysql().do_mysql(eval(sql)['sql_6'])[1]  # 获取数据库中的身份证号
            state_b=DoMysql().do_mysql(eval(sql)['sql_6'])[2]  #获取验证状态
        try:
            if case['Case_id'] ==4:
                self.assertEqual(eval(case['Expect_Result']),res)
                self.assertEqual(cre_num_v,cre_num_b)
                self.assertEqual(name,user_name)
                self.assertEqual(3,state_b)
            else:
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




