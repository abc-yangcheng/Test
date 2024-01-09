# -*- coding: utf-8 -*-

# @Project : apiTest
# @File    : socket_omc.py
# @Date    : 2019-12-16
# @Author  : hutong
# @Describe: 微信公众： 大话性能



import os
import threading
import multiprocessing



### 建立进程池和线程池 组合的demo

def main():
  print ('业务代码')

def getMacSn():
    mac = ''
    mac_real = ''
    sn = ''
    return mac, mac_real, sn


class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        apply(self.func, self.args)

def main_thread():
    global sn
    thread_num =10
    threads = []
    nloops = range(thread_num)# thread_num并发线程数
    for i in nloops:
        mac, mac_real, sn = getMacSn()
        t = MyThread(main, (mac,mac_real,sn))
        threads.append(t)
    for i in nloops:
        threads[i].start()
    for i in nloops:
        threads[i].join()


if __name__=='__main__':
    result = ''
    proc = 4
    pool = multiprocessing.Pool(processes=proc)# processes进程池数量
    print("main process(%d) running..." % os.getpid())
    for i in range(proc):# proc_num 并发进程数量
        result = pool.apply_async(main_thread)
    pool.close()
    pool.join()

    if not result.successful():
        print('主进程异常：{}'.format(result.successful()))
    else:
        print('goodbye：主进程({})执行完毕'.format(os.getpid()))
