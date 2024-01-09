# -*- coding: utf-8 -*-

# @Project : apiTest
# @File    : testlog.py
# @Date    : 2019-11-29
# @Author  : hutong
# @Describe: 微信公众： 大话性能

from logUtil.mylog import Log

mylogger = Log(__name__).getlogger()

if __name__ == '__main__':
    try:
        mylogger.info('this is test................................................................................')
        mylogger.info('this is test')
        mylogger.info('this is test')
        mylogger.info('this is test')
        mylogger.info('this is test')
        open("/home/guoweikuang/fuck.log", 'rb')
    except (SystemExit, KeyboardInterrupt):
        raise

    except Exception as e:
        mylogger.error("failed to open file, ", exc_info=True)