# -*- coding: utf-8 -*-

# @Project : apiTest
# @File    : dubboClient.py
# @Date    : 2019-11-30
# @Author  : hutong
# @Describe: 微信公众： 大话性能

from  pyhessian.client import  HessianProxy
from  pyhessian import protocol

from logUtil.mylog import Log
from retrying import retry

mylogger = Log(__name__).getlogger()


class DubboInterface():
    def __init__(self,url,interface,method,param,**kwargs):
        self.url=url
        self.interface=interface
        self.method=method
        self.param=param
        self.interfaceparam=protocol.object_factory(self.param,**kwargs)

    def getresult(self):
        try:
            result=HessianProxy(self.url+self.interface)
            return_result=getattr(result,self.method)(self.interfaceparam)
            mylogger.info('dubbo 测试返回结果:%s'%return_result)
            res={'code':0,'result':return_result}
        except Exception as e:
            mylogger.error('dubbo 测试失败，原因：%s'%e, exc_info=True)
            res={'code':1,'result':e}
        return  res


if __name__ == "__main__":
    pass
