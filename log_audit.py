from pyecharts import Bar
from pyecharts import Pie
from pyecharts import Page
import pandas as pd
import os
import datetime

list_ = []


#日志文件路径
logdir = '/apache-tomcat-7.0.88/logs'


for eachfile in os.listdir(logdir):
	logfile=os.path.join(logdir,eachfile)
	#读取日志文件到DataFrame
	reader=pd.read_table(logfile,sep=' ',engine='python',names=['ip','a','b','datetime','zone','url','code','times'] ,header=None,iterator=True)
	loop=True
	chunksize=10000000
	chunks=[]
	while loop:
		try:
			chunk=reader.get_chunk(chunksize)
			chunks.append(chunk)
		except StopIteration:
			loop=False
			print("Iteration is stopped.")
	#df dataframe
	list_.append(pd.concat(chunks))

df = pd.concat(list_)

#数据格式化处理
df['datetime'] = df['datetime'].apply(lambda x:datetime.datetime.strptime(x[1:12], '%d/%b/%Y').date())

#pandas.core.series.Series 饼图数据
df_uri_grouped = df.groupby('url').size()

df_uri_grouped_obj = df.groupby('url')[['ip']].size()



#柱状图数据
df_ip_uri_grouped = df.groupby(['ip','url']).size()

page = Page()
bar1 = Bar('多维')

for name,group in df.groupby('ip'):
	
	df_datetime_group = group.groupby('datetime').size()

	bar1.add(name,list(df_datetime_group.index),list(df_datetime_group))


page.add(bar1)


"""
attr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
v1 = [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
v2 = [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]

bar = Bar("Bar chart", "precipitation and evaporation one year")
bar.add("precipitation", attr, v1, mark_line=["average"], mark_point=["max", "min"])
bar.add("evaporation", attr, v2, mark_line=["average"], mark_point=["max", "min"])
"""
bar = Bar("Bar chart")
bar.add("test",list(df_ip_uri_grouped.index),list(df_ip_uri_grouped))
page.add(bar)

"""
bar1 = Bar("Bar chart", "precipitation and evaporation one year")
bar1.add("precipitation", attr, v1, is_stack = True)
bar1.add("evaporation", attr, v2, is_stack = True)

page.add(bar1)


attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
v1 = [11, 12, 13, 10, 10, 10]
"""
pie = Pie("饼图示例")#新建饼图示例pie

pie.add("", list(df_uri_grouped.index), list(df_uri_grouped), is_label_show=True)
#pie.show_config()#是否在命令行中显示config，此行可省略

page.add(pie)

page.render()

