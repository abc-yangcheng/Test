# -*- coding: utf-8 -*-

# @Time : 2022/3/21 6:18 下午
# @Project : nosqlUtil
# @File : mongodbDemos.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


import pymongo

# 账号密码方式连接MongoDB | "mongodb://用户名:密码@公网ip:端口/"
client = pymongo.MongoClient("mongodb://hutong:hutong123456@172.21.26.54:27017/info")
print(client.server_info())

# 指定数据库info
db = client.info

# 指定集合person
collection = db.person

# 插入数据
person = {'name': 'Tom', 'age': 20, 'sex': '男'}
ret = collection.insert_one(person)
print('insert_id:', ret.inserted_id)


# 更新数据
condition = {'name': 'Tom'}
edit = {'age': 21}
ret = collection.update_one(condition, {'$set': edit})
print('update:', ret.matched_count, ret.modified_count)

# 查询
info = collection.find_one(condition)
print('select:', info)

# 计数
count = collection.count_documents({})
print('count:', count)
#
# # 删除数据
# ret = collection.delete_one(condition)
# print('delete:', ret.deleted_count)




if __name__ == '__main__':
	pass
