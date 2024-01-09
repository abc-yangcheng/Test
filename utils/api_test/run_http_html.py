# -*- coding: utf-8 -*-

# @Project : apiTest
# @File    : requestsClient.py
# @Date    : 2019-11-30
# @Author  : hutong
# @Describe: 微信公众： 大话性能

import os,datetime,time
from testCase.httpcase import test_interface
from Public.py_html import createHtml
from logUtil.mylog import Log
from excelUtil.myexcel import OperateExcel
from config.configAll import Config
import subprocess

mylogger = Log(__name__).getlogger()

'''执行测试的主要文件'''
def test_create(casefilename):
    starttime=datetime.datetime.now()
    day= time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
    case_path = Config.case_path
    if not os.path.exists(case_path):
        # os.system(r'touch %s' % filepath)
        subprocess.run("mkdir -p {}".format(case_path), shell=True)
    testcase_file = case_path + casefilename
    data_list = OperateExcel(testcase_file, Config.sheet_name).read_all_data_line_by_line()
    list_id = []
    list_name = []
    list_params = []
    list_url = []
    list_type = []
    list_expect = []
    size = len(data_list)
    for i in range(size):
        data = data_list[i]
        params = data.get('请求数据')
        url = data.get('url')
        request_type = data.get('请求方式')
        expect_result = data.get('期望值')
        id = data.get('用例ID')
        name = data.get('用例名')
        list_id.append(id)
        list_name.append(name)
        list_params.append(params)
        list_url.append(url)
        list_type.append(request_type)
        list_expect.append(expect_result)

    list_result, fail_num, pass_num, list_json = test_interface(casefilename)
    filepath = Config.html_path + '{}_result.html'.format(day)

    if not os.path.exists(filepath):
        #os.system(r'touch %s' % filepath)
        subprocess.run("touch {}".format(filepath), shell=True)
    endtime=datetime.datetime.now()

    createHtml(titles=u'http接口自动化测试报告',filepath=filepath,starttime=starttime,
               endtime=endtime,pass_num=pass_num,fail_num=fail_num,
               id=list_id,name=list_name,content=list_params,url=list_url,method=list_type,
               yuqi=list_expect,json=list_json,results=list_result)

    #content = u'http接口自动化测试完成，测试通过:%s,测试失败：%s，详情见：%s' % (
    #list_pass, list_fail, filepath)
    #send_email(content=content)

if __name__ == '__main__':
    test_create('httpcase.xlsx')