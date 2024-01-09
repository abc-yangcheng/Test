# -*- coding:utf-8 -*-

# @Time: 2024/1/9 11:40
# @Project: test
# @File: baidu_main.py
# @Author: WSM
# 定义测试用例的目录为当前目录下的 test_case 目录
import unittest
import time

import yagmail
from XTestRunner import HTMLTestRunner


# 把测试报告作为附件发送到指定邮箱
def send_mail(report):
    yag = yagmail.SMTP(user="xx@qq.com",
                       password="xxx",
                       host='mail.qq.com')
    subject = "主题，自动化测试报告"
    contents = "正文，请查看附件。"
    yag.send('xx@qq.com', subject, contents, report)
    print('email has send out !')




if __name__ == '__main__':
    test_dir = './test_case'
    suit = unittest.defaultTestLoader.discover(test_dir, pattern='baidu.py')
    # 获取当前日期和时间
    now_time = time.strftime("%Y-%m-%d %H_%M_%S")
    html_report = './test_report/' + now_time + 'result.html'
    fp = open(html_report, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title="百度搜索测试报告",
                            description="运行环境：Windows 10, Chrome 浏览器"
                            )
    runner.run(suit)
    fp.close()
    # send_mail(html_report)  # 发送报告
