# -*- coding: utf-8 -*-

# @Time : 2022/4/17 10:32 下午
# @Project : perfTestDemo
# @File : parseJmeterLog.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8

import subprocess


def parse_jmeterlog(jmeterlog_name):
	out = subprocess.run('tail -n 1 ' + jmeterlog_name, shell=True, check=False, stdout=subprocess.PIPE,
						 stderr=subprocess.PIPE)

	if out.returncode == 0:  # 返回码为0，表示执行上面命令成功
		jmxResult = out.stdout.decode()

		# print(jmxResult)
		if 'summary =' in jmxResult:
			# print("-------解析结果为----")
			# print(jmxResult.split())
			result_list = jmxResult.split()
			# print('从jmeter.log解析出的结果为：{}'.format(result_list))
			total_requests = int(result_list[6])
			tps = result_list[10][:-2]
			avg_time = result_list[12]
			min_time = result_list[14]
			max_time = result_list[16]
			err = int(result_list[18])

			# print(tps, avg_time, float('{:.4f}'.format((err / total_requests))), total_requests, min_time, max_time)
			return tps, avg_time, float('{:.4f}'.format((err / total_requests))), total_requests, min_time, max_time
		else:
			print(jmxResult)
			# 返回值为tps，平均响应时间，错误率，总请求数，最小响应时间，最大响应时间
			return 0, 0, 1, 0, 0, 0
	else:
		print('返回码，', out.returncode, '错误内容：', out.stderr)
		return 0, 0, 1, 0, 0, 0


if __name__ == "__main__":
	pass
