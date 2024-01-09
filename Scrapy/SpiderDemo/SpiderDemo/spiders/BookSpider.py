# -*- coding: utf-8 -*-

# @Time : 2023/2/17 09:58
# @Project : myScrapy
# @File : BookSpider.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse
from ..items import BookItem
import json
import time


# 通过继承scrapy.Spider创建一个爬虫BookSpider
class BooksSpider(scrapy.Spider):
	name = 'epubitBook'  # 爬虫的唯一标识，不能重复，启动爬虫的时候要用
	allowed_domains = ['epubit.com']
	start_urls = [
		'https://www.epubit.com/pubcloud/content/front/portal/getUbookList?page=1&row=20&=&startPrice=&endPrice=&tagId=']

	def start_requests(self):
		# 爬取接口网页连接
		web_url = [
			'https://www.epubit.com/pubcloud/content/front/portal/getUbookList?page={}&row=20&=&startPrice=&endPrice=&tagId='.format(
				page) for page in range(1, 2)]
		for i in web_url:
			time.sleep(5)
			headers = {'Origin-Domain': 'www.epubit.com'}
			# scrapy.Request()参数一必须为str
			yield scrapy.Request(i, self.parse, headers=headers)

	def parse(self, response):
		# 将接口中提取的Json数据转为dict字典
		bk_dict = json.loads(response.text)
		records = bk_dict['data']['records']
		for r in records:
			item = BookItem()
			author = r['authors']
			name = r['name']
			price = r['price']
			# print(author,name,  price)
			item['author'] = author
			item['name'] = name
			item['price'] = price
			yield item
