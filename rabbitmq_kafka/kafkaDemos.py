# -*- coding: utf-8 -*-

# @Time : 2022/3/28 10:04 上午
# @Project : msgUtil
# @File : kafkaDemos.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import kafka_errors
import traceback
import json


def producer_demo():
    # 假设生产的消息为键值对（不是一定要键值对），且序列化方式为json
    producer = KafkaProducer(
        bootstrap_servers=['172.21.26.54:9092'],
        key_serializer=lambda k: json.dumps(k).encode(),
        value_serializer=lambda v: json.dumps(v).encode())
    # 发送三条消息
    for i in range(0, 3):
        future = producer.send(
            'kafka_demo',
            key='count_num',  # 同一个key值，会被送至同一个分区
            value=str(i),
            partition=0)  # 向分区0发送消息
        print("send {}".format(str(i)))
        try:
            future.get(timeout=10) # 监控是否发送成功
        except kafka_errors:  # 发送失败抛出kafka_errors
            traceback.format_exc()

def consumer_demo():
    consumer = KafkaConsumer(
        'kafka_demo',
        bootstrap_servers='172.21.26.54:9092',
        group_id='test',
    )
    #实时拉取数据
    '''
    for message in consumer:
        print("receive, key: {}, value: {}".format(
            json.loads(message.key.decode()),
            json.loads(message.value.decode())
            )
        )
    '''
    #指定拉取数据间隔
    poll_interval = 5000

    while True:
        msgs = consumer.poll(poll_interval, max_records=50)
        for msg in msgs:
            print( msgs.get(msg)[0])# 返回的是ConsumerRecord对象，可以通过字典的形式获取内容。
            print(msgs.get(msg)[0].value)


if __name__ == '__main__':
	producer_demo()
	#consumer_demo()
