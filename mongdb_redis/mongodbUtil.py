# -*- coding: utf-8 -*-

# @Time : 2022/3/21 4:52 下午
# @Project : nosqlUtil
# @File : mongodbUtil.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


import pymongo


class MongoDB:
	def __init__(self, uri='mongodb://localhost:27017/', db='test', collection='test'):
		"""初始化MongoDB数据库和表的信息并连接数据库

		:param uri: 连接名
		:param db: 数据库名
		:param collection: 表名
		"""
		client = pymongo.MongoClient(uri)
		self.db = client[db]  # 数据库
		self.collection = self.db[collection]  # 表

		if db not in client.list_database_names():
			print("数据库不存在！")
		if collection not in self.db.list_collection_names():
			print("表不存在！")

	def __str__(self):
		"""数据库基本信息"""
		db = self.db._Database__name
		collection = self.collection._Collection__name
		num = self.collection.count_documents({})

		return "数据库{} 表{} 共{}条数据".format(db, collection, num)

	def __len__(self):
		"""表的数据条数"""
		return self.collection.count_documents({})

	def count(self):
		"""表的数据条数"""
		return len(self)

	def insert(self, *args):
		"""插入多条数据

		:param args: 多条数据，可以是dict、dict的list或dict的tuple
		:return: 添加的数据在库中的_id
		"""
		documents = []
		for i in args:
			if isinstance(i, dict):
				documents.append(i)
			# print(documents)
			else:
				documents += [x for x in i]

		return self.collection.insert_many(documents)

	def delete(self, *args, **kwargs):
		"""删除一批数据

		:param args: 字典类型，如{"gender": "male"}
		:param kwargs: 直接指定，如gender="male"
		:return: 已删除条数
		"""
		# TODO(XerCis) 增加正则表达式
		list(map(kwargs.update, args))
		result = self.collection.delete_many(kwargs)
		return result.deleted_count

	def update(self, *args, **kwargs):
		"""更新一批数据

		:param args: dict类型的固定查询条件如{"author":"XerCis"}，循环查询条件一般为_id列表如[{'_id': ObjectId('1')}, {'_id': ObjectId('2')}]
		:param kwargs: 要修改的值，如country="China", age=22
		:return: 修改成功的条数
		"""
		value = {"$set": kwargs}
		query = {}
		n = 0
		list(map(query.update, list(filter(lambda x: isinstance(x, dict), args))))  # 固定查询条件
		for i in args:
			if not isinstance(i, dict):
				for id in i:
					query.update(id)
					result = self.collection.update_one(query, value)
					n += result.modified_count
		result = self.collection.update_many(query, value)
		return n + result.modified_count

	def find(self, *args, **kwargs):
		"""保留原接口"""
		return self.collection.find(*args, **kwargs)

	def find_all(self, show_id=False):
		"""所有查询结果

		:param show_id: 是否显示_id，默认不显示
		:return:所有查询结果
		"""
		if show_id == False:
			return [i for i in self.collection.find({}, {"_id": 0})]
		else:
			return [i for i in self.collection.find({})]

	def find_col(self, *args, **kwargs):
		"""查找某一列数据

		:param key: 某些字段，如"name","age"
		:param value: 某些字段匹配，如gender="male"
		:return:
		"""
		key_dict = {"_id": 0}  # 不显示_id
		key_dict.update({i: 1 for i in args})
		return [i for i in self.collection.find(kwargs, key_dict)]


if __name__ == '__main__':
	"""连接"""
	uri = "mongodb://hutong:hutong123456@172.21.26.54:27017/info"
	db = "info"
	collection = "teacher"
	mongodb = MongoDB(uri, db, collection)  # 连接数据库
	print('当前的数据库信息状态：{}'.format(mongodb))  # 基本信息

	# 插入数据
	person = {'name': 'Tom2', 'age': 22, 'sex': '男'}
	mongodb.insert(person)  # 插入一条数据，dict
	# print(len(mongodb))  # 表的数据条数
	print(mongodb.find_all())  # 所有查询结果
	print('插入后的数据库信息状态：{}'.format(mongodb))  # 基本信息
