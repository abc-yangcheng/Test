# -*- coding: utf-8 -*-

# @Time : 2022/4/13 9:36 上午
# @Project : socketTestDemo
# @File : socketTestClient.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


import socket
from threading import Thread


# 客户端代码，模拟建立socket连接，发送自定义的消息格式
def socketClient(ip, port, id):
	sockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sockClient.connect((ip, int(port)))
	except  Exception as e:
		print("except:", e)
		print('连接服务器失败')
	else:
		# 登录的消息体
		login_msg = {
			'msgTpye': 'login',
			'user': 'hutong0',
			'password': 'qazwsx'
		}

		login_msg['user'] = 'hutong' + str(id)
		import pickle, json
		# 通过pickle进行编码，通常编码后的数据会加入一些额外的字节信息，所以与json编码出的长度不一样。
		# login_bytes = pickle.dumps(login_msg)
		login_json = json.dumps(login_msg)
		print(f'\n客户端 {sockClient} \n发送的登录信息为 {login_json}')
		# print(login_json.encode('utf-8'), len(login_json.encode('utf-8')))
		# print(type(login_bytes), len(login_bytes), login_bytes)
		from packetUtil import load_packet
		# 根据自定义的消息头和消息体，封装待发送的消息内容
		packet = load_packet(0xFFFF, 0x0001, len(login_json.encode('utf-8')), login_json.encode('utf-8'))

		# 发送自定义格式的封装后的包数据
		sockClient.sendall(packet)

		sockClient.close()


if __name__ == '__main__':
	# 多线程方式创建多个socket客户端进行发送登录请求
	for i in range(3):
		Thread(target=socketClient, args=('127.0.0.1', 3000,i)).start()
