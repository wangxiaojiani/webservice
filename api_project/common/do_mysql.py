# -*- coding: utf-8 -*-
# Created by xj on 2019/4/9
import pymysql
from api_project.common.my_config import MyConfig
db_config=MyConfig().get_list('DB','db_config')

class DoMysql:
    def do_mysql(self,query,flag=2):
        '创建一个读取数据库数据的方法'
        # #准备数据库基本信息  这里的数据库名称是根据手机号来进行配置的,这里的key不要乱写 是固定的
        # db_config={'host':'120.24.235.105','port':3306,'user':'python','password':'python666','database':'sms_db_68'}
        #首先建立连接
        con=pymysql.connect(**db_config)
        #建立游标
        cur=con.cursor()
        #执行查询语句
        cur.execute(query)
        # #如果执行的是修改语句还要进行commit
        # cur.execute('commit')
        #返回查询结果
        if flag == 1:
            res=cur.fetchall() #返回所有记录，类型为元组，里面嵌套的也是元组，嵌套的元组为每一条记录
        else:
            res=cur.fetchone() #返回一条记录，类型为元组
        #关闭数据库连接
        con.close()
        return res
if __name__ == '__main__':
    query="SELECT Fmobile,Fcre_id FROM user_db.t_user_auth_info WHERE Fuid ='100005223'"
    res=DoMysql().do_mysql(query)
    print(res)

