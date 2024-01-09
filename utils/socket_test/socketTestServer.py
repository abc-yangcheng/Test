# -*- coding: utf-8 -*-

# @Time : 2022/4/13 10:21 上午
# @Project : socketTestDemo
# @File : socketTestServer.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


from threading import Thread
from struct import unpack
import socket
import json

# 只要缓冲区大于1，就存在粘包的可能
BUFFER_SIZE = 8


# 处理每个客户端的连接
def dealClient(conn, addr):
	while True:
		'''
		#接收一个整数，表示接下来要接收的数据长度
		data_length = conn.recv(4)
		if not data_length:
			break
		#解包为整数
		data_length = unpack('i', data_length)[0]
		data = []
		while data_length >0:
			if data_length > BUFFER_SIZE:
				temp = conn.recv(BUFFER_SIZE)
			else:
				#必须要动态调整缓冲区大小，避免粘包
				temp = conn.recv(data_length)
			data.append(temp)
			data_length = data_length - len(temp)
		data = b''.join(data).decode("utf-8") # 以指定的编码格式解码 bytes 对象
		'''
		# 首先获取数据的前面固定的6个字节的消息头
		data_header = conn.recv(6)
		if not data_header:
			break
		# 解包消息头信息，获取真实的消息体长度大小
		data_length = unpack('>HHH', data_header)[2]
		print(f'消息体长度大小为：{data_length}')
		#接收消息体长度大小的字节流数据，获取完整的数据包，避免粘包
		temp = conn.recv(data_length)
		#对消息体进行解包，解包后的返回数据是元组类型
		data_body_bytes = unpack('>%ds' % (int(data_length)), temp)
		#通过json进行解码字节流数据为字符
		data_body = json.loads(data_body_bytes[0].decode('utf-8'))
		print('message from {}： 登录信息为： {}'.format(addr, data_body))
	print('conn {} close'.format(addr))
	conn.close()


if __name__ == '__main__':
	sockServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sockServer.bind(('127.0.0.1', 3000))  # ip地址和端口要求以元组的形式传递，所以这里是两对括号
	sockServer.listen(5)
	while True:
		# conn 是为连接过来的客户端创建的对象,addr则是存放了客户端连接过来的ip和端口
		conn, addr = sockServer.accept()
		# 多线程接收多个客户端的信息
		Thread(target=dealClient, args=(conn, addr)).start()
