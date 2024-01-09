# -*- coding: utf-8 -*-

# @Project : apiTest
# @File    : socketClient.py
# @Date    : 2019-11-29
# @Author  : hutong
# @Describe: 微信公众： 大话性能

import socket
import os
import struct
import threading
import base64
import json
import time
import re
import subprocess
from ast import literal_eval
import binascii
from excelUtil import myexcel

#把发送请求打包成bytes
def pack_data(msgType, timeStamp, strBody,startSign = -1): #msgType：消息类型，1个字节，0-10, timeStamp:4个字节，大端模式,lenOfBody:2个字节，大端模式
    fmt = '>hbih{}s'.format(len(strBody.encode('utf-8')))  # h--2个字节，i--4个字节，b--1个字节
    msg_pack = struct.pack(fmt, startSign, msgType, timeStamp, len(strBody), bytes(strBody.encode()))
    print('打包后的字节流为: ', msg_pack)
    #print('16进制显示为： ',binascii.hexlify(msg_pack))
    return msg_pack

#解包，返回消息体的长度
def unpack_body_len(bytes_header): #消息头9个字节
    fmt = '>hbih'   #9个字节，固定消息头
    recv_msg = struct.unpack(fmt,bytes_header) # recv_msg是元组
    len_of_body = recv_msg[3]   #消息的内容的长度，用于进一步receive消息
    return len_of_body

#解包，处理tcp粘包问题
def unpack_bytes(bytes_header): #消息头9个字节
    fmt = '>hbih'   #9个字节，固定消息头
    recv_msg = struct.unpack(fmt,bytes_header) # recv_msg是元组
    startSign = recv_msg[0]
    msgType = recv_msg[1]
    timeStamp = recv_msg[2]
    len_of_body = recv_msg[3]   #消息的内容的长度，用于进一步receive消息
    str_header = 'startSign={},msgType={},timeStamp={}, bodyLen={}'.format(startSign,msgType,timeStamp,len_of_body)
    return str_header

