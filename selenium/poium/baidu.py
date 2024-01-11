# -*- coding:utf-8 -*-

# @Time: 2024/1/11 10:22
# @Project: test
# @File: baidu.py
# @Author: WSM
import unittest

from baidu_page import BaiduPage


class TestBaidu(unittest.TestCase):

    def test_baidu_search_case1(self):
        page = BaiduPage(self.driver)
        page.get("https://www.baidu.com")
        page.search_input = "selenium"
        page.search_button.click()
