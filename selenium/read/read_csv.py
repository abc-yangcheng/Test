# -*- coding:utf-8 -*-

# @Time: 2024/1/9 11:25
# @Project: test
# @File: read_csv.py
# @Author: WSM
import csv
import codecs
from itertools import islice

# 读取本地 CSV 文件
data = csv.reader(codecs.open('user_info.csv', 'r', 'utf_8_sig'))
# 存放用户数据
users = []
# 循环输出每行信息
for line in islice(data, 1, None):
    users.append(line)
# 打印
print(users)