class socketUtil():
    def __init__(self, ip, port, username, passwd, typeMsg, vendor):

        #每个厂商，生成一个以厂商命名的目录，用于保存数据
        currentPath = os.getcwd()
        self.filePath = os.path.join(currentPath,vendor)
        #print('filepath : ',self.filePath)
        if not os.path.exists(self.filePath):
            # os.makedirs( self.jmxPath)
            mkdir_cmd = 'mkdir -p ' + self.filePath
            subprocess.run(mkdir_cmd, shell=True)

        self.total_alarms = 0 # 统计上报的告警数目
        self.tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.tcpCliSock.bind(('192.168.1.6', 11560))   #可以制定客户端使用的端口
        try:
            self.tcpCliSock.connect((ip,port))
            self.tcpCliSock.setblocking(1)
            self.tcpCliSock.settimeout(180)

            #获取本机的ip和端口
            self.cli_addr = self.tcpCliSock.getsockname()
            print('client {} socket connect success'.format(self.cli_addr))
        except BaseException as msg:
            print('client {} socket connect fail!! exception result:{}'.format( self.cli_addr,msg))

        #登陆认证的用户名/密码
        self.username = username
        self.passwd =passwd
        #请求类别type：msg/file
        self.type = typeMsg


    #socket进行认证
    def login(self,timeStamp ):
        msg_type = 1  # 需要参数化
        #time_stamp = 1576143698  # 需要参数化
        str_body = 'reqLogin;user={};key={};type={}'.format(self.username,self.passwd,self.type)  # 需要参数化
        login_bytes = pack_data(msg_type, timeStamp, str_body)  # 登陆请求打包成bytes

        try:
            result = self.tcpCliSock.sendall(login_bytes)    #发送完整的TCP数据，成功返回None，失败抛出异常
            if None == result:
                print('{} send {} login msg success'.format(self.cli_addr,self.username))

        except Exception as e:
            print('{} send login msg error: {} '.format(self.cli_addr,e))

        # 开始接收登陆响应请求
        login_header= self.tcpCliSock.recv(9) # 消息头，9个字节
        print('收到服务端的原始消息头：{}, 解码后消息头：{}'.format(login_header,unpack_bytes(login_header)))
        body_login_size = unpack_body_len(login_header)  # 解包消息头,获取消息体长度
        body_response_login = self.tcpCliSock.recv(body_login_size).decode('utf-8')  # 获取消息体
        if 'fail' in body_response_login:
            print('login error, client {}, response msg: {} '.format(self.cli_addr,body_response_login))
            # return {'error':body_response_login}
            # resDesc：登录失败原因，长度小于32个字符。
            # 消息样例：ackLoginAlarm;result = fail;resDesc = username - error
            try:
                req_desc_pattern = r'resDesc=(.*)'
                res_desc = re.search(req_desc_pattern, body_response_login).group(1)
                #res_desc = body_response_login.split('=')[2]
            except Exception as e:
                print('解析响应结果错误，响应为：{}'.format(body_response_login))
            else:
                if len(res_desc) >= 32:
                    print('login error, 返回的resDesc字符串长度大于32个字符，不符合要求,client {}'.format(self.cli_addr))
                    # return {'error': '返回的resDesc字符串长度大于32个字符，不符合要求'}
        elif 'succ' in body_response_login:
            print('login success, client {}, user {} '.format(self.cli_addr, self.username))
        else:
            print( 'other error, 响应：{}'.format(body_response_login))
        #return True

    #统计告警数目
    def receive_static(self, period): #对于上报的告警消息realTimeAlarm，消息体中只包括一条json格式的告警数据。
        start_time = time.time()
        while True:
            body_alarm_size = unpack_body_len(self.tcpCliSock.recv(9))  # 接收消息头，9个字节,解包函数返回到是消息体的长度
            body_alarm_bytes = self.tcpCliSock.recv(body_alarm_size)
            body_alarm_json = body_alarm_bytes.decode('utf-8')  # 获取告警消息体，是json
            body_alarm_dict = json.loads(body_alarm_json)
            alarmSeq = body_alarm_dict.get('alarmSeq')  # 获取告警消息序号
            self.total_alarms += 1
            now_time = time.time()
            if now_time -start_time >= period:
                print('在{}s时间内，收到告警数：{}'.format(period,self.total_alarms))
                break


    #认证成功后，开始接收omc上报的实时告警，并保存到文件,文件命名规则：
    # msg-all-{username}-2019-12-25-13.txt
    # msg-lost-{username}-2019-12-25-13.txt
    # msg-found-{username}-2019-12-25-13.txt
    # file-XXX-{username}.zip
    def receive_save(self, year,month,day,hour): #对于上报的告警消息realTimeAlarm，消息体中只包括一条json格式的告警数据。
        #msg_type = 0

        fileName = '{}-all-{}-{}-{}-{}-{}.txt'.format(self.type,self.username,year,month,day,hour)
        full_file_name = os.path.join(self.filePath,fileName)
        print('保存收到的所有实时告警全路径文件为：{}'.format(full_file_name))
        #开始接收告警数据
        body_alarm_size_1 = unpack_body_len(self.tcpCliSock.recv(9))  # 接收消息头，9个字节,解包函数返回到是消息体的长度
        body_alarm_bytes_1 = self.tcpCliSock.recv(body_alarm_size_1)
        body_alarm_json_1 = body_alarm_bytes_1.decode('utf-8')  # 获取告警消息体，是json
        body_alarm_dict_1 = json.loads(body_alarm_json_1)
        alarmSeq_1 = body_alarm_dict_1.get('alarmSeq')  #获取告警消息序号
        self.total_alarms += 1
        while True:
            body_alarm_size_2 = unpack_body_len(self.tcpCliSock.recv(9))  # 接收消息头，9个字节,解包函数返回到是消息体的长度
            body_alarm_bytes_2 = self.tcpCliSock.recv(body_alarm_size_2)
            body_alarm_json_2 = body_alarm_bytes_2.decode('utf-8')  # 获取告警消息体，是json
            body_alarm_dict_2 = json.loads(body_alarm_json_2)
            alarmSeq_2 = body_alarm_dict_2.get('alarmSeq')  # 获取告警消息序号
            self.total_alarms += 1
            with open(full_file_name, "wb+") as f:
                f.write(body_alarm_bytes_2)
                f.write("\r\n")
            result = self.check_sequence(alarmSeq_1,alarmSeq_2)
            if result != 1: #告警消息序号不连续
                print('告警消息序号不连续!!!!!，序号编号：{},具体消息内容：{}'.format(alarmSeq_1,body_alarm_json_1))
                print('告警消息序号不连续!!!!!，序号编号：{},具体消息内容：{}'.format(alarmSeq_2,body_alarm_json_2))
            alarmSeq_1 = alarmSeq_2
            body_alarm_json_1 = body_alarm_json_2


    #检验前后2个序号是否连续，序号到了2**31-1后，就重新编号为1
    @staticmethod
    def check_sequence(first_n, second_n):
        div_num = second_n - first_n
        if div_num == 1 or div_num == -2147483646:
            return 1

    #发送消息方式同步告警请求，消息名：reqSyncAlarmMsg
    def send_sync_msg(self,reqId,alarmSeq):
        msg_type = 3  # 需要参数化
        time_stamp = 1576143698  # 需要参数化
        #消息样例：reqSyncAlarmMsg;reqId=33;alarmSeq=10
        str_body = 'reqSyncAlarmMsg;reqId={};alarmSeq={}'.format(reqId,alarmSeq)  # 需要参数化
        sync_msg_bytes = pack_data(msg_type, time_stamp, str_body)  # 请求打包成bytes

        try:
            result = self.tcpCliSock.sendall(sync_msg_bytes)
            # 发送完整的TCP数据，成功返回None，失败抛出异常
            if None == result:
                print('success,send sync msg success')
        except Exception as e:
            print('send sync_msg error ', e)

        # 开始接收同步响应请求
        body_sync_msg_size = unpack_body_len(self.tcpCliSock.recv(9))  # 接收消息头，9个字节
        body_response_sync_msg = self.tcpCliSock.recv(body_sync_msg_size).decode('utf-8')  # 获取消息体
        if 'fail' in body_response_sync_msg:
            print('error, sync msg response: {}'.format(body_response_sync_msg))
            # resDesc：登录失败原因，长度小于32个字符，不允许带分号“;”。
            #消息样例：ackSyncAlarmMsg;reqId=33;result=succ;resDesc=null
            try:
                req_desc_pattern = r'resDesc=(.*)'
                res_desc = re.search(req_desc_pattern, body_response_sync_msg).group(1)
                #res_desc = body_response_sync_msg.split('=')[3]
            except Exception as e:
                print('解析响应结果错误，响应为：{}'.format(body_response_sync_msg))
            else:
                if len(res_desc) >= 32 or ';' in res_desc:
                    print('error, 消息方式同步告警，返回的resDesc字符串长度大于32个字符或者包含分号，不符合要求')
                    # return {'error': '返回的resDesc字符串长度大于32个字符，不符合要求'}
        elif 'succ' in body_response_sync_msg:
            print('success，receive sync msg response success')
        else:
            print('other error , 响应：{}'.format(body_response_sync_msg))

    #保存补发的告警，文件命名规则：msg-found-{username}-2019-12-25-13.txt
    def save_alarm_msg(self, fileName): #对于上报的告警消息realTimeAlarm，消息体中只包括一条json格式的告警数据。
        #msg_type = 0
        #开始接收告警数据
        msgNum = 0 #统计接收的数目
        while True:
            body_alarm_size = unpack_body_len(self.tcpCliSock.recv(9))  # 接收消息头，9个字节,解包函数返回到是消息体的长度
            body_alarm_bytes = self.tcpCliSock.recv(body_alarm_size)
            body_alarm_json = body_alarm_bytes.decode('utf-8')  # 获取告警消息体，是json
            body_alarm_dict = json.loads(body_alarm_json)
            alarmSeq = body_alarm_dict.get('alarmSeq')  # 获取告警消息序号
            with open(fileName, "wb+") as f:
                f.write(body_alarm_bytes)
                f.write("\r\n")
            print('接收到的实时告警序号为：{}, 具体告警内容见文件：{}'.format(alarmSeq,fileName))
            msgNum = msgNum +1
            if msgNum == 50:   break

    #发送文件方式同步告警请求，步骤4
    #1、基于告警起止时间进行文件方式同步
    def send_sync_file_time(self,startTime,endTime,reqId,syncSource):    #syncSource 取值0或1
        #消息样例：reqSyncAlarmFile;reqId=34;startTime=2014-11-27 10:00:00;endTime=2014-11-27 10:30:00; syncSource =1
        msg_type = 5  # 需要参数化
        time_stamp = 1576143698  # 需要参数化
        str_body = 'reqSyncAlarmFile;reqId={};startTime={};endTime={};syncSource={}'.format(reqId, startTime,endTime,syncSource)
        sync_file_bytes = pack_data(msg_type, time_stamp, str_body)  # 请求打包成bytes

        try:
            result = self.tcpCliSock.sendall(sync_file_bytes)
            # 发送完整的TCP数据，成功返回None，失败抛出异常
            if None == result:
                print('success,send sync file success，基于告警起止时间方式')
        except Exception as e:
            print('send sync file error，基于告警起止时间方式 ', e)

        # 开始接收同步响应请求，无结果的立即应答，步骤5
        body_sync_file_size = unpack_body_len(self.tcpCliSock.recv(9))  # 接收消息头，9个字节
        body_response_sync_file = self.tcpCliSock.recv(body_sync_file_size).decode('utf-8')  # 获取消息体
        if 'fail' in body_response_sync_file:
            print('error, sync msg response: {}，基于告警起止时间方式'.format(body_response_sync_file))
            # resDesc：登录失败原因，长度小于32个字符，不允许带分号“;”。
            #消息样例：ackSyncAlarmFile;reqId=33;result=succ;resDesc=null
            try:
                req_desc_pattern = r'resDesc=(.*)'
                res_desc = re.search(req_desc_pattern, body_response_sync_file).group(1)
                #res_desc = body_response_sync_msg.split('=')[3]
            except Exception as e:
                print('解析响应结果错误，响应为：{}，基于告警起止时间方式'.format(body_response_sync_file))
            else:
                if len(res_desc) >= 32 or ';' in res_desc:
                    print('error, 基于告警起止时间方式，文件方式同步告警请求响应，返回的resDesc字符串长度大于32个字符或者包含分号，不符合要求')
                    # return {'error': '返回的resDesc字符串长度大于32个字符，不符合要求'}
        elif 'succ' in body_response_sync_file:
            print('success，receive sync file response success，基于告警起止时间方式')
        else:
            print('error, 其他错误，响应：{}，基于告警起止时间方式'.format(body_response_sync_file))


    # 2、基于起始告警消息序号进行文件方式同步
    def send_sync_file_seq(self,reqId,alarmSeq): #syncSource只能取值1

        # 消息样例：reqSyncAlarmFile;reqId=35;alarmSeq=100;syncSource =1
        syncSource = 1
        msg_type = 5  # 需要参数化
        time_stamp = 1576143698  # 需要参数化
        str_body = 'reqSyncAlarmFile;reqId={};alarmSeq={};syncSource=1'.format(reqId, alarmSeq)
        sync_file_bytes = pack_data(msg_type, time_stamp, str_body)  # 请求打包成bytes

        try:
            result = self.tcpCliSock.sendall(sync_file_bytes)
            # 发送完整的TCP数据，成功返回None，失败抛出异常
            if None == result:
                print('success,send sync file success, 基于起始告警序号方式')
        except Exception as e:
            print('send sync file error，基于起始告警序号方式 ', e)

        # 开始接收同步响应请求，无结果的立即应答，步骤5
        body_sync_file_size = unpack_body_len(self.tcpCliSock.recv(9))  # 接收消息头，9个字节
        body_response_sync_file = self.tcpCliSock.recv(body_sync_file_size).decode('utf-8')  # 获取消息体
        if 'fail' in body_response_sync_file:
            print('error, sync msg response: {}，基于起始告警序号方式'.format(body_response_sync_file))
            # resDesc：登录失败原因，长度小于32个字符，不允许带分号“;”。
            # 消息样例：ackSyncAlarmFile;reqId=33;result=succ;resDesc=null
            try:
                req_desc_pattern = r'resDesc=(.*)'
                res_desc = re.search(req_desc_pattern, body_response_sync_file).group(1)
                # res_desc = body_response_sync_msg.split('=')[3]
            except Exception as e:
                print('解析响应结果错误，响应为：{}，基于起始告警序号方式'.format(body_response_sync_file))
            else:
                if len(res_desc) >= 32 or ';' in res_desc:
                    print('error, 基于起始告警序号方式，文件方式同步告警请求响应，返回的resDesc字符串长度大于32个字符或者包含分号，不符合要求')
                    # return {'error': '返回的resDesc字符串长度大于32个字符，不符合要求'}
        elif 'succ' in body_response_sync_file:
            print('success，receive sync file response success，基于起始告警序号方式')
        else:
            print('error, 其他错误，响应：{}，基于起始告警序号方式'.format(body_response_sync_file))


    #接收文件告警同步的结果消息，非立即响应结果， 步骤8
    def receive_sync_file(self): #ackSyncAlarmFileResult（含有文件同步结果的应答）
        #ackSyncAlarmFileResult;reqId=33;result=suc;fileName=/ftproot/GD/WX/HW/JS_OMC2/FM/20150611/FM-OMC-1A-V1.1.0-20150611011603-001.txt;resDesc=null
        body_alarm_file_size = unpack_body_len(self.tcpCliSock.recv(9))  # 接收消息头，9个字节,解包函数返回到是消息体的长度
        body_alarm_file_bytes = self.tcpCliSock.recv(body_alarm_file_size)
        body_alarm_file_str = body_alarm_file_bytes.decode('utf-8')  # 获取告警消息体
        if 'fail' in body_alarm_file_str:
            print('error，收到文件告警同步的结果错误，返回消息：{}'.format(body_alarm_file_str))
        elif 'succ' in body_alarm_file_str:
            try:
                req_id_pattern = r'reqId=(.*?);'
                filename_pattern = r'fileName=(.*?);'
                reqId = re.search(req_id_pattern, body_alarm_file_str).group(1)
                fileName = re.search(filename_pattern, body_alarm_file_str).group(1) #返回的告警文件全路径
                #reqId = body_alarm_file_str.split(';')[1].split('=')[1]
                print('收到的文件告警同步结果消息，reqId：{},fileName:{}'.format(reqId,fileName))
                return (reqId,fileName)
            except Exception as e:
                print('解析响应结果错误，响应为：{}'.format(body_alarm_file_str))
        else:
            print('error, 其他错误，响应：{}'.format(body_alarm_file_str))



    def send(self, data):
        try:
            try:
                result = self.tcpCliSock.send(data)  # 返回发送的字节数

                #clientSocket.send(bytes(data, encoding="utf8"))
            except BaseException as msg:
                # self.__conn(self.conn_data)
                # result = self.tcpCliSock.send(data)
                print(msg)
                raise msg
            print('socket send_len:{}'.format(result))
            return result
        except BaseException as msg:
            raise ('socket send_error:{}'.format(msg))

    def recv(self, size, code):
        result = ''
        try:
            try:
                result = self.tcpCliSock.recv(int(size))

                while len(result) < int(size):
                    result += self.tcpCliSock.recv(int(size) - len(result))
            except:
                pass
            if not result:
                print('socket recv_result ERROR:result is null')
            print('socket recv_result:{}'.format( len(result)))
            data_struct = struct.unpack(code, result)
            #str(data, encoding="utf8")
            print('socket recv_result_unpack:{}'.format( data_struct))
            return data_struct
        except BaseException as msg:
            print('socket recv_error:{}'.format( msg))
            raise msg

    def only_recv(self, size):
        try:
            result = self.tcpCliSock.recv(int(size))
            # while len(result) < int(size):
            #    result += self.tcpCliSock.recv(int(size) - len(result))
            print('socket only_recv_result_len:{}'.format(len(result)))
            print('only_recv:{}'.format(result))
            return result
        except BaseException as msg:
            print('socket recv_error:{}'.format( msg))
            raise msg

    #下载文件
    def downFile(self, fileName):
        # 将文件名发送至服务器端
        self.tcpCliSock.send(fileName.encode())
        # 创建一个空文件
        new_file = open(fileName, "wb")
        # 用与计算读取的字节数
        size = 0

        while True:
            # 接收服务器端返回的内容
            mes = self.tcpCliSock.recv(4096)
            # 如果内容不为空执行
            if mes:
                # 解码并向文件内写入
                # mes = mes.decode()
                new_file.write(mes)
                # 计算字节
                size += len(mes)
            else:
                # 如果字节数为空即未收到内容
                if size == 0:
                    # 关闭文件
                    new_file.close()
                    # 删除刚刚创建的文件
                    os.remove(fileName)
                    print("没有您要下载的文件")
                else:
                    # 如过time有值时name文件传输完成
                    print("文件下载成功")
                break

    #上传文件
    def uploadFile(self,upfile):
        self.tcpCliSock.send(upfile.encode())
        while True:
            flag = self.tcpCliSock.recv(1024)
            if flag:
                with open(upfile, 'rb') as f:
                    buf = base64.b64encode(f.read())
                    self.tcpCliSock.send(buf)
                    print("finished uploading!")
                break

    # 断开连接
    def close(self):
        try:
            print('client socket {} has been closed'.format(self.cli_addr))
            self.tcpCliSock.close()
        except BaseException as msg:

            print('client socket {} close_error:{}'.format(self.cli_addr, msg))


