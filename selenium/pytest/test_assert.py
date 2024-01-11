# -*- coding:utf-8 -*-

# @Time: 2024/1/11 10:41
# @Project: test
# @File: test_assert.py
# @Author: WSM
# 功能：用于计算 a 与 b 相加的和
def add(a, b):
    return a + b


# 功能：用于判断素数
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
            return True


# 测试相等
def test_add_1():
    assert add(3, 4) == 7


# 测试不相等
def test_add_2():
    assert add(17, 22) != 50


# 测试大于或等于
def test_add_3():
    assert add(17, 22) <= 50


# 测试小于或等于
def test_add_4():
    assert add(17, 22) >= 38

    # 测试包含
    def test_in():
        a = "hello"
        b = "he"
        assert b in a

    # 测试不包含
    def test_not_in():
        a = "hello"
        b = "hi"
        assert b not in a

    # 判断是否为 True
    def test_true_1():
        assert is_prime(13)

    # 判断是否为 True
    def test_true_2():
        assert is_prime(7) is True

    # 判断是否不为 True
    def test_true_3():
        assert not is_prime(4)

    # 判断是否不为 True
    def test_true_4():
        assert is_prime(6) is not True

    # 判断是否为 False
    def test_false_1():
        assert is_prime(8) is False

# pytest -k add test_assert.py 运行名称中包含某字符串的测试用例可以
# 通过“-k”来指定在名称中包含“add”的测试用例。

# pytest -q test_assert.py 减少测试的运行冗长

# pytest -x test_fail.py 如果出现一条测试用例失败，则退出测试

# pytest ./test_dir 运行测试目录

# 生成 JUnit XML 文件
# pytest ./test_dir --junit-xml=./report/log.xml

# 生成在线测试报告
# pytest ./test_dir --pastebin=all

# 指定特定类或方法执行
# pytest test_fixtures_02.py::TestMultiply::test_numbers_5_6
