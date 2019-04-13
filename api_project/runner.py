# # -*- coding: utf-8 -*-
# # Created by xj on 2019/4/9
# import unittest
# from api_project.test_data import sendMCode_test_case
# from HTMLTestRunnerNew import HTMLTestRunner
# from api_project.common.real_path import test_report_path
# from api_project.test_data import userRegister_test_case
# from api_project.test_data import verifiedUserAuth_test_case
# from api_project.test_data import bindBankCard_test_case
# suit=unittest.TestSuite()#创建测试套件对象
# loader=unittest.TestLoader()#创建loader对象
# suit.addTest(loader.loadTestsFromModule(sendMCode_test_case)) #添加发送验证码用例
# suit.addTest(loader.loadTestsFromModule(userRegister_test_case)) #添加注册接口用例
# suit.addTest(loader.loadTestsFromModule(verifiedUserAuth_test_case)) #添加安全验证信息
# suit.addTest(loader.loadTestsFromModule(bindBankCard_test_case)) #添加手机绑定银行卡用例
# #生成测试报告
# with open(test_report_path,'wb') as f:
#     runner=HTMLTestRunner(stream=f,verbosity=2,title='websevice项目api_test报告',description='websevice项目实战',tester='xiaojian')
#     runner.run(suit) #将用例集添加到suit套件
# #
import sys
print(sys.path)