# -*- coding: utf-8 -*-

# @Project : apiTest
# @File    : dataConvert.py
# @Date    : 2019-12-02
# @Author  : hutong
# @Describe: 微信公众： 大话性能

import time

#数据类型转换

#bitarray对象可以轻松将二进制串转化为bitarray对象，然后bitarray对象可以轻松转化为bytes

from bitarray import bitarray

import struct
import binascii

from enum import Enum, unique


# 定义msgType
@unique
class MsgType(Enum):
    realTimeAlarm = 0

    reqLoginAlarm = 1
    ackLoginAlarm = 2

    reqSyncAlarmMsg = 3
    ackSyncAlarmMsg = 4

    reqSyncAlarmFile = 5
    ackSyncAlarmFile = 6
    ackSyncAlarmFileResult = 7

    reqHeartBeat = 8
    ackHeartBeat = 9
    closeConnAlarm = 10

def str2bitarray(s):
    ret = bitarray(''.join([bin(int('1' + hex(c)[2:], 16))[3:] for c in s.encode('utf-8')]) , endian ='big')
    return ret

def bitarray2str(bit):
    return bit.tobytes().decode('utf-8')

def str_to_hex(s):
    return ' '.join([hex(ord(c)).replace('0x', '') for c in s])

def hex_to_str(s):
    return ''.join([chr(i) for i in [int(b, 16) for b in s.split(' ')]])

def str_to_bin(s):
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])

def bin_to_str(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])



#利用struct打包和解包自定义的socket消息
#startSign = 0xFFFF # 2个字节
#startSign = -1
#打包
def pack_data(msgType, timeStamp, lenOfBody, strBody,startSign = -1): #msgType：消息类型，1个字节，0-10, timeStamp:4个字节，大端模式,lenOfBody:2个字节，大端模式
    fmt = '>hbih{}s'.format(len(strBody.encode('utf-8')))  # h--2个字节，i--4个字节，b--1个字节
    msg_pack = struct.pack(fmt, startSign, msgType, timeStamp, lenOfBody, bytes(strBody.encode()))
    print('打包后的字节流为: ', msg_pack)
    #print('16进制显示为： ',binascii.hexlify(msg_pack))
    return msg_pack

#解包
#hexstr = b'ffff015df20b5200247265714c6f67696e3b757365723d7969793b6b65793d71772324403b747970653d6d7367'
def unpack_hexstr(hexstr):
    packed_data = binascii.unhexlify(hexstr)
    lenOfBody = len(packed_data) - 9
    fmt = '>hbih{}s'.format(lenOfBody)
    recv_msg = struct.unpack(fmt,packed_data)
    msgType = recv_msg[1]
    timeStamp = recv_msg[2]
    len_of_body = recv_msg[3]
    strbody = recv_msg[4]
    print(msgType,timeStamp,len_of_body,strbody)

#bytesstr = b'\xff\xff\x01]\xf2\x0bR\x00$reqLogin;user=yiy;key=qw#$@;type=msg'
def unpack_bytes(bytesstr): #消息头9个字节
    lenOfBody = len(bytesstr) - 9
    fmt = '>hbih{}s'.format(lenOfBody)
    recv_msg = struct.unpack(fmt,packed_data)
    msgType = recv_msg[1]
    timeStamp = recv_msg[2]
    len_of_body = recv_msg[3]
    bytes_body = recv_msg[4]   #bytes类型
    str_body = bytes_body.decode('utf-8')
    body_list = str_body.split(';')

    if (MsgType.reqLoginAlarm == msgType):
        #登陆响应
        #ackLoginAlarm;result=fail;resDesc=username-error
        result = body_list[1]
        if 'result=success' == result:
            print('login success')
        else:
            print('login error, {}'.format(body_list[2]))

        #
        #ackSyncAlarmMsg;reqId=33;result=succ;resDesc=null
    print(body_list)

    print(msgType,timeStamp,len_of_body,str_body)


