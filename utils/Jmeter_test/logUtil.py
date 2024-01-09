# -*- coding: utf-8 -*-

# @Time : 2022/4/17 5:21 下午
# @Project : perfTestDemo
# @File : loggerutil.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8

import logging
import os.path
import logging.handlers
from Settings import SettingConf

setting = SettingConf()


# 封装了日志
class Mylogger(object):
	def __init__(self, loggerName=None, fileName='operation.log'):
		"""
		指定保存日志的文件路径，日志级别
		"""

		# 创建一个logger
		self.logger = logging.getLogger(loggerName)
		self.logger.setLevel(logging.DEBUG)

		# 日志名称，带有路径的全路径文件名
		self.log_name = setting.log_prefix + fileName

		# print(os.path.dirname(os.getcwd()))
		# 创建一个handler，用于写入日志文件 (每天生成1个，保留30天的日志)
		# fh = logging.handlers.TimedRotatingFileHandler(self.log_name, 'D', 1, 30)
		# 创建一个handler写入所有日志
		all_fh = logging.FileHandler(self.log_name, mode='a+', encoding='utf-8')
		all_fh.setLevel(logging.INFO)
		# 创建一个handler写入错误日志
		# err_fh = logging.FileHandler(self.error_log_name, mode='a+', encoding='utf-8')
		# err_fh.setLevel(logging.ERROR)

		# 再创建一个handler，用于输出到控制台
		ch = logging.StreamHandler()
		ch.setLevel(logging.INFO)

		# 定义handler的输出格式
		# 以时间-日志器名称-日志级别-日志内容的形式展示
		all_formatter = logging.Formatter(
			'[%(asctime)s] - [%(levelname)s] line:%(lineno)d %(filename)s;%(module)s->%(funcName)s  %(message)s')
		# error日志的记录输出格式
		# err_formatter = logging.Formatter(
		#		'[%(asctime)s] - %(filename)s:%(module)s->%(funcName)s line:%(lineno)d [%(levelname)s] %(message)s')
		all_fh.setFormatter(all_formatter)
		# err_fh.setFormatter(err_formatter)
		# ch.setFormatter(err_formatter)

		# 给logger添加handler
		self.logger.addHandler(all_fh)
		# self.logger.addHandler(err_fh)
		self.logger.addHandler(ch)

		all_fh.close()
		# err_fh.close()
		ch.close()

	def __str__(self):
		return "logger为: %s，日志文件名为: %s" % (
			self.logger,
			self.log_name,
		)

	def getlog(self):
		return self.logger


if __name__ == "__main__":
	Mylogger().getlog().info(
		'1111111'
	)
