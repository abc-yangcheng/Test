'''常用的Python代码片段'''
'''（1）交换两个变量的值'''
# 一行代码搞定交换两个变量的值
num_1, num_2 = num_2, num_1

'''（2）查找对象使用的内存占用大小'''
import sys
slogan = "今天你学python了么？"
size = sys.getsizeof(slogan)

'''（3）反转字符串'''
slogan = "今天你学习python了么？"
# 一行代码搞定字符串的反转
new_slogan = slogan[::-1]

'''（4）将字符串列表合并为单个字符串'''
slogan = ["今", "天", "你", "学", "python", "了", "么", "？"]
# 一行代码搞定将字符串列表合并为单个字符串
real_slogan = "".join(slogan)

'''（5）查找存在于两个列表中任一列表存在的元素'''
# 定义一个函数用来查找存在于两个列表中任一列表存在的元素
def union(list1, list2):
    return list(set(list1 + list2))

'''（6）统计列表中元素的频率'''
from collections import Counter
numbers = [1, 1, 3, 2, 4, 4, 3, 6]
# 一行代码搞定求列表中每个元素出现的频率
count = Counter(numbers)

'''（7）判断字符串所含元素是否相同'''
from collections import Counter
course = "python"
new_course = "ypthon"
count_1, count_2 = Counter(course), Counter(new_course)
if count_1 == count_2:
    print("两个字符串所含元素相同！")

'''（8）使用enumerate()函数来获取索引-数值对'''
string = "python"
for index, value in enumerate(string):
    print(index, value)

'''（9）字典的合并'''
info_1 = {"apple": 13, "orange": 22}
info_2 = {"爆款写作": 48, "跃迁": 49}
# 一行代码搞定合并两个字典
new_info = {**info_1, **info_2}

'''（10）判断列表中元素的唯一性'''
# 定义一个函数判断列表中元素的唯一性
def is_unique(list):
    if len(list) == len(set(list)):
        return True
    else:
        return False

'''（11）列出当前目录下的所有文件和目录名'''
import os
files = [file for file in os.listdir(".")]

'''（12）把原字典的键值对颠倒并生产新的字典'''
dict_1 = {1: "python", 2: "java"}
new_dict = {value:key for key, value in dict_1.items()}

'''（13）随机生成验证码，调用随机模块'''
import random, string
str_1 = "0123456789"
# str_2 是包含所有字母的字符串
str_2 = string.ascii_letters
str_3 = str_1 + str_2
# 多个字符中选取特定数量的字符
verify_code = random.sample(str_3, 6)
# 使用join方法拼接转换为字符串
verify_code = "".join(verify_code)