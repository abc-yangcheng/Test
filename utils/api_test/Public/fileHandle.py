# -*- coding: utf-8 -*-

# @Project : apiTest
# @File    : fileHandle.py
# @Date    : 2019-12-11
# @Author  : hutong
# @Describe: 微信公众： 大话性能


#遍历文件时想在错误消息中使用行号定位
def parse_data(filename):
    with open(filename, 'rt') as f:
        for lineno, line in enumerate(f, 1):
            fields = line.split()
            try:
                count = int(fields[1])
            except ValueError as e:
                print('Line {}: Parse error: {}'.format(lineno, e))



if __name__ == "__main__":
    pass