#每隔60s发送一次心跳，单独开一个线程，用于处理心跳
def pingpong(sock):
    reqId = 1

    while True:
        msg_type = 8  # 需要参数化
        time_stamp = 1576143698  # 需要参数化
        str_body = 'reqHeartBeat;reqId={}'.format(reqId)  # 需要参数化
        heart_bytes = pack_data(msg_type, time_stamp, str_body)  # 心跳请求打包成bytes
        #msgType：8
        #消息样例：reqHeartBeat;reqId=33
        heart_result = sock.sendall(heart_bytes)
        if heart_result ==None:
            print('send reqHeartBeat msg success, reqId:{}'.format(reqId))
            #return False
        # 开始接收心跳响应请求
        try:
            body_size = unpack_bytes(sock.recv(9))  # 接收消息头，9个字节
            body_response = sock.recv(body_size).decode('utf-8')  # 获取消息体
        except socket.timeout:
            print('接收心跳包超时，180s没收到omc的响应，nms主动断开连接')
            sock.close()
            break
        else:
            #服务端返回
            #消息样例：ackHeartBeat;reqId=33
            if reqId in body_response:
                print('receive reqHeartBeat msg success, reqId:{}'.format(reqId))
                print('收到心跳响应: ', body_response)

            #return True
        time.sleep(60)
        reqId = reqId +1
        if reqId == 200:break


    '''接收大数据
            had_received = 0
            data_body = bytes()
            while had_received < pack_length:
                    part_body= self._client_socket.recv(pack_length - had_received)
                    data_body +=  part_body
                    part_body_length = len(part_body)
                    #print('part_body_length', part_body_length)
                    had_received += part_body_length

'''

