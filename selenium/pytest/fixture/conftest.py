# -*- coding:utf-8 -*-

# @Time: 2024/1/11 10:59
# @Project: test
# @File: conftest.py
# @Author: WSM
import pytest


# 设置测试钩子
@pytest.fixture()
def test_url():
    return "http://www.baidu.com"


def test_baidu(test_url):
    print(test_url)

# pytest-html 可以生成 HTML 格式的测试报告。
#  pip install pytest-html
#  pytest ./ --html=./report/result.html

# pytest-rerunfailures 可以在测试用例失败时进行重试。
#  pip install pytest-rerunfailures

# 通过“--reruns”参数设置测试用例运行失败后的重试次数。
# pytest -v test_rerunfailures.py --reruns 3

# pytest-parallel 扩展可以实现测试用例的并行运行。
#  pip install pytest-parallel

# 参数“--tests-per-worker”用来指定线程数，“auto”表示自动分配
# pytest -q test_parallel.py --tests-per-worker auto

