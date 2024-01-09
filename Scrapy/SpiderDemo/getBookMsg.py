# -*- coding: utf-8 -*-

# @Time : 2023/2/17 08:57
# @Project : myScrapy
# @File : getBookMsg.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


import requests
'''抓取指定页的数据，默认是第1页'''
def get_page(page=1):
	# 使用page动态拼接URL
	url = f'https://www.epubit.com/pubcloud/content/front/portal/getUbookList?page={page}&row=20&=&startPrice=&endPrice=&tagId='
	headers = {'Origin-Domain': 'www.epubit.com'}
	# 请求的时候同时传入headers
	res = requests.get(url, headers=headers)
	print(res.text)


get_page(1)
