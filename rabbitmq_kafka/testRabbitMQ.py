# -*- coding: utf-8 -*-

# @Time : 2022/3/19 8:50 下午
# @Project : msgUtil
# @File : testRabbitMQ.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


import threading

import threadpool
from  rabbitMQUtil import RabbitMQClient

def producer(params):
    mq_1 = RabbitMQClient("testQueue")
    for i in range(params):
        mq_1.producer(i) # 往队列中生产数据
    print("the msg nums:{}".format(mq_1.msg_count("testQueue")))


def consumer(params):
    print("this is index:{}".format(params))


def consumer_data(params):
    mq_2 = RabbitMQClient("testQueue", on_message_callback=consumer)
    mq_2.consumer() # 消费数据


if __name__ == '__main__':
    # --------生产者--------
    t1 = threading.Thread(target=producer, args=(5,))
    t1.start()

    # --------消费者--------
    pool = threadpool.ThreadPool(2)
    requests = threadpool.makeRequests(consumer_data, "data")
    [pool.putRequest(req) for req in requests]
    pool.wait()
