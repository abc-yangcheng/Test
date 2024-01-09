# -*- coding: utf-8 -*-

# @Time : 2022/3/15 10:41 上午
# @Project : msgUtil
# @File : producerKafka.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8

# from kafka import KafkaProducer

# producer = KafkaProducer(bootstrap_servers=['172.21.26.54:9092'])
# future = producer.send('my_topic',
#                        key=b'my_key',
#                        value=b'my_value',
#                        partition=0)
# result = future.get(timeout=10)
# print(result)

import time
import random
import sys

from kafka import KafkaProducer
from kafka.errors import KafkaError, KafkaTimeoutError
import json

'''生产者，
一个生产者其实是2个线程，后台有一个IO线程用于真正发送消息出去，前台有一个线程用于把消息发送到本地缓冲区'''


class Producer(object):
	def __init__(self, KafkaServerList=['127.0.0.1:9092'], ClientId="Producer01", Topic='TestTopc'):
		self._kwargs = {
			"bootstrap_servers": KafkaServerList,
			"client_id": ClientId,
			"acks": 1,
			"buffer_memory": 33554432,
			'compression_type': None,
			"retries": 3,
			"batch_size": 1048576,
			"linger_ms": 100,
			"key_serializer": lambda m: json.dumps(m).encode('utf-8'),
			"value_serializer": lambda m: json.dumps(m).encode('utf-8'),
		}
		self._topic = Topic
		try:
			self._producer = KafkaProducer(**self._kwargs)
		except Exception as err:
			print(err)

	def _onSendSucess(self, record_metadata):
		"""
		异步发送成功的回调函数，也就是真正发送到kafka集群且成功才会执行。发送到缓冲区不会执行回调方法。
		:param record_metadata:
		:return:
		"""
		print("发送成功")
		print("被发往的主题：", record_metadata.topic)
		print("被发往的分区：", record_metadata.partition)
		print("队列位置：", record_metadata.offset)  # 这个偏移量是相对偏移量，也就是相对起止位置，也就是队列偏移量。

	def _onSendFailed(self):
		print("发送失败")

	# 异步发送数据
	def sendMessage_asyn(self, value=None, partition=None):
		if not value:
			return None

		# 发送的消息必须是序列化后的，或者是字节
		# message = json.dumps(msg, encoding='utf-8', ensure_ascii=False)

		kwargs = {
			"value": value,  # value 必须必须为字节或者被序列化为字节，由于之前我们初始化时已经通过value_serializer来做了，所以我上面的语句就注释了
			"key": None,  # 与value对应的键，可选，也就是把一个键关联到这个消息上，KEY相同就会把消息发送到同一分区上，所以如果有这个要求就可以设置KEY，也需要序列化
			"partition": partition  # 发送到哪个分区，整型。如果不指定将会自动分配。
		}

		try:
			# 异步发送，发送到缓冲区，同时注册两个回调函数，一个是发送成功的回调，一个是发送失败的回调。
			# send函数是有返回值的是RecordMetadata，也就是记录的元数据，包括主题、分区、偏移量
			future = self._producer.send(self._topic, **kwargs).add_callback(self._onSendSucess).add_errback(
				self._onSendFailed)
			print("发送消息:", value)

		# 注册回调也可以这样写，上面的写法就是为了简化
		# future.add_callback(self._onSendSucess)
		# future.add_errback(self._onSendFailed)
		except KafkaTimeoutError as err:
			print(err)
		except Exception as err:
			print(err)

	def closeConnection(self, timeout=None):
		# 关闭生产者，可以指定超时时间，也就是等待关闭成功最多等待多久。
		self._producer.close(timeout=timeout)

	def sendNow(self, timeout=None):
		# 调用flush()函数可以放所有在缓冲区的消息记录立即发送，即使ligner_ms值大于0.
		# 这时候后台发送消息线程就会开始立即发送消息并且阻塞在这里，等待消息发送成功，当然是否阻塞取决于acks的值。
		# 如果不调用flush函数，那么什么时候发送消息取决于ligner_ms或者batch任意一个条件满足就会发送。
		try:
			self._producer.flush(timeout=timeout)
		except KafkaTimeoutError as err:
			print(err)
		except Exception as err:
			print(err)

	# 同步发送数据
	def sendMessage_sync_(self, data):
		"""
		同步发送 数据
		:param topic:  topic
		:param data_li:  发送数据
		:return:
		"""
		future = self._producer.send(self._topic, data)
		record_metadata = future.get(timeout=10)  # 同步确认消费
		partition = record_metadata.partition  # 数据所在的分区
		offset = record_metadata.offset  # 数据所在分区的位置
		print("save success, partition: {}, offset: {}".format(partition, offset))


def main():
	p = Producer(KafkaServerList=["172.21.26.54:9092"], ClientId="Producer01", Topic="TestTopic")
	for i in range(10):
		time.sleep(1)
		closePrice = random.randint(1, 500)
		msg = {
			"Publisher": "Procucer01",
			"股票代码": 60000 + i,
			"昨日收盘价": closePrice
		}
		# p.sendMessage_asyn(value=msg,partition=0)
		p.sendMessage_sync_(msg)
	# p.sendNow()
	p.closeConnection()


if __name__ == "__main__":
	try:
		main()
	finally:
		sys.exit()
