# -*- coding: utf-8 -*-

# @Project : apiTest
# @File    : ftpClient.py
# @Date    : 2019-11-29
# @Author  : hutong
# @Describe: 微信公众： 大话性能


import ftplib, string

import os, sys
import threading
import multiprocessing

class MyFtp():
    timeout = 30
    def __init__(self, ip,user,passwd,port):
        self.ip=ip
        self.user=user
        self.passwd=passwd
        self.port=port
        self.ftp=ftplib.FTP(ip,user,passwd,port,30)

        # 0主动模式 1 #被动模式
        #self.ftp.set_pasv(0)
        # 关闭调试模式
        # self.ftp.set_debuglevel(0)
        print(self.ftp.getwelcome())  # 打印出欢迎信息

    def DownLoadFile(self, LocalFile, RemoteFile):  # 下载指定目录下的指定文件
        with open(LocalFile, 'wb') as fw:
            print(fw)
            #接收服务器上文件并写入本地文件
            self.ftp.retrbinary('RETR ' + RemoteFile, fw.write)

        return True

    def DownLoadFileTree(self, LocalDir, RemoteDir):  # 下载整个目录下的文件
        print("remoteDir:", RemoteDir)
        if not os.path.exists(LocalDir):
            os.makedirs(LocalDir)
        self.ftp.cwd(RemoteDir)
        RemoteNames = self.ftp.nlst()
        print("RemoteNames", RemoteNames)
        for file in RemoteNames:
            Local = os.path.join(LocalDir, file)
            print(self.ftp.nlst(file))
            if file.find(".") == -1:
                if not os.path.exists(Local):
                    os.makedirs(Local)
                self.DownLoadFileTree(Local, file)
            else:
                self.DownLoadFile(Local, file)
        self.ftp.cwd("..")
        return True

    # 从本地上传文件到ftp
    def UploadFile(self, remotepath, localpath):
        '''以二进制形式上传文件
            ftp.size()验证远程文件是否存在并且判断文件大小
        '''
        try:
            if self.ftp.size(remotepath) == os.path.getsize(localpath):
                return
        except ftplib.error_perm as err:
            print("{0}.When upload file:{1}".format(err.args[0], remotepath))
        except Exception as e:
            print("uupload file other error!")

        bufsize = 1024
        with open(localpath, 'rb') as fp:
            try:
                self.ftp.storbinary('STOR ' + remotepath, fp, bufsize)
                self.ftp.set_debuglevel(0)
            except:
                print('error!!!')

    @staticmethod
    def checkFileExtension(localfile, extension):

        '''
        检查文件名是否符合需要上传的文件类型
        extension为*时，无文件类型限制上传
        '''
        if extension == "*":
            return True
        elif localfile.endswith(extension):

            return True
        else:
            return False

    @staticmethod
    def checkFileNameContains(localfile, filecontain):

        '''
        检查特定文件名的文件
        filecontain 为 * 时,不限制上传文件名
        '''
        if filecontain == "*":
            return True
        elif filecontain in localfile:

            return True
        else:
            return False



    def close(self):
        self.ftp.quit()


if __name__=='__main__':

    ip = ''
    user = ''
    passwd = ''
    port = ''
    # 多线程下载视频文件到本地,  前提是ftp服务器中已经有100个视频文件
    fileName = 'test.xml'
    filePath = ''
    mythread = []
    for i in range(10):
        myftp = MyFtp(ip,user,passwd,port)
        mythread[i] = threading.Thread(target=myftp.DownLoadFile, args=(fileName, filePath))
        mythread[i].start()

    for i in range(10):
        mythread[i].join()


