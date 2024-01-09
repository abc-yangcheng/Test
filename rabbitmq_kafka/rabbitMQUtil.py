# -*- coding: utf-8 -*-

# @Time : 2022/3/19 8:49 下午
# @Project : msgUtil
# @File : rabbitMQUtil.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


import pika
import traceback
import logging

# 配置文件
MQ_CONFIG = {
	"host": "172.21.26.54",
	"port": 5672,
	"user": "admin",
	"password": "admin"
}

def check_connection(func):
	def wrapper(self, *args, **kwargs):
		if not all([self.channel, self.connection]) or \
				any([self.channel.is_closed, self.connection.is_closed]):
			self.clean_up()
			self.connect_mq()
		return func(self, *args, **kwargs)

	return wrapper


class RabbitMQClient(object):
	'''RabbitMQClient using pika library'''

	def __init__(self, queue, on_message_callback=None):
		self.mq_config = MQ_CONFIG
		self.connection = None
		self.channel = None
		self.queue = queue
		self.on_message_callback = on_message_callback
		self.connect_mq()

	def connect_mq(self):
		"""连接 RabbitMQ 创建连接、通道 声明队列"""
		try:
			credentials = pika.PlainCredentials(self.mq_config['user'], self.mq_config['password'])
			connect_params = pika.ConnectionParameters(self.mq_config['host'],
													   self.mq_config['port'],
													   credentials=credentials,
													   heartbeat=0)

			self.connection = pika.BlockingConnection(connect_params)
			self.channel = self.connection.channel()
			self.channel.queue_declare(queue=self.queue, durable=True)
			# self.channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=True)
			# self.channel.queue_bind(queue=queue, exchange=exchange, routing_key=binding_key)
			logging.info("Succeeded to connect to RabbitMQ.")
		except Exception as e:
			logging.error("Failed to connect to RabbitMQ: {}".format(str(e)))
			traceback.print_exc()
			return False

		return True

	def clean_up(self):
		"""断开通道、链接"""
		try:
			if self.channel and self.channel.is_open:
				self.channel.close()
			if self.connection and self.connection.is_open:
				self.connection.close()
		except Exception as e:
			logging.error("Failed to close connection with RabbitMQ: {}".format(str(e)))
			traceback.print_exc()

	@check_connection
	def producer(self, message):
		"""向队列发送消息"""
		if not isinstance(message, bytes):
			message = str(message).encode()

		try:
			self.channel.basic_publish(
				exchange='',
				routing_key=self.queue,  # queue名字
				body=message,
				properties=pika.BasicProperties(
					delivery_mode=2,  # 消息持久化
					content_type="application/json"
				)
			)
		except Exception as e:
			logging.error('Failed to send message to rabbitMQ: {}'.format(str(e)))
			traceback.print_exc()

	@check_connection
	def consumer(self):
		"""从队列获取消息"""
		self.channel.basic_qos(prefetch_count=1)  # 类似权重，按能力分发，如果有一个消息，就不在给你发
		self.channel.basic_consume(  # 消费消息
			on_message_callback=self.callback,  # 如果收到消息，callback
			queue=self.queue,
		)
		try:
			self.channel.start_consuming()
		except KeyboardInterrupt:
			self.channel.stop_consuming()
			self.connection.channel()

	def callback(self, ch, method, properties, body):
		"""获取消息后的回调函数"""
		# message = ast.literal_eval(body.decode())
		print("consumed %r " % body)
		# self.on_message_callback(message)
		ch.basic_ack(delivery_tag=method.delivery_tag)  # 告诉生产者，消息处理完成

	# 统计消息数目
	def msg_count(self, queue_name, is_durable=True):
		queue = self.channel.queue_declare(queue=queue_name, durable=is_durable)
		count = queue.method.message_count

		return count


if __name__ == '__main__':
	mq = RabbitMQClient('testQueue2')
	import json

	msg = json.dumps({'name': 'hutong'})
	mq.producer(msg)
	mq.consumer()
