# -*- coding: utf-8 -*-
# Created by xj on 2019/4/8
"""
1.在线安装pip install suds.jurko
2.引入suds库，from suds.client import Client
3.创建webservice对象  client=Client(URL)
4.打印这个client中所有接口信息 print(client)
5.用soapui来查看某个接口的组成和参数
6.将参数当作字典存储t
7.在python中调用这个接口 result=client.service.userRegister(t)
8打印响应结果
本脚本主要定义一个webhttp类用来发起websevice请求
"""
from suds.client import Client #从第三方插件中sus.jurko 中导入suds 在从suds中引入Client类
from api_project.common.api_log import Mylog#导入日志模块
mylog=Mylog()#创建日志对象
class Webhttp:
    '定义一个webhttp类，用来发起webservice请求'
    def __init__(self,url,params):
        self.params =params
        self.url=url
    def web_sendMCode(self):
        '定义一个发起短信验证码的接口'
        try:
            client=Client(self.url) #创建webservice对象
            result_1=client.service.sendMCode(self.params) #发送获取验证码请求，这里params参数必须是字典格式
            mylog.info("====成功发起短信验证码接口请求")
            res_1=[result_1.retCode,result_1.retInfo] #请求成功返回状态码/响应信息
        except Exception as e:
            mylog.error("====发起短信验证请求失败，错误是{}".format(e.fault.faultstring))
            res_1=[e.fault.faultcode,e.fault.faultstring] #请求失败返回错误信息
        return res_1 #返回响应结果
    def web_userRegister(self):
        '定义一个注册接口'
        try:
            client=Client(self.url) #创建一个webservice对象
            result_2 =client.service.userRegister(self.params) #发送获取注册请求
            mylog.info("====成功发起注册接口请求")
            res_2 = [result_2.retCode,result_2.retInfo]  # 请求成功返回状态码
        except Exception as e:
            mylog.error("====发起注册请求失败，错误是{}".format(e.fault.faultstring))
            res_2 = [e.fault.faultcode,e.fault.faultstring] # 请求失败返回错误信息
        return res_2
    def web_verifyUserAuth(self):
        '定义一个实名验证接口'
        try:
            client=Client(self.url) #创建一个webservice对象
            result_3 = client.service.verifyUserAuth(self.params) #发起实名验证请求
            mylog.info("====成功发起实名验证请求")
            res_3 = [result_3.retCode,result_3.retInfo] # 请求成功返回状态码
        except Exception as e:
            mylog.error("====发起实名验证请求失败，错误是{}".format(e.fault.faultstring))
            res_3 = [e.fault.faultcode,e.fault.faultstring] # 请求失败返回错误信息
        return res_3
    def web_bindBankCard(self):
        '定义一个绑定银行卡接口'
        try:
            client =Client(self.url)
            result_4=client.service.bindBankCard(self.params) #发起绑定验证码请求
            mylog.info('====成功发起绑定银行卡请求')
            res_4 =[result_4.retCode,result_4.retInfo]  # 请求成功返回状态码
        except Exception as e:
            mylog.error("====发起绑定银行卡请求失败，错误是{}".format(e.fault.faultstring))
            res_4= [e.fault.faultcode,e.fault.faultstring] # 请求失败返回错误信息
        return res_4

if __name__ == '__main__':
    T={'client_ip':'130.110.289.119','tmpl_id':'1','mobile':'13333322219'}
    s=Webhttp('http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl',T).web_sendMCode()
    print(str(s))


