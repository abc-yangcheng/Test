# -*- coding: utf-8 -*-

# @Project : apiTest
# @File    : mylog.py
# @Date    : 2019-11-29
# @Author  : hutong
# @Describe: 微信公众： 大话性能



import logging
import os.path
import time
import logging.handlers
import subprocess
from config.configAll import Config

'''
all_log_path = os.path.join(setting.log_prefix, 'all_logs/')
# all_log_path =  '/home/logs/all_logs/'
error_log_path = os.path.join(setting.log_prefix, 'err_logs/')
# error_log_path = '/home/logs/err_logs/'
# 先确保新建存放log的目录
if not os.path.exists(all_log_path):
	subprocess.run("mkdir -p " + all_log_path, shell =True)
if not os.path.exists(error_log_path):
	subprocess.run("mkdir -p " + error_log_path, shell = True)
print("all_log_path: ",all_log_path)
print("error_log_path: ",error_log_path)
'''


class Log(object):
    def __init__(self, loggerName=None, fileName='test.log'):
        if not os.path.exists(Config.log_path):
            subprocess.run("mkdir -p  {}".format(Config.log_path) , shell=True)

        """
        指定保存日志的文件路径，日志级别
        """

        # 创建一个logger
        self.logger = logging.getLogger(loggerName)
        self.logger.setLevel(logging.DEBUG)

        # 创建日志名称,all_logs记录所有的日志，err_logs只记录错误日志
        timenow = time.strftime('%Y%m%d', time.localtime(time.time()))
        # os.getcwd()获取当前文件的路径，os.path.dirname()获取指定文件路径的上级路径

        # print('日志路径为：', all_log_path)

        # self.all_log_name = all_log_path + timenow + '_' + fileName + '_all.log'
        # self.error_log_name = error_log_path + timenow + '_' + fileName + '_err.log'
        self.log_name = Config.log_path + fileName

        # print(os.path.dirname(os.getcwd()))
        # 创建一个handler，用于写入日志文件 (每天生成1个，保留30天的日志)
        # fh = logging.handlers.TimedRotatingFileHandler(self.log_name, 'D', 1, 30)
        # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
        #file_log_handler = logging.handlers.RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
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
            '[%(asctime)s] [%(levelname)s] line:%(lineno)d %(filename)s  %(message)s')
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

    def getlogger(self):
        return self.logger



if __name__ == "__main__":
    pass
