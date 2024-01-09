# -*- coding: utf-8 -*-

# @Project : apiTest
# @File    : __init__.py.py
# @Date    : 2019-11-29
# @Author  : hutong
# @Describe: 微信公众： 大话性能

import os

class Config(object):
    """Base config class."""
    # 项目路径
    prj_path = os.path.dirname(os.path.abspath(__file__))  # 当前文件的绝对路径的上一级，__file__指当前文件

    data_path = prj_path  # 数据目录，暂时在项目目录下
    test_path = prj_path  # 用例目录，暂时在项目目录下

    log_file = os.path.join(prj_path, 'log.txt')  # 也可以每天生成新的日志文件
    report_file = os.path.join(prj_path, 'report.html')  # 也可以每次生成新的报告


    case_path = '/PycharmProjects/apiTest/test_case_data/' #excel测试用例数据路径
    sheet_name = 'httpcase' #excel的sheet页名字
    html_path = '/PycharmProjects/apiTest/test_report/' #html 结果报告路径

    log_path = '/PycharmProjects/apiTest/log/'

    # 邮件配置
    smtp_server = 'smtp.sina.com'
    smtp_user = 'test_results@sina.com'
    smtp_password = 'hanzhichao123'

    sender = smtp_user  # 发件人
    receiver = '2375247815@qq.com'  # 收件人
    subject = '接口测试报告'  # 邮件主题
    '''开发环境'''



    '''生产环境'''


