# -*- coding: utf-8 -*-

# @Project : apiTest
# @File    : baidu_main.py
# @Date    : 2019-12-16
# @Author  : hutong
# @Describe: 微信公众： 大话性能

import socket

if 'success' in 'ok, success in the end':
    print('ok')


num1 = 2**31-1
num2 = 1
test = num2 - num1
print(test ,type(test))



def check_sequence(first_n,second_n):
    div_num = second_n - first_n
    if div_num ==1 or div_num == -2147483646:
        return 1

if __name__ == "__main__":
    print(check_sequence(2**31-1,1))
    # tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # hostport = ('127.0.0.1', 8888)
    # tcpCliSock.connect(hostport)
    # cli_addr = tcpCliSock.getsockname()
    # print(cli_addr)
    str = 'ackSyncAlarmFileResult;reqId=33;result=suc;reqId=44;fileName= /ftproot/GD/WX/HW/JS_OMC2/FM/20150611/FM-OMC-1A-V1.1.0-20150611011603-001.txt;resDesc=null'
    import re
    req_id_pattern = r'reqId=(.*?);'
    res_des_pattern = r'resDesc=(.*)'
    reqId = re.search(req_id_pattern,str)
    resDes = re.search(res_des_pattern,str)
    print(reqId)
    print(reqId.group(1))
    print(resDes)
    print(resDes.group(1))

    test = [1,2,3]
    print(type(test))