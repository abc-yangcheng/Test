# -*- coding:utf-8 -*-

# @Time: 2024/1/11 10:31
# @Project: test
# @File: main.py
# @Author: WSM
import pytest


def inc(x):
    return x + 1


# 测试文件和测试函数必须以“test”开头
def test_answer():
    assert inc(3) == 5


if __name__ == '__main__':
    pytest.main()
