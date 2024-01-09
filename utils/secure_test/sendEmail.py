# -*- coding: utf-8 -*-

# @Time : 2022/4/12 5:19 下午
# @Project : scanDemo
# @File : sendEmail.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8

import smtplib
from email.mime.text import MIMEText
from email.header import Header


def sendemail(sender, receiver, subject, content, smtpserver, smtpuser, smtppass):
	msg = MIMEText(content, 'html', 'utf-8')  # 中文需参数‘utf-8'，单字节字符不需要
	msg['Subject'] = Header(subject, 'utf-8')
	msg['From'] = '<%s>' % sender
	msg['To'] = ";".join(receiver)
	try:
		smtp = smtplib.SMTP()
		smtp.connect(smtpserver)
		smtp.login(smtpuser, smtppass)
		smtp.sendmail(sender, receiver, msg.as_string())
		smtp.quit()
	except Exception as e:
		print(e)


if __name__ == '__main__':
	import time

	datestring = '2021-11-03 10:43:17'
	import yaml

	import yaml

	# 通过open方式读取文件数据
	file = open('config.yml', 'r', encoding="utf-8")
	y = yaml.load_all(file, Loader=yaml.FullLoader)
	for data in y:
		print(data)


