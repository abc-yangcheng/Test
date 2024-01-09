# -*- coding: utf-8 -*-

# @Time : 2022/4/17 5:21 下午
# @Project : perfTestDemo
# @File : SettingConf.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


class SettingConf():
	def __init__(self):
		# 存放jmeter各个版本压测工具的路径前缀（注意1、更改jmeter、jmeter-server为可执行）
		self.jmeter_path_prefix = '/home/apprun/hutong/'

		# 存放jtl结果的路径前缀
		self.jtl_prefix = '/home/apprun/hutong/'

		# 存放日志的路径前缀
		self.log_prefix = '/home/apprun/hutong/'


if __name__ == '__main__':
	pass
