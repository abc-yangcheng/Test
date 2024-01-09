# -*- coding: utf-8 -*-

# @Time : 2022/4/14 7:20 下午
# @Project : dataTestDemo
# @File : parseJTL.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


# encoding: utf-8

"""
@python: v3.5.4
@author: hutong
@file: parseJTL.py
@time: 2019/04/23 上午11:08
"""

import pandas as pd
import time, datetime
import json

"""
jtl文件的格式：
timeStamp,elapsed,label,responseCode,responseMessage,threadName,dataType,success,failureMessage,bytes,sentBytes,
grpThreads,allThreads,Latency,IdleTime,Connect
"""


# 解析jtl文件，并返回json格式
class HandleJtl():
	# 计算timesatmp时差
	@staticmethod
	def div(df):
		return (df.max() - df.min()) / 1000

	# 计算95%的时间位
	@staticmethod
	def quantile95(df):
		return df.quantile(0.95)

	@staticmethod
	def parseJtl(fileName, jmxId, projectId, taskId, jmxRound, threads, durations, jmxName, projectName, hosts,
				 userName, createTime):
		# if len(sys.argv) != 2:
		#  print('Usage:', sys.argv[0], 'file_of_csv')
		#  exit()
		# else:
		#  csv_file = sys.argv[1]
		csv_file = fileName
		####### 生成数据 #####

		# 需统计字段对应的日志位置
		'''
		timestamp = 0
		label = 2
		responsecode = 3
		threadname = 5
		status = 7
		bytes = 9
		latency = 13
		'''
		start = time.time()
		# 将csv读入DataFrame，usecols根据名字来判断，而不能是位置，因为jmeter版本不同，jtl有不一样
		try:
			reader = pd.read_csv(csv_file, sep=',', header=0,
								 usecols=['timeStamp', 'label', 'success', 'bytes', 'Latency'],
								 iterator=True, low_memory=False,
								 encoding='utf-8', dtype={'success': object}, skip_blank_lines=True,
								 on_bad_lines='skip'
								 )
		# error_bad_lines=False 跳过报错的行
		except Exception as e:
			raise RuntimeError('the exception is: ', e)

		loop = True
		chunkSize = 1000000
		chunks = []
		while loop:
			try:
				chunk = reader.get_chunk(chunkSize)
				chunks.append(chunk)
			except StopIteration:
				# Iteration is stopped.
				# testlogger.error("拼接jtl文件异常" , exc_info=1)
				loop = False
		df = pd.concat(chunks, ignore_index=True)
		df = df.dropna(axis=0, how='any')
		# print(df.head(20))

		# 新增判断，如果jtl文件，只有一行头数据
		# print(df)
		if df.empty:
			nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			err_result = {}
			total = {'startTime': nowTime, 'samples': 0, 'label': 'total', 'throughput': 0, 'th95': 0,
					 'mean': 0, 'min': 0, 'max': 0, 'error': 1, 'kb': 0, 'id': taskId, 'isDelete': 0,
					 'hosts': hosts, 'round': jmxRound, 'jmxId': jmxId, 'jmxName': jmxName, 'projectId': projectId,
					 'duration': durations,
					 'projectName': projectName, 'username': userName, 'createTime': createTime, 'endTime': nowTime,
					 'threads': threads}

			total['message'] = 'parse failure'
			err_result['total'] = total

			err_result['recode'] = 500
			err_result['message'] = 'parse failure'
			# print(err_result)
			print(err_result)
			# print(type(result))

			err_json = json.dumps(err_result, ensure_ascii=False)
			return err_json

		##########  总请求结果处理 ########

		# 最小时间(开始时间)
		start_time = int(df['timeStamp'].min())
		# print((df['timeStamp'].min()))
		# print(type(start_time))

		# 转换成新的时间格式(2016-05-05 20:28:54)
		starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time / 1000))
		# 最大时间(结束时间)
		end_time = int(df['timeStamp'].max())
		endtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time / 1000))

		# 总消耗的时间（s）
		time_total = (end_time - start_time) / 1000

		# 响应时间最小值
		time_min = round(float(df['Latency'].min()), 2)
		# 响应时间最大值
		time_max = round(float(df['Latency'].max()), 2)
		# 95%的响应时间
		time_95 = round(float(df['Latency'].quantile(0.95)), 2)
		# 平均的响应时间
		time_avg = round(float(df['Latency'].mean()), 2)
		kb = round(float(df['bytes'].mean()), 2)

		# 请求成功率
		total_req = int(len(df.index))  # 总请求数
		# print(df['success'].head())
		request_result = dict(df['success'].value_counts())  # 统计值
		# print(request_result, type(request_result))
		# 优化，新增了异常判断，jtl全是false到时候，true不存在
		if 'true' in request_result.keys():
			success_req = request_result['true']
			success_rate = success_req / total_req
			error_rate = format(1 - success_rate, '.2f')
		else:
			error_rate = 1.00
		# tps
		tps = round(total_req / time_total, 2)

		########## 计算具体请求的结果   ##########
		group_request = df.groupby('label')
		# print(group_request.head())
		# print(type(group_request))
		# 计算每个请求的成功失败个数
		status_detail = pd.DataFrame(group_request['success'].value_counts())
		df2 = status_detail.unstack(fill_value=0)
		# print(df2)
		# print(type(df2))

		# 不同的列应用不同的计算，返回datafram
		start_time_detail = group_request.agg(
			{'timeStamp': [HandleJtl.div, 'min'], 'success': 'count', 'bytes': 'mean',
			 'Latency': ['mean', 'min', 'max', HandleJtl.quantile95]})
		# print(start_time_detail)
		# print(type(start_time_detail))

		# print(start_time_detail.index)
		# print(type(start_time_detail['success']))
		# print(start_time_detail['success']/start_time_detail['timeStamp'])
		start_time_detail['tps'] = start_time_detail['success']['count'] / start_time_detail['timeStamp']['div']
		# print(df2['success'],type(df2['success']),df2['success'].columns, df2['success'].index)
		# 优化，新增了异常判断，jtl全是false到时候，true不存在
		if 'true' in df2['success'].columns:
			# print('llll')
			start_time_detail['success_req'] = df2['success']['true']
		else:
			start_time_detail['success_req'] = 0
		# print(start_time_detail)
		# print(start_time_detail.index)
		# print(start_time_detail.columns)
		# print(type(start_time_detail))

		###### 结果打印  ######
		'''
		print('*' * 30, '---总的请求性能结果---', '*' * 30)

		# print(status_total.sum()[0])
		print('开始测试时间： ', starttime)
		print('成功率：%.3f ' % success_rate)
		print('总tps: %f /s ' % tps)
		print('平均响应时间：' + '%.2fms' % time_avg)
		print('95%响应时间：' + '%.2fms' % time_95)
		print('kb为：' + '%.2f' % kb)
		print('总测试时长：%.3fs ' % time_total)
		print('解析%d行jtl数据，消耗时间：%.3fs' % (len(df.index), (time.time() - start)))

		print('*' * 30, '----具体每个请求的性能结果----', '*' * 30)
		'''
		# 存储结果
		result = {}
		num = 0
		for index, row in start_time_detail.iterrows():
			detail_starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(row["timeStamp"]['min'] / 1000))
			detail_time_avg = round(float(row["Latency"]['mean']), 2)
			detail_time_min = round(float(row["Latency"]['min']), 2)
			detail_time_max = round(float(row["Latency"]['max']), 2)
			detail_time_th95 = round(float(row["Latency"]['quantile95']), 2)
			detail_kb = round(float(row["bytes"]['mean']), 2)
			detail_total = round(float(row["success"]['count']), 2)  # 请求数目
			detail_success = round(float(row["success_req"]['']), 2)  # 成功请求数目
			detail_error_rate = round(1 - detail_success / detail_total, 2)
			detail_tps = round(float(row['tps']['']), 2)
			detail_label = index
			'''
			print("请求： ", detail_label, "  开始测试时间为: ", detail_starttime,
			      "  平均响应时间为(ms): ", detail_time_avg,
			      "  95%响应时间为(ms): ", detail_time_th95,
			      "  最小响应时间为(ms): ", detail_time_min,
			      "  最大响应时间为(ms): ", detail_time_max,
			      "  bytes为(kb): ", detail_kb,
			      "  error率: ", detail_error_rate,
			      "  tps(/s): ", detail_tps)
			'''
			num = num + 1
			detailname = 'detail' + str(num)

			result[detailname] = {'startTime': detail_starttime, 'samples': detail_total, 'label': detail_label,
								  'throughput': detail_tps, 'th95': detail_time_th95, 'kb': detail_kb,
								  'mean': detail_time_avg, 'min': detail_time_min, 'max': detail_time_max,
								  'error': detail_error_rate, 'jmxId': jmxId,
								  'totalId': taskId, 'creatTime': createTime}

		# 结果封装成json

		total = {'startTime': starttime, 'samples': total_req, 'label': 'total', 'throughput': tps, 'th95': time_95,
				 'mean': time_avg, 'min': time_min, 'max': time_max, 'error': error_rate, 'kb': kb, 'id': taskId,
				 'isDelete': 0,
				 'hosts': hosts, 'round': jmxRound, 'jmxId': jmxId, 'jmxName': jmxName, 'projectId': projectId,
				 'duration': durations,
				 'projectName': projectName, 'username': userName, 'createTime': createTime, 'endTime': endtime,
				 'threads': threads}
		total['message'] = 'parse success'
		result['total'] = total
		result['recode'] = 200
		result['message'] = 'parse success'
		# print(result)
		# print(type(result))

		total_json = json.dumps(result, ensure_ascii=False)
		time_take = time.time() - start
		# print('*' * 30, '----组装为json的结果为----', '*' * 30)
		# print(total_json)
		print('成功，解析jtl成功，{}行，耗时{}秒，json结果为：\n {}'.format(len(df), round(time_take, 2), total_json))
		# testlogger.info('成功，解析jtl成功，%s行，耗时%s秒，json结果为：\n %s' % (len(df), round(time_take, 2), total_json))
		print('------------ 7、正常结束此次压测 -----------')
		return total_json


if __name__ == "__main__":
	hosts = [{'ip': '172.28.20.154', 'port': 400, }]
	result = HandleJtl.parseJtl('/Users/personal/python工程/result.jtl', 'jmxid', 'projectid', 'taskid', 11, 12, 13,
								'jmxname', 'projectname',
								hosts, 'admin', '2019-05-15 17:46:02')

	print(result)
