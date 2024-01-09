# -*- coding:utf-8 -*-

# @Time: 2024/1/9 11:31
# @Project: test
# @File: baidu.py
# @Author: WSM
import unittest
from time import sleep

from ddt import data, unpack, file_data
from selenium import webdriver
from selenium.webdriver.common.by import By


class baidu(unittest.TestCase):
    """ 百度搜索测试 """
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.base_url = "https://www.baidu.com"

    def baidu_search(self, search_key):
        self.driver.get(self.base_url)
        self.driver.find_element(By.ID, "kw").send_keys(search_key)
        self.driver.find_element(By.ID, "su").click()
        sleep(2)

    def test_search_key_selenium(self):
        """" 搜索关键字：selenium """
        search_key = "selenium"
        self.baidu_search(search_key)
        self.assertEqual(self.driver.title, search_key + "_百度搜索")

    def test_search_key_unittest(self):
        """" 搜索关键字：unittest """
        search_key = "unittest"
        self.baidu_search(search_key)
        self.assertEqual(self.driver.title, search_key + "_百度搜索")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