def unpack_bytes_2(bytesstr): #消息头9个字节

    fmt = '>hbih{}s'.format(lenOfBody)
    recv_msg = struct.unpack(fmt,packed_data)
    msgType = recv_msg[1]
    timeStamp = recv_msg[2]
    len_of_body = recv_msg[3]
    bytes_body = recv_msg[4]   #bytes类型
    str_body = bytes_body.decode('utf-8')
    body_list = str_body.split(';')

    if (MsgType.reqLoginAlarm == msgType):
        #登陆响应
        #ackLoginAlarm;result=fail;resDesc=username-error
        result = body_list[1]
        if 'result=success' == result:
            print('login success')
        else:
            print('login error, {}'.format(body_list[2]))

        #
        #ackSyncAlarmMsg;reqId=33;result=succ;resDesc=null
    print(body_list)

    print(msgType,timeStamp,len_of_body,str_body)

#登陆请求
strBody = 'reqLogin;user=yiy;key=qw#$@;type=msg'

fmt = '>hbih{}s'.format(len(strBody.encode())) #h--2个字节，i--4个字节，b--1个字节
#startSign = 0xFFFF # 2个字节
startSign = -1
print (struct.unpack('h',b'\xff\xff'))
msgType = 1 #1个字节
#timeStamp = time.time().split(.)    #4字节
timeStamp =  1576143698   #4字节
print(type(timeStamp))
lenOfBody= len(strBody.encode('utf-8'))#2个字节
print(lenOfBody)
offset = struct.calcsize('>l')
print(offset)
print(type(startSign),startSign)
print(str)
print(struct.pack('>hbh',-1,1,36))
time_pack = struct.pack('>i',1576143698) #R对应的16进制是\x52，显示bug
print(time_pack)
print(binascii.hexlify(time_pack))
print(str_to_hex(strBody))
print(len(strBody.encode()))
print(bytes(strBody, encoding="utf8"))
packed_data = struct.pack('>36s',bytes(strBody.encode()))
print(binascii.hexlify(packed_data))
login_pack= struct.pack(fmt,startSign,msgType,timeStamp,lenOfBody,bytes(strBody.encode()))
print('finall: ',login_pack)

print(type(binascii.hexlify(login_pack)))

#print(str2bitarray(msgType))


# 假设有一个结构体
# struct header {
#   int buf1;
#   double buf2;
#   char buf3[11];
# }
#bin_buf_all = struct.pack('id11s', buf1, buf2, buf3)



'''
文本总是Unicode，由str类型表示，二进制数据则由bytes类型表示。
以Unicode表示的str通过encode()方法可以编码为指定的bytes
如果我们从网络或磁盘上读取了字节流，那么读到的数据就是bytes。要把bytes变为str，就需要用decode()方法'''


#struct模块来解决bytes和其他二进制数据类型的转换
import struct

struct.pack('>I', 10240099) #>表示字节顺序是big-endian，也就是网络序，I表示4字节无符号整数。

struct.unpack('>IH', b'\xf0\xf0\xf0\xf0\x80\x80')   #根据>IH的说明，后面的bytes依次变为I：4字节无符号整数和H：2字节无符号整数



#Python的hashlib提供了常见的摘要算法，如MD5，SHA1等等


import hashlib

md5 = hashlib.md5()
md5.update('how to use md5 in python hashlib?'.encode('utf-8'))
#print(md5.hexdigest())

import socket



if __name__ == "__main__":
    msgType = 1
    timeStamp = 1576143698
    strBody = 'reqLogin;user=yiy;key=qw#$@;type=msg'
    lenOfBody = len(strBody)
    msg_pack = pack_data(msgType, timeStamp, lenOfBody, strBody, startSign=-1)
    hexstr = b'ffff015df20b5200247265714c6f67696e3b757365723d7969793b6b65793d71772324403b747970653d6d7367'
    print(len(hexstr))
    packed_data = binascii.unhexlify(b'ffff015df20b5200247265714c6f67696e3b757365723d7969793b6b65793d71772324403b747970653d6d7367')
    print(len(packed_data))
    #unpack_data(hexstr)
    print(type(hexstr),type(packed_data))
    print(time.time(),int(time.time()))
    bytesstr = b'\xff\xff\x01]\xf2\x0bR\x00$reqLogin;user=yiy;key=qw#$@;type=msg'
    unpack_bytes(bytesstr)

    import json
    #自定义消息头，共9个字节
    socket_header = {
        'startSign': -1,#2个字节
        'msgType': 1, #1个字节
        'timeStamp': timeStamp, #4个字节，大端模式
        'lenOfBody': lenOfBody  #2个字节，大端模式
    }
    print('socket_header 字符串长度，', len(socket_header),len(json.dumps(socket_header).encode()))
    print(socket_header.get('timeStamp'))