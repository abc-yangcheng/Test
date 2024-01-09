# -*- coding: utf-8 -*-

# @Time : 2022/3/13 1:24 下午
# @Project : sqlDemo
# @File : pymysqlUtil.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8

import logging

import pymysql
from timeit import default_timer
from readConfig import choiceConfig


# 用pymysql操作mysql数据库
def get_connection(dbEnv):
    '''
    利用pymysql建立特定环境的数据库连接
    :param dbEnv: 哪个环境的mysql数据库配置
    :return: 返回建立的单个连接
    '''
    conn = pymysql.connect(host=choiceConfig(dbEnv).get(dbEnv).get('host'),
                           port=int(choiceConfig(dbEnv).get(dbEnv).get('port')),
                           db=choiceConfig(dbEnv).get(dbEnv).get('database'),
                           user=choiceConfig(dbEnv).get(dbEnv).get('user'),
                           password=choiceConfig(dbEnv).get(dbEnv).get('password'))
    return conn


# 使用 with 的方式来优化连接的关闭
class UsingMysql(object):

    def __init__(self, commit=True, log_time=True, log_label='总共用时'):
        """

        :param commit: 是否在最后提交事务(设置为False的时候方便单元测试)
        :param log_time:  是否打印程序运行总时间
        :param log_label:  自定义log的文字
        """
        self._log_time = log_time
        self._commit = commit
        self._log_label = log_label

    def __enter__(self):

        # 如果需要记录时间
        if self._log_time is True:
            self._start = default_timer()

        # 在进入的时候自动获取连接和cursor
        conn = get_connection('Test')
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


#查询
def get_it():
    with UsingMysql(log_time=True) as db:
        db.cursor.execute("select count(id) as total from personal")
        data = db.cursor.fetchone()
        print("-- 当前数量: %d " % data['total'])
        
#增加
def add_it():
    with UsingMysql(log_time=True) as db:
        sql = "insert into personal(id,name,age,address) values(%(id)s,%(name)s,%(age)s,%(address)s)"
        data = {'id':4,'name':'hutong','age':33,'address':'ddd'}
        #db.cursor.execute("insert into personal values(3,'tt',18,'zhejiang')")
        result = db.cursor.execute(sql,data)
        if result == 1:
            print('insert success')
        
#删除
def del_it():
    with UsingMysql(log_time=True) as db:
        sql = "delete from  personal where id = %(id)s"
        data = {'id':4}
        print(db.cursor.execute(sql,data))


#更新
def update_it():
    with UsingMysql(log_time=True) as db:
        sql = "update  personal set name = %(name)s where id = %(id)s"
        data = {'id':3,'name':'hutong3'}
        db.cursor.execute(sql,data)
    

class MySQLConnection(object):
    """
    数据库连接池代理对象
    查询参数主要有两种类型
    第一种：传入元祖类型,例如(12,13),这种方式主要是替代SQL语句中的%s展位符号
    第二种: 传入字典类型,例如{"id":13},此时我们的SQL语句需要使用键来代替展位符,例如：%(name)s
    """
    def __init__(self,dbName="master"):
        dbFactory={}
        self.connect = dbFactory[dbName].connection()
        self.cursor = self.connect.cursor()
        logging.debug("获取数据库连接对象成功,连接池对象:{}".format(str(self.connect)))

    def execute(self,sql,param=None):
        """
        基础更新、插入、删除操作
        :param sql:
        :param param:
        :return: 受影响的行数
        """
        ret=None
        try:
            if param==None:
                ret=self.cursor.execute(sql)
            else:
                ret=self.cursor.execute(sql,param)
        except TypeError as te:
            logging.debug("类型错误")
            logging.exception(te)
        return ret
    def query(self,sql,param=None):
        """
        查询数据库
        :param sql: 查询SQL语句
        :param param: 参数
        :return: 返回集合
        """
        self.cursor.execute(sql,param)
        result=self.cursor.fetchall()
        return result
    def queryOne(self,sql,param=None):
        """
        查询数据返回第一条
        :param sql: 查询SQL语句
        :param param: 参数
        :return: 返回第一条数据的字典
        """
        result=self.query(sql,param)
        if result:
            return result[0]
        else:
            return None
    def listByPage(self,sql,current_page,page_size,param=None):
        """
        分页查询当前表格数据
        :param sql: 查询SQL语句
        :param current_page: 当前页码
        :param page_size: 页码大小
        :param param:参数
        :return:
        """
        countSQL="select count(*) ct from ("+sql+") tmp "
        logging.debug("统计SQL:{}".format(sql))
        countNum=self.count(countSQL,param)
        offset=(current_page-1)*page_size
        totalPage=int(countNum/page_size)
        if countNum % page_size>0:
            totalPage = totalPage + 1
        pagination={"current_page":current_page,"page_size":page_size,"count":countNum,"total_page":totalPage}
        querySql="select * from ("+sql+") tmp limit %s,%s"
        logging.debug("查询SQL:{}".format(querySql))
        # 判断是否有参数
        if param==None:
            # 无参数
            pagination["data"]=self.query(querySql,(offset,page_size))
        else:
            # 有参数的情况,此时需要判断参数是元祖还是字典
            if isinstance(param,dict):
                # 字典的情况,因此需要添加字典
                querySql="select * from ("+sql+") tmp limit %(tmp_offset)s,%(tmp_pageSize)s"
                param["tmp_offset"]=offset
                param["tmp_pageSize"]=page_size
                pagination["data"]=self.query(querySql,param)
            elif isinstance(param,tuple):
                # 元祖的方式
                listtp=list(param)
                listtp.append(offset)
                listtp.append(page_size)
                pagination["data"]=self.query(querySql,tuple(listtp))
            else:
                # 基础类型
                listtp=[]
                listtp.append(param)
                listtp.append(offset)
                listtp.append(page_size)
                pagination["data"]=self.query(querySql,tuple(listtp))
        return pagination
    def count(self,sql,param=None):
        """
        统计当前表记录行数
        :param sql: 统计SQL语句
        :param param: 参数
        :return: 当前记录行
        """
        ret=self.queryOne(sql,param)
        count=None
        if ret:
            for k,v in ret.items():
                count=v
        return count

    def insert(self,sql,param=None):
        """
        数据库插入
        :param sql: SQL语句
        :param param: 参数
        :return: 受影响的行数
        """
        return self.execute(sql,param)
    def update(self,sql,param=None):
        """
        更新操作
        :param sql: SQL语句
        :param param: 参数
        :return: 受影响的行数
        """
        return self.execute(sql,param)
    def delete(self,sql,param=None):
        """
        删除操作
        :param sql: 删除SQL语句
        :param param: 参数
        :return: 受影响的行数
        """
        return self.execute(sql,param)
    def batch(self,sql,param=None):
        """
        批量插入
        :param sql: 插入SQL语句
        :param param: 参数
        :return: 受影响的行数
        """
        return self.cursor.executemany(sql,param)
    def commit(self,param=None):
        """
        提交数据库
        :param param:
        :return:
        """
        if param==None:
            self.connect.commit()
        else:
            self.connect.rollback()

    def close(self):
        """
        关闭数据库连接
        :return:
        """
        if self.cursor:
            self.cursor.close()
        if self.connect:
            self.connect.close()
        logging.debug("释放数据库连接")
        return None

if __name__ == '__main__':
    get_it()
    del_it()
    add_it()
    get_it()
    update_it()
    
