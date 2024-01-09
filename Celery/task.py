# -*- coding: utf-8 -*-

# @Time : 2022/3/31 9:58 上午
# @Project : myCelery
# @File : task.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


from celeryApp import celery_app
import time

#这里定义一个后台任务task，异步执行装饰器@celery_app.task
@celery_app.task(bind=True)
def long_task(self):
	total = 100
	for i in range(total):
		# 自定义状态state为waiting..，另外添加meta元数据，模拟任务当前的进度状态
		self.update_state(state='waiting..', meta={'current': i, 'total': total, })
		##使用sleep模拟耗时的业务处理
		time.sleep(1)
	#任务处理完成后，自定义返回结果
	return {'current': 100, 'total': 100, 'result': 'completed'}




if __name__ == '__main__':
	pass
