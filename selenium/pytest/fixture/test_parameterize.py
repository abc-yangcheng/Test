# -*- coding:utf-8 -*-

# @Time: 2024/1/11 10:53
# @Project: test
# @File: test_parameterize.py
# @Author: WSM
import pytest
import math


# “base,exponent,expected”用来定义参数的名称。通过数组定义参数时，每一个元组都
# 是一条测试用例使用的测试数据。ids 参数默认为 None，用于定义测试用例的名称。
# pytest 参数化
@pytest.mark.parametrize(
    "base, exponent, expected",
    [(2, 2, 4),
     (2, 3, 8),
     (1, 9, 1),
     (0, 9, 0)],
    ids=["case1", "case2", "case3", "case4"]
)
def test_pow(base, exponent, expected):
    assert math.pow(base, exponent) == expected
