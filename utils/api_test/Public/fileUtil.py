# -*- coding: utf-8 -*-

# @Project : apiTest
# @File    : fileUtil.py
# @Date    : 2019-12-01
# @Author  : hutong
# @Describe: 微信公众： 大话性能

import os

class FileOperate():


    base_path = r'E:\download\generator\result'

    #依次读取特定目录下的所有文件
    def readFiles(self):
        files = os.listdir(FileOperate.base_path)
        files.sort(key=lambda x: int(x.split('.')[0]))
        for path in files:
            full_path = os.path.join(FileOperate.base_path, path)
            # print(full_path)
            with open(full_path) as fp:
                data = fp.read()
                print(data)




if __name__ == "__main__":
    pass
