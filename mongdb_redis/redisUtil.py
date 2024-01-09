# -*- coding: utf-8 -*-

# @Time : 2022/3/21 9:50 下午
# @Project : nosqlUtil
# @File : redisUtil.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


import redis


class RedisClient():
	'''以String数据类型为例的增删改查简单封装'''
	
	def __init__(self, ip, port, db, password):
		self.host = ip
		self.port = port
		self.db = db
		self.password = password
		self.r = redis.Redis(host=self.host, port=self.port, db=self.db, password=self.password)
	
	# 以strings 类型及操作为例
	# 设置 key 对应的值为 string 类型的 value
	def set(self, key, value):
		return self.r.set(key, value)
	
	# 设置 key 对应的值为 string 类型的 value。如果 key 已经存在,返回 0,nx 是 not exist 的意思
	def setnx(self, key, value):
		return self.r.setnx(key, value)
	
	# 设置 key 对应的值为 string 类型的 value,并指定此键值对应的有效期
	def setex(self, key, time, value):
		return self.r.setex(key, time, value)
	
	# 给已有的键设置新值，并返回原有的值。返回字符串，当所给的键不存在时，会设置新值，
	# 但返回值是None
	def getset(self, key, value):
		return self.r.getset(key, value)
	
	# 获取指定 key 的 value 值从start到end的子字符串
	def getrange(self, key, start, end):
		return self.r.getrange(key, start, end)
	
	# 获取指定key的值
	def get(self, key):
		if isinstance(key, list):
			return self.r.mget(key)
		else:
			return self.r.get(key)
	
	# 删除指定的key
	def remove(self, key):
		return self.r.delete(key)


if __name__ == '__main__':
	redisC = RedisClient('172.21.26.54',6379,0,'hutong123456')
	redisC.set('name','TOM')
	print('原来的值 ',redisC.get('name'))
	#给已有的键设置新值，并返回原有的值
	print(redisC.getset('name','TOM2'))
	print('修改后的值 ',redisC.get('name'))
