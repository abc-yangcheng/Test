# -*- coding: utf-8 -*-

# @Project : apiTest
# @File    : ftpsharefile.py
# @Date    : 2019-12-01
# @Author  : hutong
# @Describe: 微信公众： 大话性能


#文件共享服务器
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer



if __name__ == "__main__":
    authorizer = DummyAuthorizer()
    authorizer.add_user('python', '123456', 'F:\\Working~Study', perm='elradfmwM')
    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer(('0.0.0.0', 8888), handler)
    server.serve_forever()
