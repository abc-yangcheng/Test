# -*- coding: utf-8 -*-

# @Time : 2022/4/20 5:49 下午
# @Project : socketTestDemo
# @File : packetUtil.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


import struct
import ctypes

#封包
#封装自定义的消息格式，消息头包含2字节的开始标志、2字节的消息类型，2字节的消息体长度，若干字节的消息体
def load_packet(msg_startSign, msg_type, msg_lenOfBody, msg_payLoad):
	#创建一个string缓存, 大小为10
	packet = ctypes.create_string_buffer(msg_lenOfBody+6)
	#第一个参数 "9s i f" 表示格式化字符串(format), 里面的符号则代表数据的类型,第二个参数表示缓冲区, 第三个参数表示偏移量, 0表示从头开始; 然后后面的参数就是打包的数据
	struct.pack_into('>HHH', packet, 0, msg_startSign, msg_type,msg_lenOfBody)
	struct.pack_into('>%ds' % (int(msg_lenOfBody)), packet, 6, msg_payLoad)
	return packet

#解包
def unload_packet(packet):
	msg_startSign, msg_type, msg_lenOfBody = struct.unpack_from('>HHH', packet, 0)
	msg_payload = struct.unpack_from('>%ds' % (int(msg_lenOfBody)), packet, 6)
	return msg_startSign, msg_type, msg_payload

if __name__ == '__main__':
	login_msg = {
	'msgTpye':'login',
	'user': 'hutong',
	'password': 'qazwsx'
	}
	ping_msg = {
	'msgTpye':'ping',
	'msg': 'ping'
	}
	#测试用json编解码和pickle编解码的区别
	import json
	import pickle
	login_json =json.dumps(login_msg)
	print(login_json,len(login_json))
	print(login_json.encode('utf-8'),len(login_json.encode('utf-8')))
	login_bytes = pickle.dumps(login_msg)
	login_bytes1 = pickle.dumps(login_msg,protocol=1)
	login_bytes2 = pickle.dumps(login_msg,protocol=2)
	print(login_bytes1)
	print(login_bytes2)
	print(type(login_bytes), len(login_bytes), login_bytes)
	# 还可以将打包后的结果转成十六进制, 这样传输起来更加方便
	import binascii
	print(binascii.hexlify(login_bytes))


