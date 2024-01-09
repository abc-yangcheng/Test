# -*- coding: utf-8 -*-

# @Project : apiTest
# @File    : py_html.py
# @Date    : 2019-11-30
# @Author  : hutong
# @Describe: 微信公众： 大话性能


titles = 'api test'


def title(titles):
	title = '''<!DOCTYPE html>
<html>
<head>
	
	<meta http-equiv=Content-Type content="text/html; charset=utf-8">
	<title>%s</title>
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- 引入 Bootstrap -->
    <link href="https://cdn.bootcss.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">
    <!-- HTML5 Shim 和 Respond.js 用于让 IE8 支持 HTML5元素和媒体查询 -->
    <!-- 注意： 如果通过 file://  引入 Respond.js 文件，则该文件无法起效果 -->
    <!--[if lt IE 9]>
     <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
     <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
    <style type="text/css">
        .hidden-detail,.hidden-tr{
            display:none;
        }
    </style>
</head>
<body>
	''' % (titles)
	return title


connent = '''
<div  class='col-md-4 col-md-offset-4' style='margin-left:3%;'>
<h1>接口测试的结果</h1>'''


def shouye(starttime, endtime, pass_num, fail_num):
	summary = '''
    <table  class="table table-hover table-condensed">
            <tbody>
                <tr>
		<td><strong>开始时间:</strong> %s</td>
		</tr>
		<td><strong>结束时间:</strong> %s</td></tr>
		<td><strong>耗时:</strong> %s</td></tr>
		<td><strong>结果:</strong>
			<span >Pass: <strong >%s</strong>
			Fail: <strong >%s</strong>
			 
			    </span></td>                  
			   </tr> 
			   </tbody></table>
			   </div> ''' % (starttime, endtime, (endtime - starttime), pass_num, fail_num)
	return summary


detail = '''<div class="row " style="margin:60px">
        <div style='    margin-top: 18%;' >
        <div class="btn-group" role="group" aria-label="...">
            <button type="button" id="check-all" class="btn btn-primary">所有用例</button>
            <button type="button" id="check-success" class="btn btn-success">成功用例</button>
            <button type="button" id="check-danger" class="btn btn-danger">失败用例</button>
        </div>
        <div class="btn-group" role="group" aria-label="...">
        </div>
        <table class="table table-hover table-condensed table-bordered" style="word-wrap:break-word; word-break:break-all;  margin-top: 7px;">
		<tr >
            <td ><strong>用例ID&nbsp;</strong></td>
            <td><strong>用例名字</strong></td>
            <td><strong>请求内容</strong></td>
            <td><strong>url</strong></td>
            <td><strong>请求方式</strong></td>
            <td><strong>预期</strong></td>
            <td><strong>实际返回</strong></td>  
            <td><strong>结果</strong></td>
        </tr>
    '''


def passfail(tend):
	if tend == 'pass':
		htl = '''<td bgcolor="green">pass</td>'''
	# elif tend =='fail':
	#    htl='''<td bgcolor="fail">fail</td>'''
	# elif tend=='weizhi':
	#    htl='''<td bgcolor="red">error</td>'''
	else:
		htl = '''<td bgcolor="red">fail</td>'''
	return htl


def details(result, id, name, content, url, method, yuqi, json, relust):
	xiangqing = '''
        <tr class="case-tr %s">
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            %s
        </tr>
    ''' % (result, id, name, content, url, method, yuqi, json, passfail(relust))
	return xiangqing


weibu = '''</div></div></table><script src="https://code.jquery.com/jquery.js"></script>
<script src="https://cdn.bootcss.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
<script type="text/javascript">
	$("#check-danger").click(function(e){
	    $(".case-tr").removeClass("hidden-tr");
        $(".success").addClass("hidden-tr"); 
	});

	$("#check-success").click(function(e){
		 $(".case-tr").removeClass("hidden-tr");
         $(".danger").addClass("hidden-tr"); 
	});

	$("#check-all").click(function(e){
	    $(".case-tr").removeClass("hidden-tr");
	});
</script>
</body></html>'''


def generate(titles, starttime, endtime, pass_num, fail_num, id, name, content, url, method, yuqi, json, result):
	if type(name) == list:
		relus = ' '
		for i in range(len(name)):
			if result[i] == "pass":
				clazz = "success"
			else:
				clazz = 'danger'
			relus += (details(clazz, id[i], name[i], content[i], url[i], method[i], yuqi[i], json[i], result[i]))

		text = title(titles) + connent + shouye(starttime, endtime, pass_num, fail_num) + detail + relus + weibu
	else:
		text = title(titles) + connent + shouye(starttime, endtime, pass_num, fail_num) + detail + details(result, id,
																										   name,
																										   content, url,
																										   method, yuqi,
																										   json,
																										   result) + weibu
	return text


def createHtml(filepath, titles, starttime, endtime, pass_num, fail_num, id, name, content, url, method, yuqi, json,
			   results):
	texts = generate(titles, starttime, endtime, pass_num, fail_num, id, name, content, url, method, yuqi, json,
					 results)
	with open(filepath, 'wb') as f:
		f.write(texts.encode('utf-8'))
