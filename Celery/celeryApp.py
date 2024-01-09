# -*- coding: utf-8 -*-

# @Time : 2022/3/31 6:49 下午
# @Project : myCelery
# @File : celeryApp.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


from flask import Flask
from celery import Celery, platforms
from urllib.parse import quote

REDIS_IP = '172.21.26.54'
REDIS_DB = 0
#若密码中出现一下特殊的字符，建议用quote进行转义，否则直接赋值会导致后续读取失败
PASSWORD = quote('hutong123456')
#创建Flask的一个实例
flask_app = Flask(__name__)

##配置好celery的backend和broker，只需要在初始化flask的app中加入这行代码，将下面的配置信息写入app的配置文件
# 使用Redis作为消息代理
flask_app.config['CELERY_BROKER_URL'] = 'redis://:{}@{}:6379/{}'.format(PASSWORD, REDIS_IP, REDIS_DB)
# 把任务结果保存在Redis中
flask_app.config['CELERY_RESULT_BACKEND'] = 'redis://:{}@{}:6379/{}'.format(PASSWORD, REDIS_IP, REDIS_DB)
platforms.C_FORCE_ROOT = True  # 解决root用户不能启动celery的问题
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'

# 创建Celery的一个实例
celery_app = Celery(flask_app.name,
					broker=flask_app.config['CELERY_BROKER_URL'],
					backend=flask_app.config['CELERY_RESULT_BACKEND'],
					include=['task', 'task2'])
celery_app.conf.update(flask_app.config)
celery_app.autodiscover_tasks()

if __name__ == '__main__':
	pass
