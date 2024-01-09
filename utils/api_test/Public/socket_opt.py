# -*- coding: utf-8 -*-

# @Project : apiTest
# @File    : socket_opt.py
# @Date    : 2019-12-17
# @Author  : hutong
# @Describe: 微信公众： 大话性能

# ！ /usr/bin/env python
# -*- coding: utf-8 -*-

import socket

# 设置发送缓冲域大小
SEND_BUF_SIZE = 4096
# 设置接收缓冲域大小
RECV_BUF_SIZE = 4096


def modify_buff_size():
    # 创建TCP socket
    # UDP socket —— s=socket.socket(socket.AF_INET,SOCK_DGRAM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 获取当前套接字关联的选项
    # socket.SOL_SOCKET —— 正在使用的socket选项
    # socket.SO_SNDBUF —— 发送缓冲区大小
    bsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    #打印更改前的发送缓冲区大小
    print("Buffer size [Before]: %d" % bsize)

    # 设置TCP套接字关联的选项
    # socket.TCP_NODELAY TCP层套接口选项
    # 1 —— 表示将TCP_NODELAY标记为TRUE
    sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)

    # 设置发送缓冲域套接字关联的选项
    sock.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_SNDBUF,
        SEND_BUF_SIZE)

    # 设置接收缓冲域套接字关联的选项
    sock.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_RCVBUF,
        RECV_BUF_SIZE)

    # 获取设置后的发送缓冲域
    bsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    print("Buffer size [After] : %d" % bsize)

if __name__ == '__main__':
    modify_buff_size()