if __name__ == "__main__":
    '''
    mythread = []
    for i in range(10):
        who = ''
        ip = ''
        port = ''
        username = ''
        passwd = ''
        type = ''
        mysock = socketUtil(who, ip, port, username, passwd, type, is_ping =1)
        mythread[i] = threading.Thread(target=mysock.login, args=())    #并发登陆
        mythread[i].start()

    for i in range(10):
        mythread[i].join()
    '''
    filepath = '/PycharmProjects/apiTest/test_case_data/socketcase.xlsx'  # 文件绝对路径,也可以是相对路径
    sheetname = 'hw'  # sheetname
    sheetObject = myexcel.OperateExcel(filepath, sheetname)
    testdata = sheetObject.read_all_data_line_by_line()[0]
    #for onetestdata in testdatas:
    #    print(onetestdata)
    print(testdata)
    #ip = testdata.get('ip')
    ip = '172.28.20.167'
    #port = int(testdata.get('port'))
    port = 8899
    typeMsg = 'msg'
    vendor = testdata.get('vendor')

    # 通过 literal_eval 这个函数，将str类型的列表转换成类型为list的真正的列表类型

    users = testdata.get('users')
    user_list = literal_eval(users)

    username = user_list[0].get('username')
    passwd = user_list[0].get('passwd')
    print(username)
    print(ip)
    timeStamp = 1576143698
    mysock = socketUtil(ip, port, username, passwd, typeMsg,vendor)
    mysock.login(timeStamp=timeStamp)
    #mythread = threading.Thread(target=pingpong, args=(mysock.tcpCliSock))    # 发心跳
    #mythread.start()


