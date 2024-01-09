# -*- coding: utf-8 -*-

# @Time : 2022/3/6 9:49 下午
# @Project : sqlDemo
# @File : pymysqlPool.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8

import pymysql
from dbutils.pooled_db import PooledDB
from timeit import default_timer
from readConfig import choiceConfig



''' pymysql数据库连接池封装 '''
#用连接池来返回数据库连接
class PoolConn(object):
    #存储连接池
    __pool = None

    def __init__(self, dbEnv):
        '''
        :param dbEnv: 选择的某个环境的数据库信息
        '''
        if self.__pool is None:
            #print(choiceConfig(dbEnv).get(dbEnv))
            self.__pool = PooledDB(creator=pymysql,
                                   mincached=int(choiceConfig(dbEnv).get(dbEnv).get('mincached')) ,
                                   maxcached=int(choiceConfig(dbEnv).get(dbEnv).get('maxcached')) ,
                                   maxconnections=int(choiceConfig(dbEnv).get(dbEnv).get('maxconns')) ,
                                   host=choiceConfig(dbEnv).get(dbEnv).get('host') ,
                                   port=int(choiceConfig(dbEnv).get(dbEnv).get('port')),
                                   user=choiceConfig(dbEnv).get(dbEnv).get('user') ,
                                   passwd=choiceConfig(dbEnv).get(dbEnv).get('password') ,
                                   db=choiceConfig(dbEnv).get(dbEnv).get('database') ,
                                   charset=choiceConfig(dbEnv).get(dbEnv).get('charset')
                                   )
            
    def get_PoolConn(self):
        return self.__pool.connection()
    
#选择测试环境的数据库
#在程序的开始初始化一个连接池
pool =PoolConn('Test')
print(pool)

# ---- 使用 with 的方式来优化连接的自动关闭
class PoolUtil():
    def __init__(self, commit=True, log_time=True, log_label='总共用时'):
        """
        使用 with 的方式来优化，使用连接池中的连接，自动关闭
        :param commit: 是否在最后提交事务(设置为False的时候方便单元测试)
        :param log_time:  是否打印程序运行总时间
        :param log_label:  自定义log的文字
        """
        self._log_time = log_time
        self._commit = commit
        self._log_label = log_label
        
    #使用with命令的时候，会自动调用该函数
    def __enter__(self):
        # 如果需要记录时间
        if self._log_time is True:
            self._start = default_timer()
        
        # 从连接池获取数据库连接
        conn = pool.get_PoolConn()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        conn.autocommit = False
        
        self._conn = conn
        self._cursor = cursor
        return self
    
    def __exit__(self, *exc_info):
        # 提交事务
        if self._commit:
            self._conn.commit()
        # 在退出的时候自动关闭连接和cursor
        self._cursor.close()
        self._conn.close()
        
        if self._log_time is True:
            diff = default_timer() - self._start
            print('-- %s: %.6f 秒' % (self._log_label, diff))
    @property
    def cursor(self):
        return self._cursor



#测试
def TestMySQL():  
    #申请资源 
    with PoolUtil() as db:
        # SQL 查询语句
        sql = "SELECT * FROM personal"
        try:
            # 获取全部记录列表
            db.cursor.execute(sql)
            results = db.cursor.fetchall()
            for row in results:
                # 打印结果
                print (row)
        except:
            print ("Error: unable to fecth data")



if __name__ == '__main__':
    TestMySQL()





