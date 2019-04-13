# -*- coding: utf-8 -*-
# Created by xj on 2019/4/8

import os

#获取当前工程路径
res=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]


#获取测试数据路径
test_data_path=os.path.join(res,'data','API_TEST.xlsx')

#获取测试报告路径
test_report_path=os.path.join(res,'result','test_report','test_report.html')
#获取测试日志路径
test_log_path=os.path.join(res,'result','test_log','test_log.log')

#获取配置文件路径
test_conf_path=os.path.join(res,'case_conf','api_conf.conf')
