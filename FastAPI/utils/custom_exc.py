# -*- coding: utf-8 -*-

# @Project : fastapiDemo
# @File    : custom_exc.py
# @Date    : 2020-11-16
# @Author  : hutong
# @Describe: 微信公众： 大话性能


"""
自定义异常
"""


class PostParamsError(Exception):
    def __init__(self, err_desc: str="POST请求参数错误"):
        self.err_desc = err_desc


class TokenAuthError(Exception):
    def __init__(self, err_desc: str="token认证失败"):
        self.err_desc = err_desc

if __name__ == "__main__":
    pass
