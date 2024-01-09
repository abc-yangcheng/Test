# -*- coding: utf-8 -*-

# @Time : 2022/3/13 11:38 上午
# @Project : sqlDemo
# @File : propertyTest.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


class Student():
	def __init__(self, name, age):
		self.__name = name
		self.__age = age
	
	@property #property作用1: 方法加入@property后，这个方法相当于一个属性，这个属性可以让用户进行使用，而且用户有没办法随意修改。
	def age(self):
		return self.__age
	
	@age.setter  # property作用2：可以设置属性，另外在设置时候触发相关的验证等功能.
	def age(self, value):
		if not isinstance(value, int):
			raise ValueError("age must be a integer!")
		if value < 0 or value > 100:
			raise ValueError("age must be between 0 and 100!")
		self.__age = value


	def print_info(self):
		print('%s: %s' % (self.__name, self.__age))



if __name__ == '__main__':
	s = Student('tong',18)
	s.print_info()
	s.age=101
	s.print_info()
	
