# -*- coding: utf-8 -*-

# @Time : 2022/5/10 10:07 上午
# @Project : dataTestDemo
# @File : chartsDemo.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8

from pyecharts.charts import Line, Gauge
# 使用 options 配置项，在 pyecharts 中，一切皆 Options，进行参数设置；
import pyecharts.options as opts


# 折线图，双坐标轴，数据从Influxdb数据库中读取，描绘出TPS和响应时间曲线图
def line_chart_tps(x_list, tps_list, th95_list):
	line = Line(init_opts=opts.InitOpts(width="720px", height="350px", chart_id='2'))
	# 添加x坐标数据
	line.add_xaxis(x_list)
	line.add_yaxis("tps", tps_list, is_smooth=True, linestyle_opts=opts.LineStyleOpts(color='red', width=1))
	# 扩展右边的y轴坐标
	line.extend_axis(yaxis=opts.AxisOpts(type_="value",
										 name="响应时间",
										 name_location='middle',
										 name_gap=35,
										 position='right',
										 axislabel_opts=opts.LabelOpts(formatter="{value}")))
	line.add_yaxis("响应时间(ms)", th95_list, is_smooth=True, label_opts=opts.LabelOpts(font_size=3), yaxis_index=1)

	# 设置图表的标题、副标题、工具栏组件、坐标轴名称、位置以及距离坐标轴的距离，X轴标签旋转45度显示
	line.set_global_opts(title_opts=opts.TitleOpts(title='性能结果', pos_left='center', pos_top=5),
						 toolbox_opts=opts.ToolboxOpts(is_show=False),
						 xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
						 yaxis_opts=opts.AxisOpts(name='tps', name_location='middle', name_gap=35),
						 legend_opts=opts.LegendOpts(pos_left='center', pos_top=30)
						 )
	line.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

	return line


# 请求成功率
def gauge_success(all_requests, success_rate):
	gauge = Gauge(init_opts=opts.InitOpts(width='600px', height='400px', chart_id='5'))
	gauge.add(
		'业务指标',
		[('成功率', success_rate * 100)],
		axisline_opts=opts.AxisLineOpts(
			linestyle_opts=opts.LineStyleOpts(
				color=[(0.3, "#fd666d"), (0.7, "#D20875"), (1, "#67e0e3")], width=30
			)
		)
	)
	gauge.set_global_opts(
		title_opts=opts.TitleOpts(title='请求成功率', subtitle=str(all_requests), pos_left='center'),
		legend_opts=opts.LegendOpts(is_show=False)
	)

	return gauge


if __name__ == '__main__':
	pass
