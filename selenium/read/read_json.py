# -*- coding:utf-8 -*-

# @Time: 2024/1/9 11:30
# @Project: test
# @File: read_json.py
# @Author: WSM
import json
with open("./data_file/user_info.json", "r") as f:
 data = f.read()
user_list = json.loads(data)
print(user_list)
