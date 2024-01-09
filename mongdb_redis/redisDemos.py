# -*- coding: utf-8 -*-

# @Time : 2022/3/21 9:50 下午
# @Project : nosqlUtil
# @File : redisDemos.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


import redis

pool = redis.ConnectionPool(host='172.21.26.54', port=6379,password= 'hutong123456', decode_responses=True)
r = redis.Redis(connection_pool=pool)
r.set('name', 'hutong', ex=3)
r.append("name", " nihao")    # 在name对应的值后面追加字符串nihao
print(r.get('name'))



if __name__ == '__main__':
	pass
