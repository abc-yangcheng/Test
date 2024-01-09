# -*- coding: utf-8 -*-

# @Time : 2022/4/17 11:37 上午
# @Project : perfTestDemo
# @File : executeJmeter.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8

import os
import subprocess
import json

from logUtil import Mylogger
from Settings import SettingConf
from parseJmeterLog import parse_jmeterlog

# 获取本脚本名称，传入日志函数
# moduename = os.path.basename(__file__)
# (filename, extension) = os.path.splitext(moduename)
myLogger = Mylogger(__name__).getlog()

# 所有的配置都从setting去获取
setting = SettingConf()

"""
jmeter压测的远程执行、强制停止、结果解析、收尾处理，支持单机

"""


class JMeterClient():
	def __init__(self, jmeterVersion, userName):  # 以userName为名创建文件夹，存放jmx、csv、jar
		self.userName = userName
		# 执行jmeter的路径
		self.jmeter_path = setting.jmeter_path_prefix + 'apache-jmeter-' + jmeterVersion + '/bin/'
		# 存放jmx的路径
		self.jmx_path = self.jmeter_path + userName + '/'
		if not os.path.exists(self.jmeter_path):
			print("jmeter_path:", self.jmeter_path)
			raise RuntimeError('{}路径下不存在jmeter工具包，请先上传'.format(setting.jmeter_path_prefix))
		if not os.path.exists(self.jmx_path):
			# os.makedirs( self.jmxPath)
			mkdir_cmd = 'mkdir -p ' + self.jmx_path
			# 确保目录创建
			subprocess.run(mkdir_cmd, shell=True)
		self.jar_path = setting.jmeter_path_prefix + 'apache-jmeter-' + jmeterVersion + '/lib/ext/'
		self.txt_path = self.jmx_path  # csv 和jmx 脚本存放路径一致

		# 远程连接ssh前缀

		# self.ssh_prefix = ' ssh -p '+ str(setting.ssh_port) + ' '+ setting.ssh_user +'@'
		# self.ssh_prefix = 'sshpass -p apprun ssh -o "StrictHostKeyChecking no" -p ' + str(
		#	setting.ssh_port) + ' ' + setting.ssh_user + '@'
		# self.check_jmeter_cmd = "ps aux| grep ApacheJMeter |grep -v grep |awk '{print $2}'"
		#  ssh apprun@172.28.96.100  "ps aux| grep ApacheJMeter |grep -v grep |awk '{print \$2}' |xargs kill -9"
		# self.kill_jmeter_cmd_remote = " \"ps aux| grep ApacheJMeter |grep -v grep |awk '{print \$2}' |xargs kill -9 \""
		self.kill_jmeter_cmd_local = "ps aux| grep ApacheJMeter |grep -v grep |awk '{print $2}' |xargs kill -9"

		# self.start_slave_cmd = " source /etc/profile; cd " + self.jmx_path + \
		#                     " && nohup ./jmeter-server >/tmp/jmeter_slave.log &"
		# self.start_slave_cmd = " \"source /etc/profile && nohup " + self.jmeter_path + "jmeter-server >/dev/null 2>&1 & \""
		# 当进程kill掉的是，这ssh后台进程也会自动done结束
		# nohup ssh apprun@172.28.96.100 'source /etc/profile && nohup /apprun/apache-jmeter-3.3/bin/jmeter-server >/dev/null 2>&1 & ' &

		# 存储文件名，后续清理时候用
		self.jar_names = []
		self.txt_names = []
		# jtl文件的全路径,临时文件
		self.jtl_file_tmp = setting.jtl_prefix + 'testresult.jtl'
		#
		self.rm_jtl_tmp_cmd = 'rm -rf ' + self.jtl_file_tmp

	# hosts是一个元素为dict的list，是压测机器列表
	def run_jmeter(self, jmxName, csvName=None, jarName=None):

		# 返回错误信息内容，根据不同错误，返回不同的recode和message信息。
		fail_msg = {
			"info": {
				"jmxName": jmxName,
				"username": self.userName
			},
			"recode": '',
			"message": ''
		}

		# 1、确保文件在单机的压测机上
		myLogger.info('--------------------  1、确保脚本存在 ------------------')
		jmx = self.jmx_path + jmxName

		if not os.path.exists(jmx):
			fail_msg['recode'] = '00001'
			fail_msg['message'] = 'jmx file not found'
			fail_msg_json = json.dumps(fail_msg, ensure_ascii=False)
			return fail_msg_json
		myLogger.info('测试脚本{}存在。'.format(jmx))
		if jarName:
			jar = self.jar_path + jarName
			if not os.path.exists(jar):
				fail_msg['recode'] = '00001'
				fail_msg['message'] = 'jar file not found'
				fail_msg_json = json.dumps(fail_msg, ensure_ascii=False)
				return fail_msg_json
		if csvName:
			csv = self.txt_path + csvName
			if not os.path.exists(csv):
				fail_msg['recode'] = '00001'
				fail_msg['message'] = 'csv file not found'
				fail_msg_json = json.dumps(fail_msg, ensure_ascii=False)
				return fail_msg_json

		# 2、启动命令，开始单机压测
		myLogger.info('--------------------  2、启动jmeter命令 -------------------')
		# 本机就是master机器
		# master_host = {"ip": "172.28.20.154", 'port': 22, "username": "root", "passwd": "UWvw30!8"}

		# 先删除老的jtl文件
		if os.path.exists(self.jtl_file_tmp):
			subprocess.run(self.rm_jtl_tmp_cmd, shell=True, check=True)

		# 单机压测，启动命令如下
		start_master_cmd = "source /etc/profile;cd " + self.jmeter_path + \
						   " && ./jmeter  -n  -t " + jmx + "  -l " + self.jtl_file_tmp

		# 在真正开始压测之前，确保jmeter进程不存在，故要先kill
		myLogger.info("开始压测前先确保jmeter进程不存在")
		self.execute_terminate()

		# 真正开始执行压测
		myLogger.info("开始压测，压测命令为：{}".format(start_master_cmd))
		# 如果check参数的值是True，且执行命令的进程以非0状态码退出，则会抛出一个CalledProcessError的异常,故需要改成false
		out = subprocess.run(start_master_cmd, shell=True, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		if out.returncode == 0:  # 返回码为0，表示执行上面命令成功
			jmxResult = out.stdout.decode()
			# print(jmxResult)
			if '... end of run' in jmxResult:
				myLogger.info("{} 脚本执行正常完成，success. \n".format(jmx))
			else:
				myLogger.info("脚本运行未正常结束, error， 结果：{}".format(jmxResult), exc_info=1)

				# 返回对应的错误信息,异常码00002
				fail_msg['recode'] = '00002'
				fail_msg['message'] = 'jmx not ended normally'
				# print('fail_base_msg', fail_base_msg)
				myLogger.info("脚本运行未正常结束的返回：{}".format(fail_msg))
				fail_msg_json = json.dumps(fail_msg, ensure_ascii=False)

				return fail_msg_json
		else:
			# print('命令行执行异常为： ', out)
			myLogger.info("强制中止，subprocess的错误码为: {},错误内容：{}".format(out.returncode, out.stderr), exc_info=1)
			# myLogger.error('执行jmeter错误： ',traceback.print_exc())
			# 返回对应的错误信息（执行异常） 00003
			fail_msg['recode'] = '00003'
			fail_msg['message'] = 'jmx not run  normally'
			myLogger.info("脚本运行错误的返回：{}".format(fail_msg))
			fail_msg_json = json.dumps(fail_msg, ensure_ascii=False)

			return fail_msg_json

		# 3、单机压测结束后，清理工作

		# 1、把testsult.jtl保存为jmxname的名字
		# 2、如有必要，清理jar/txt文件
		myLogger.info('---------------------- 3、清理文件工作 -------------------')

		# 把testresult.jtl结果重新命名为脚本.jtl
		jtl_final_name = setting.jtl_prefix + jmxName[:-4] + ".jtl"
		if os.path.exists(jtl_final_name):
			rm_cmd = "rm -rf " + jtl_final_name
			subprocess.run(rm_cmd, shell=True, check=True)

		mv_cmd = "mv " + self.jtl_file_tmp + " " + jtl_final_name
		subprocess.run(mv_cmd, shell=True, check=True)

		# 4、测试结果处理

		myLogger.info('---------------------- 4、结果解析处理 --------------------')
		# # 取最后一行的summary
		# summary = jmxResult[-3]
		# ##正则表达式[ ]中的任何一个出现至少一次
		## tps = re.split('[ ]+', summary)[6]
		## avg = re.split('[ ]+', summary)[8]

		## error = re.split('[ ]+', summary)[15]
		# print(tps, avg, error)
		# print('*'*40, "分布式压测： 5、结果处理完成",'*'*40)
		# print('jtlname: ',jtl_final_name)
		# 检测文件大小，如果文件小于2g，那么就用如下函数解析，否则就用另一个方法

		result = {}
		try:
			tps, time_avg, err, total_req, minvalue, maxvalue = parse_jmeterlog(
				self.jmeter_path + 'jmeter.log')
		except Exception as e:
			myLogger.info('异常信息为{}'.format(e))
			# 返回对应错误信息（解析jtl失败）00004 
			# 更新字段
			fail_msg['recode'] = '00004'
			fail_msg['message'] = 'parse jmeter log fail'
			fail_msg_json = json.dumps(fail_msg, ensure_ascii=False)

			return fail_msg_json
		else:
			total = {'samples': total_req, 'throughput': tps,
					 'mean': time_avg, 'min': minvalue, 'max': maxvalue, 'error': err,
					 'jmxName': jmxName, 'username': self.userName
					 }
			result['total'] = total
			result['recode'] = '00000'
			result['message'] = 'result parse success'
			result_json = json.dumps(result, ensure_ascii=False)
			myLogger.info('解析结果为：%s \n' % result_json)

		myLogger.info('--------------------  5、结束此次压测 --------------------\n')
		# 返回特定格式 正确的json结果

		if os.path.exists(jtl_final_name):
			rm_cmd = "rm -rf " + jtl_final_name
			subprocess.run(rm_cmd, shell=True, check=True)  # 删除解析完成后的jtl文件

		return result_json

	# 清理工作的时候调用，确保进程已经不在
	def kill_jmeter(self, cmd, ip='local ip'):
		# 杀死master机器进程
		# kill_master_cmd = self.kill_jmeter_cmd_local
		# myLogger.info("执行命令： {}".format(cmd))
		out = subprocess.run(cmd, shell=True, check=False,
							 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		if out.returncode == 0:
			# print('kill slave机器上的进程成功')
			myLogger.info('kill jmeter 进程成功,ip: {}'.format(ip))
		elif out.returncode == 123:
			myLogger.info('jmeter 进程不存在了,不需要kill ,ip: {}'.format(ip))
		# print( ' slave 进程不存在')
		else:
			raise RuntimeError('执行 {} 异常，错误信息：{}'.format(cmd, out.stderr))

	# 强制中止的时候调用
	def execute_terminate(self):

		kill_master_cmd = self.kill_jmeter_cmd_local
		self.kill_jmeter(kill_master_cmd)  # 杀死master进程

		# 删除jtl,jar,csv
		if os.path.exists(self.jtl_file_tmp):
			subprocess.run(self.rm_jtl_tmp_cmd, shell=True)

		return 0  # 强制中止完成


if __name__ == '__main__':
	pass
