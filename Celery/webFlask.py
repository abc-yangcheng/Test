# -*- coding: utf-8 -*-

# @Time : 2022/3/31 10:42 上午
# @Project : myCelery
# @File : webFlask.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8

from flask import jsonify, url_for
from celeryApp import flask_app
from task import long_task


# 通过在浏览器中输入ip:port/longtask进行触发异步任务
@flask_app.route('/longtask', methods=['GET'])
def longtask():
	# 发送或触发异步任务，通过apply_async函数调用，生成AsyncResult对象
	task = long_task.apply_async()
	print('task id : {}'.format(task.task_id))
	# task_id和id一样的
	# print('task id : {}'.format(task.id))
	#url_for重定向到taskstatus()函数
	return jsonify({"msg": "success"}), 202, {'Location': url_for('taskstatus',
																  task_id=task.task_id)}


# 通过在浏览器中输入ip:port/status/<task_id>进行异步任务的执行状态查询
@flask_app.route('/status/<task_id>')
def taskstatus(task_id):
	# 获取异步任务的结果
	task = long_task.AsyncResult(task_id)
	print('执行中的 task id ：{}'.format(task))
	# 等待处理
	if task.state == 'PENDING':
		response = {
			'state': task.state,
			'current': 0,
			'total': 100
		}
	# 执行中
	elif task.state != 'FAILURE':
		print('task info : {}'.format(task.info))
		# task.info 和 task.result是一样的
		# print('task info : {}'.format(task.result))
		response = {
			'state': task.state,
			'current': task.info.get('current', 0),
			'total': task.info.get('total', 100)
		}
		# 因为task中定义了执行成功后返回的结果中包含result字符
		if 'result' in task.info:
			response['result'] = task.info['result']
	else:
		# 后台任务出错
		response = {
			'state': task.state,
			'current': task.info.get('current', 0),
			'total': 100
		}
	return jsonify(response)


if __name__ == '__main__':
	# 运行flask
	flask_app.run()
