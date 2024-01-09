# -*- coding: utf-8 -*-

# @Project : apiTest
# @File    : stfpClient.py
# @Date    : 2019-12-01
# @Author  : hutong
# @Describe: 微信公众： 大话性能



import paramiko
import uuid

class MySftp(object):

    def __init__(self, host, port=22, username='root',pwd='123456'):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.__k = None

    def connect(self):
        transport = paramiko.Transport((self.host,self.port))
        transport.connect(username=self.username,password=self.pwd)
        self.__transport = transport
        self.__sftp = paramiko.SFTPClient.from_transport(self.__transport)
        self.__ssh = paramiko.SSHClient()
        self.__ssh._transport = self.__transport

    def close(self):
        self.__transport.close()
        self.__sftp.close()
    def close_ssh(self):
        self.__transport.close()
        self.__ssh.close()

    def upload(self,local_path,target_path):
        # 连接，上传
        # file_name = self.create_file()
        # 将location.py 上传至服务器 /tmp/baidu_main.py
        self.__sftp.put(local_path, target_path)

    def download(self,remote_path,local_path):
        #sftp = paramiko.SFTPClient.from_transport(self.__transport)
        self.__sftp.get(remote_path,local_path)

    def cmd(self, command):

        # 执行命令
        stdin, stdout, stderr = self.__ssh.exec_command(command)
        # 获取命令结果
        result = stdout.read()
        print (str(result,encoding='utf-8'))
        return result

if __name__ == "__main__":
    pass
