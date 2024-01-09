# -*- coding: utf-8 -*-

# @Time : 2022/3/15 10:48 上午
# @Project : msgUtil
# @File : consumerKafka.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8

# from kafka import KafkaConsumer
#
# consumer = KafkaConsumer('my_topic',
#                          group_id='group2',
#                          bootstrap_servers=['172.21.26.54:9092'])
# for msg in consumer:
# 	print(msg)


import sys
import traceback

from kafka import KafkaConsumer, TopicPartition
import json

'''单线程消费者'''


class Consumer(object):
	def __init__(self, KafkaServerList=['172.21.26.54:9092'], GroupID='TestGroup', ClientId="Test",
				 Topics=['TestTopic', ]):
		"""
		用于设置消费者配置信息，这些配置项可以从源码中找到，下面为必要参数。
		:param KafkaServerList: kafka服务器IP:PORT 列表
		:param GroupID: 消费者组ID
		:param ClientId: 消费者名称
		:param Topic: 主题
		"""

		"""
		初始化一个消费者实例，消费者不是线程安全的，所以建议一个线程实现一个消费者，而不是一个消费者让多个线程共享
		下面这些是可选参数，可以在初始化KafkaConsumer实例的时候传递进去
		enable_auto_commit 是否自动提交，默认是true
		auto_commit_interval_ms 自动提交间隔毫秒数
		auto_offset_reset="earliest"  重置偏移量，earliest移到最早的可用消息，latest最新的消息，默认为latest
		"""
		self._kwargs = {
			"bootstrap_servers": KafkaServerList,
			"client_id": ClientId,
			"group_id": GroupID,
			"enable_auto_commit": False,
			"auto_offset_reset": "latest",
			"key_deserializer": lambda m: json.loads(m.decode('utf-8')),
			"value_deserializer": lambda m: json.loads(m.decode('utf-8')),
		}

		try:
			self._consumer = KafkaConsumer(**self._kwargs)
			self._consumer.subscribe(topics=(Topics))

		except Exception as err:
			print("Consumer init failed, %s" % err)

	def consumeMsg(self):
		try:
			while True:
				# 手动方式拉取消息
				data = self._consumer.poll(timeout_ms=5, max_records=100)  # 拉取消息，字典类型
				if data:
					for key in data:
						consumerrecord = data.get(key)[0]  # 返回的是ConsumerRecord对象，可以通过字典的形式获取内容。
						if consumerrecord != None:
							# 消息消费逻辑
							message = {
								"Topic": consumerrecord.topic,
								"Partition": consumerrecord.partition,
								"Offset": consumerrecord.offset,
								"Key": consumerrecord.key,
								"Value": consumerrecord.value
							}
							print(message)
							# 消费逻辑执行完毕后在提交偏移量
							self._consumer.commit()
						else:
							print("%s consumerrecord is None." % key)
				# 非手动方式拉取消息
				'''
				for consumerrecord in self._consumer:
					if consumerrecord:
						message = {
							"Topic": consumerrecord.topic,
							"Partition": consumerrecord.partition,
							"Offset": consumerrecord.offset,
							"Key": consumerrecord.key,
							"Value": consumerrecord.value
						}
						print(message)
						self._consumer.commit()
				'''
		except Exception as err:
			print(err)

	# 获取规定个数的数据（可修改做无限持续获取数据）
	def get_message(self, count=1):
		"""
		:param topic:   topic
		:param count: 取的条数
		:return: msg
		"""
		counter = 0
		msg = []
		try:
			for message in self._consumer:
				print(
					"%s:%d:%d: key=%s value=%s header=%s" % (
						message.topic, message.partition,
						message.offset, message.key, message.value, message.headers
					)
				)
				msg.append(message.value)
				counter += 1
				if count == counter:
					break
				else:
					continue
			self._consumer.commit()
		except Exception as e:
			print("{0}, {1}".format(e, traceback.print_exc()))
			return None
		return msg

	# 查看剩余量
	def get_count(self, topic):
		"""
		:param topic: topic
		:return: count
		"""
		try:
			partitions = [TopicPartition(topic, p) for p in self._consumer.partitions_for_topic(topic)]

			# print("start to cal offset:")

			# total
			toff = self._consumer.end_offsets(partitions)
			toff = [(key.partition, toff[key]) for key in toff.keys()]
			toff.sort()
			# print("total offset: {}".format(str(toff)))

			# current
			coff = [(x.partition, self._consumer.committed(x)) for x in partitions]
			coff.sort()
			# print("current offset: {}".format(str(coff)))

			# cal sum and left
			toff_sum = sum([x[1] for x in toff])
			cur_sum = sum([x[1] for x in coff if x[1] is not None])
			left_sum = toff_sum - cur_sum
		# print("kafka left: {}".format(left_sum))

		except Exception as e:
			print("{0}, {1}".format(e, traceback.print_exc()))
			return None

		return left_sum

	def closeConnection(self):
		# 关闭消费者。
		self._consumer.close()


def main():
	try:
		c = Consumer(KafkaServerList=['172.21.26.54:9092'], Topics=['TestTopic'])
		# c.consumeMsg()
		c.get_message(2)
		print(c.get_count('TestTopic'))

	except Exception as err:
		print(err)


if __name__ == "__main__":
	try:
		main()
	finally:
		sys.exit()
