# -*- coding: utf-8 -*-

# @Time : 2022/3/31 6:51 下午
# @Project : myCelery
# @File : task2.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8

from celeryApp import celery_app


@celery_app.task(bind=True)
def short_task():
	return  'this is second task !'

if __name__ == '__main__':
	pass
