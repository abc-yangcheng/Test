# -*- coding: utf-8 -*-

# @Time : 2022/4/17 10:32 下午
# @Project : perfTestDemo
# @File : main.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


from executeJmeter import JMeterClient

if __name__ == '__main__':
	jmeterVersion = '5.2.1'
	userName = 'hutong'
	jmeterCli = JMeterClient(jmeterVersion,userName)
	jmxName = 'TestPlan.jmx'
	result = jmeterCli.run_jmeter(jmxName)
	print('性能测试结果为：')
	print(result)
