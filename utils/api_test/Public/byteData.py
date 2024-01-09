# -*- coding: utf-8 -*-

# @Project : apiTest
# @File    : byteData.py
# @Date    : 2019-12-11
# @Author  : hutong
# @Describe: 微信公众： 大话性能

from enum import Enum, unique

#定义msgType
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



data = b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'

#为了将 bytes 解析为整数，使用 int.from_bytes() 方法
int.from_bytes(data, 'little')

#为了将一个大整数转换为一个字节字符串，使用 int.to_bytes() 方法
x = 94522842520747284487117727783387188
x.to_bytes(16, 'big')



if __name__ == "__main__":
    pass
