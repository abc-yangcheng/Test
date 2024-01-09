# -*- coding: utf-8 -*-

# @Time : 2022/3/20 12:45 下午
# @Project : msgUtil
# @File : RabbitMQDemos.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


import pika
import sys



'''
###### 队列模式 ######
#生产者
credentials = pika.PlainCredentials('admin','admin')
connection = pika.BlockingConnection(pika.ConnectionParameters(
	host='172.21.26.54',
	credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True) # 队列持久化

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
	                      delivery_mode=2,  # make message persistent消息持久化
                      ))
print(" [x] Sent %r" % message)
connection.close()

#消费者
connection = pika.BlockingConnection(pika.ConnectionParameters(
	host='172.21.26.54',
	credentials=credentials))

channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)
	#time.sleep(body.count(b'.'))
	print(" [x] Done")
	#生产者端消息持久后,需要在消费者端加上(ch.basic_ack(delivery_tag =method.delivery_tag)):
	# 保证消息被消费后，消费端发送一个ack，然后服务端从队列删除该消息.
	ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue',on_message_callback=callback)
channel.start_consuming()
'''

#### 发布与订阅 #####
'''
## fanout
#生产者
credentials = pika.PlainCredentials('admin','admin')
connection = pika.BlockingConnection(pika.ConnectionParameters(
	host='172.21.26.54',
	credentials=credentials))
channel = connection.channel()
channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

message = ''.join(sys.argv[1:]) or "info:HelloWorld!"
channel.basic_publish(exchange='logs',
                      routing_key='',  # fanout的话为空(默认)
                      body=message)
print("[x]fanout模式 Sent%r" % message)
connection.close()

#消费者
credentials = pika.PlainCredentials('admin','admin')
connection = pika.BlockingConnection(pika.ConnectionParameters(
	host='172.21.26.54',
	credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')
# 不指定queue名字(为了收广播),rabbit会随机分配一个queue名字,
# exclusive=True会在使用此queue的消费者断开后,自动将queue删除
result = channel.queue_declare('',exclusive=True)
queue_name = result.method.queue

# 把声明的queue绑定到交换器exchange上
channel.queue_bind(exchange='logs',
                   queue=queue_name)

print('[*]Waiting for logs.To exit press CTRL+C')


def callback(ch, method, properties, body):
	print("[x]fanout模式 %r" % body)

channel.basic_consume(on_message_callback=callback,queue=queue_name,
                      auto_ack=True)

channel.start_consuming()
'''

##direct
'''
#生产者
credentials = pika.PlainCredentials('admin','admin')
connection = pika.BlockingConnection(pika.ConnectionParameters(
	host='172.21.26.54',
	credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct')

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'

message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange='direct_logs',
                      routing_key=severity,  # 关键字不为空，告知消息发送到哪里(info,error~)
                      body=message)

print(" [x] Sent %r:%r" % (severity, message))

connection.close()


#消费者
credentials = pika.PlainCredentials('admin','admin')
connection = pika.BlockingConnection(pika.ConnectionParameters(
	host='172.21.26.54',
	credentials=credentials))
channel = connection.channel()
channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct')

result = channel.queue_declare('',exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]

if not severities:
	sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
	sys.exit(1)

for severity in severities:
	channel.queue_bind(exchange='direct_logs',
	                   queue=queue_name,
	                   routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
	print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(on_message_callback=callback,
                      queue=queue_name,
                      auto_ack=True)

channel.start_consuming()

#topic
#生产者
credentials = pika.PlainCredentials('admin','admin')
connection = pika.BlockingConnection(pika.ConnectionParameters(
	host='172.21.26.54',
	credentials=credentials))
channel = connection.channel()
channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic') # 类型为topic


routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange='topic_logs',
                      routing_key=routing_key,
                      body=message)

print(" [x] Sent %r:%r" % (routing_key, message))
connection.close()

#消费者
credentials = pika.PlainCredentials('admin','admin')
connection = pika.BlockingConnection(pika.ConnectionParameters(
	host='172.21.26.54',
	credentials=credentials))
channel = connection.channel()
channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')

result = channel.queue_declare('',exclusive=True)

queue_name = result.method.queue

binding_keys = sys.argv[1:]

if not binding_keys:
	sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
	sys.exit(1)

#所有绑定的都能收到消息
for binding_key in binding_keys:
	channel.queue_bind(exchange='topic_logs',
	                   queue=queue_name,
	                   routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
	print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(on_message_callback=callback,
                      queue=queue_name,
                      auto_ack=True)

channel.start_consuming()
'''

#### RPC ####
#client端
import uuid


class FibonacciRpcClient(object):
	def __init__(self):
		credentials = pika.PlainCredentials('admin', 'admin')
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(
						host='172.21.26.54',
						credentials=credentials))
		self.channel = self.connection.channel()
		
		# 随机建立一个queue，为了监听返回的结果
		result = self.channel.queue_declare('',exclusive=True)
		self.callback_queue = result.method.queue  ##队列名
		self.channel.basic_consume(on_message_callback=self.on_response,  # 一接收客户端发来的指令就调用回调函数on_response
		                           auto_ack=True,
		                           queue=self.callback_queue)
	
	def on_response(self, ch, method, props, body):  # 回调
		# 每条指令执行的速度可能不一样，指令１比指令２先发送，但可能指令２的执行结果比指令１先返回到客户端，
		# 此时如果没有下面的判断，客户端就会把指令２的结果误认为指令１执行的结果
		
		if self.corr_id == props.correlation_id:
			self.response = body
	
	def call(self, n):
		self.response = None  ##指令执行后返回的消息
		self.corr_id = str(uuid.uuid4())  ##可用来标识指令(顺序)
		
		self.channel.basic_publish(exchange='',
		                           routing_key='rpc_queue',  # client发送指令，发到rpc_queue
		                           properties=pika.BasicProperties(
			                           reply_to=self.callback_queue,  # 将指令执行结果返回到reply_to队列
			                           correlation_id=self.corr_id,
		                           ),
		                           body=str(n))
		
		while self.response is None:
			self.connection.process_data_events()  # 去queue接收数据(不阻塞)

		return int(self.response)

fibonacci_rpc = FibonacciRpcClient()
print(fibonacci_rpc.channel)
print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(30)
print(" [.] Got %r" % response)

'''
#server端
import time

credentials = pika.PlainCredentials('admin','admin')
connection = pika.BlockingConnection(pika.ConnectionParameters(
	host='172.21.26.54',
	credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')


def fib(n):
	if n == 0:
		return 0
	elif n == 1:
		return 1
	else:
		return fib(n - 1) + fib(n - 2)

def on_request(ch, method, props, body):
	n = int(body)
	print(" [.] fib(%s)" % n)
	response = fib(n)  # 从客户端收到的消息
	ch.basic_publish(exchange='',  ##服务端发送返回的数据到props.reply_to队列(客户端发送指令时声明)
	                 routing_key=props.reply_to,  # correlation_id (随机数)每条指令都有随机独立的标识符
	                 properties=pika.BasicProperties(
		                    correlation_id= props.correlation_id),
	                        body=str(response))
	
	ch.basic_ack(delivery_tag=method.delivery_tag)  # 客户端持久化

channel.basic_qos(prefetch_count=1)  # 公平分发
channel.basic_consume(on_message_callback=on_request,  # 一接收到消息就调用on_request
                      queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()
'''

if __name__ == '__main__':
	pass
