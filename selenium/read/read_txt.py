# -*- coding:utf-8 -*-

# @Time: 2024/1/9 11:23
# @Project: test
# @File: read_txt.py
# @Author: WSM
# 读取文件
with(open("user_info.txt", "r")) as user_file:
    data = user_file.readlines()
# 格式化处理
users = []
for line in data:
    user = line[:-1].split(":")
    users.append(user)
# 打印 users 二维数组
print(users)
