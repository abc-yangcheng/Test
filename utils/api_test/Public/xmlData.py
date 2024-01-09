# -*- coding: utf-8 -*-

# @Project : apiTest
# @File    : xmlData.py
# @Date    : 2019-12-12
# @Author  : hutong
# @Describe: 微信公众： 大话性能

#xml 数据

import json
import xmltodict
import re


#定义xml转json的函数
def xmltojson(xmlstr):
  #parse是的xml解析器
  xmlparse = xmltodict.parse(xmlstr)
  #json库dumps()是将dict转化成json格式，loads()是将json转化成dict格式。
  #dumps()方法的ident=1，格式化json
  jsonstr = json.dumps(xmlparse,indent=1)
  print(jsonstr)

#json转xml函数
def jsontoxml(jsonstr):
  #xmltodict库的unparse()json转xml
  xmlstr = xmltodict.unparse(jsonstr)
  print(xmlstr)

# 修改xml里的内容，利用正则表达式
def replaceContent(field):
    pattern = r'(?<=continue_forever">).*?(?=<)'
    #line = re.sub(pattern, 'false', line)
    pass


if __name__ == "__main__":
    ### 增量的资源数据xml样例
    p_rex = r'<\?[xX].*?\?>'
    xmlstr = """

<?xml version="1.0" encoding="utf-8"?>
<DataFile xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="file:///C:/Users/Administrator/Desktop/schema.xsd">  
  <FileHeader> 
    <TimeStamp>2015-01-12T04:01:00</TimeStamp>  
    <TimeZone>UTC+8</TimeZone>  
    <VendorName>HW</VendorName>  
    <ElementType>PTN</ElementType>  
    <CmVersion>V1.0.0</CmVersion> 
  </FileHeader>  
  <Objects> 
    <ObjectType>NEL</ObjectType>  
    <FieldName> 
      <N i="1">nativeName</N>  
      <N i="2">location</N>  
      <N i="3">productName</N>  
      <N i="4">vendor</N>  
      <N i="5">reality</N>  
      <N i="6">IPAddress</N>  
      <N i="7">controlPlaneIP</N>  
      <N i="8">hardwareVersion</N>  
      <N i="9">softwareVersion</N>  
      <N i="10">maxCapacity</N>  
      <N i="11">state</N> 
    </FieldName>  
    <FieldValue> 
      <Object rmUID="1101HWCSANEL89a2536c60b67c99" OperationType="1"> 
        <V i="1">NE-41</V>  
        <V i="2">Beijing China</V>  
        <V i="3">OptiX PTN 905E</V>  
        <V i="4">HW</V>  
        <V i="5">real</V>  
        <V i="6">190.107.6.41</V>  
        <V i="7">--</V>  
        <V i="8">--</V>  
        <V i="9">V100R010C00</V>  
        <V i="10">--</V>  
        <V i="11">unavailable</V> 
      </Object>  
      <Object rmUID="1101HWCSANEL89a2536c60b67c9" OperationType="3"> 
        <V i="1">NE-42</V>  
        <V i="2">--</V>  
        <V i="3">--</V>  
        <V i="4">--</V>  
        <V i="5">--</V>  
        <V i="6">--</V>  
        <V i="7">--</V>  
        <V i="8">--</V>  
        <V i="9">--</V>  
        <V i="10">--</V>  
        <V i="11">--</V> 
      </Object> 
    </FieldValue> 
  </Objects> 
</DataFile>
    """

    #out  = re.search(p_rex,xmlstr)
    xmlstr = re.sub(p_rex,'',xmlstr) #删除xml的<?xml version="1.0" encoding="utf-8"?>

    xmltojson(xmlstr)