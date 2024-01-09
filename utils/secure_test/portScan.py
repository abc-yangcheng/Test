# -*- coding: utf-8 -*-

# @Time : 2022/4/12 4:55 下午
# @Project : scanDemo
# @File : portScan.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


import nmap
import re
import sendEmail
import sys
from multiprocessing import Pool
from functools import partial


# reload(sys)
# sys.setdefaultencoding('utf8')

# 端口扫描，可以通过白名单赦免
def myScan(host, portrange, whitelist):
	p = re.compile("^(\d*)\-(\d*)$")
	# if type(hostlist) != list:
	#    help()
	portmatch = re.match(p, portrange)
	if not portmatch:
		help()

	if host == '121.42.32.172':
		whitelist = [25, ]
	result = ''
	nm = nmap.PortScanner()
	tmp = nm.scan(host, portrange)
	result = result + "<h2>ip地址:%s   ......  %s</h2><hr>" % (
		host, tmp['scan'][host]['status']['state'])
	try:
		ports = tmp['scan'][host]['tcp'].keys()
		for port in ports:
			info = ''
			if port not in whitelist:
				info = '<strong><font color=red>Alert:非预期端口</font><strong>&nbsp;&nbsp;'
			else:
				info = '<strong><font color=green>Info:正常开放端口</font><strong>&nbsp;&nbsp;'
			portinfo = "%s <strong>port</strong> : %s &nbsp;&nbsp;<strong>state</strong> : %s &nbsp;&nbsp;<strong>product<strong/> : %s <br>" % (
				info, port, tmp['scan'][host]['tcp'][port]['state'], tmp['scan'][host]['tcp'][port]['product'])
			result = result + portinfo
	except KeyError as e:
		if whitelist:
			whitestr = ','.join(whitelist)
			result = result + "未扫到开放端口!请检查%s端口对应的服务状态" % whitestr
		else:
			result = result + "扫描结果正常，无暴漏端口"
	return result


def help():
	print("Usage: nmScan(['127.0.0.1',],'0-65535')")
	return None


if __name__ == "__main__":
	# hostlist = ['172.21.26.54', '172.21.26.51']
	hostlist = ['172.21.26.54']
	pool = Pool(5)
	import time

	start = time.time()
	'''多进程
	nmargu = partial(myScan, portrange='0-6550', whitelist=[])
	results = pool.map(nmargu, hostlist)
	'''
	from concurrent.futures.thread import ThreadPoolExecutor
	from concurrent.futures._base import as_completed

	executor = ThreadPoolExecutor(max_workers=3)  # 初始化线程池，指定4线程
	all_task = []
	for host in hostlist:
		task = executor.submit(myScan, host=host, portrange='0-6550', whitelist=[])
		all_task.append(task)
	print("all_task size is " + str(len(all_task)))
	results = ''
	for future in as_completed(all_task):  # 这里会等待线程执行完毕
		result = future.result()
		print(result)
		results = results + result
	print(results)

	print(time.time() - start)
	# 发送邮件
	subject = '服务器端口扫描'
	# 设置自己邮件服务器和账号密码
	smtpserver = 'smtp.163.com'
	user = 'hutong_0306@163.com'
	# 在邮件服务器上设置客户端的授权码
	password = 'hutong0306'
	# 设置接收邮箱和主题
	sender = user
	receiver = ['hutong@cmhi.chinamobile.com']
	mailcontent = '<br>'.join(results)
	# mailcontent = results
	sendEmail.sendemail(sender, receiver, subject, mailcontent, smtpserver, user, password)
