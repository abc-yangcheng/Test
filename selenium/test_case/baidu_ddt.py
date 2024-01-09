# -*- coding:utf-8 -*-

# @Time: 2024/1/9 13:29
# @Project: test
# @File: baidu_ddt.py
# @Author: WSM
# -*- coding:utf-8 -*-

# @Time: 2024/1/9 11:31
# @Project: test
# @File: baidu_ddt.py
# @Author: WSM
import unittest
from time import sleep

from ddt import data, unpack, file_data
from parameterized import parameterized
from selenium import webdriver
from selenium.webdriver.common.by import By


class baidu_ddt(unittest.TestCase):
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

    # 通过 Parameterized 实现参数化
    @parameterized.expand([
        ("case1", "selenium"),
        ("case2", "unittest"),
        ("case3", "parameterized"),
    ])
    def test_search(self, name, search_key):
        self.baidu_search(search_key)
        self.assertEqual(self.driver.title, search_key + "_百度搜索")

    # 参数化使用方式一 列表
    @data(["case1", "selenium"], ["case2", "ddt"], ["case3", "python"])
    @unpack
    def test_search1(self, case, search_key):
        print("第一组测试用例：", case)
        self.baidu_search(search_key)
        self.assertEqual(self.driver.title, search_key + "_百度搜索")

    # 参数化使用方式二 元组
    @data(("case1", "selenium"), ("case2", "ddt"), ("case3", "python"))
    @unpack
    def test_search2(self, case, search_key):
        print("第二组测试用例：", case)
        self.baidu_search(search_key)
        self.assertEqual(self.driver.title, search_key + "_百度搜索")

    # 参数化使用方式三 字典
    @data({"search_key": "selenium"}, {"search_key": "ddt"}, {"search_key": "python"})
    @unpack
    def test_search3(self, search_key):
        print("第三组测试用例：", search_key)
        self.baidu_search(search_key)
        self.assertEqual(self.driver.title, search_key + "_百度搜索")

    # 参数化读取 JSON 文件
    @file_data('ddt_data_file.json')
    def test_search4(self, search_key):
        print("第四组测试用例：", search_key)
        self.baidu_search(search_key)
        self.assertEqual(self.driver.title, search_key + "_百度搜索")

    # 参数化读取 YML 文件
    @file_data('ddt_data_file.yaml')
    def test_search5(self, case):
        search_key = case[0]["search_key"]
        print("第五组测试用例：", search_key)
        self.baidu_search(search_key)
        self.assertEqual(self.driver.title, search_key + "_百度搜索")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == '__main__':
    unittest.main(verbosity=2)
