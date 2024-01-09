# -*- coding:utf-8 -*-

# @Time: 2024/1/8 15:12
# @Project: test
# @File: test_baidu.py.py
# @Author: WSM
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.baidu.com")
driver.find_element(By.ID, "kw").send_keys("Selenium")
driver.find_element(By.ID, "su").click()
# driver.quit()
