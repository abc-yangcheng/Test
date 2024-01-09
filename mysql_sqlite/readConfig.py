# -*- coding: utf-8 -*-

# @Time : 2022/3/13 6:17 下午
# @Project : sqlDemo
# @File : readConfig.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


import configparser

def choiceConfig(dbEnv:str):
	'''
	根据db的环境，选择读取对应的配置信息
	:param dbEnv: db.conf中的数据库的配置名称，Test或Product
	:return: 选择的
	'''

	# 读取数据库配置信息
	config = configparser.ConfigParser()
	config.read('./db.conf', encoding='UTF-8')
	sections = config.sections()
	# 数据库工厂，存储环境的db配置信息
	dbFactory = {}
	if dbEnv in sections:
		# 读取相关属性
		host = config.get(dbEnv, "host")
		port = config.get(dbEnv, "port")
		user = config.get(dbEnv, "user")
		password = config.get(dbEnv, "password")
		database = config.get(dbEnv, "database")
		charset = config.get(dbEnv, "db_charset")
		mincached = config.get(dbEnv, "db_min_cached")
		maxcached = config.get(dbEnv, "db_max_cached")
		maxconnections = config.get(dbEnv, "db_max_connections")
	
		dbFactory[dbEnv] = {'host':host,'port':port,'user':user,'password':password,'database':database,
		                     'charset':charset,'mincached':mincached,'maxcached':maxcached,'maxconns':maxconnections}
		return dbFactory

if __name__ == '__main__':
	print((choiceConfig('Test').get('Test').get('host')))
	
	
