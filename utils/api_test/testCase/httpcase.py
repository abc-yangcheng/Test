# -*- coding: utf-8 -*-

# @Project : apiTest
# @File    : httpcase.py
# @Date    : 2019-11-29
# @Author  : hutong
# @Describe: 微信公众： 大话性能

from excelUtil.myexcel import OperateExcel
from Public import requestsClient
from config.configAll import Config
import os
import subprocess
from logUtil.mylog import Log
mylogger = Log(__name__).getlogger()




def test_interface(casefilename):
    case_path = Config.case_path
    if not os.path.exists(case_path):
        # os.system(r'touch %s' % filepath)
        subprocess.run("mkdir -p {}".format(case_path), shell=True)
    testcase_file = case_path + casefilename
    data_list = OperateExcel(testcase_file, Config.sheet_name).read_all_data_line_by_line()


    pass_num = 0
    fail_num = 0
    list_json = [] #存储请求的响应结果
    list_result = [] #存储pass 或者 fail

    for i in range(len(data_list)):
        #print(data_list)
        request_data = data_list[i]
        #print(request_data, type(request_data))
        data_type = request_data.get('数据类型')
        #print('数据类型: {}',data_type)
        #print(type(data_type))
        case_id = request_data.get('用例ID')
        params = request_data.get('请求数据')
        params = params.replace("\n", "")
        url = request_data.get('url')
        request_type = request_data.get('请求方式')
        expect_result = request_data.get('期望值')
        expect_code = str(expect_result.split('=')[1])
        #print('expect_code: {}'.format(expect_code))
        #print('请求参数：{}'.format(params))
        myrequest = requestsClient.requestUtil(str(data_type)) #请求类型不同，请求头不同
        if request_type == 'POST':
            result = myrequest.post(url=url, params=params ) #返回值是dict
        if request_type == 'GET':
            result = myrequest.get(url=url, params=params)

        #print('result : {}'.format(result))
        real_result = result.get('result').get('code')
        #print(result.get('result').get('code'))
        if expect_code == str(real_result):
            mylogger.info('成功，case id {}' .format(case_id))
            list_json.append(result)
            list_result.append('pass')
            pass_num += 1

        else:
            mylogger.error('失败，case id {} ，请求参数：{}, url: {}, 数据类型：{}, 请求类型：{},错误结果：{}'.format(case_id,params,url,data_type,request_type,result))
            fail_num += 1
            list_result.append('fail')
            list_json.append(result)
    # print('list_result: {}'.format(list_result))
    # print('list_fail: {}'.format(fail_num))
    # print('list_pass: {}'.format(pass_num))
    # print('list_json: {}'.format(list_json))
    return list_result, fail_num, pass_num, list_json

if __name__ == "__main__":
    test_interface('httpcase.xlsx')