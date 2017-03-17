from django.shortcuts import render
# from django.utils import simplejson
from django.http import HttpResponse
import json
from .models import *
from datetime import datetime, date, timedelta
import requests
import io
import pandas as pd

# Create your views here.

##################
##### renders home page
#############

def home(request):
	return render(request, 'pulse/main.html',{})

###################
###### for graph info
################

def graphs(request):
	# print('graphsssss')
	# print(today)
	today=date.today()
	print('--------------------today')
	print(today)
	start_day = '2017-03-8'
	start=datetime.strptime(start_day, '%Y-%m-%d').date()
	print(start)
	num_days=(today-start).days
	date_list = [str(today-timedelta(days=x)) for x in range(0,num_days)]
	print(date_list)
	
	tesla_stock_data = make_stock_list('TSLA') 
	# tesla_date_list = tesla_stock_data['date_list']
	# print('\\\\\\\\\\\\\\\\tesla_date_list')
	# print(tesla_date_list)
	# tesla_hits = Hit.objects.filter(date_pub__contains=today)
	tesla_count_list=date_counter('tesla', date_list)
	# tesla_obj = {'tesla':[tesla_stock_data, tesla_count_list, tesla_date_list]}
	
	coke_stock_data = make_stock_list('Ko') 
	# coke_date_list = coke_stock_data['date_list']
	# coke_hits = Hit.objects.filter(date_pub__contains=today)
	# tesla_count=len(tesla_hits)
	coke_count_list=date_counter('cocacola', date_list)
	# print(len(tesla_hits))
	# coke_obj = {'cocacola':[coke_stock_data,coke_count_list,coke_date_list]}


	snap_stock_data = make_stock_list('SNAP') 
	# snap_date_list = snap_stock_data['date_list']
	# snap_hits = Hit.objects.filter(date_pub__contains=today)
	# tesla_count=len(tesla_hits)
	snap_count_list=date_counter('snap', date_list)
	# print(len(tesla_hits))
	# snap_obj = {'snap':[snap_stock_data,snap_count_list,snap_date_list]}

	# coke_stock_data = make_stock_list('KO') 
	# coke_date_list = coke_stock_data['date_list']
	# coke_hits = Hit.objects.filter(company='cocacola')
	# coke_count=len(tesla_hits)
	# coke_obj = {'coke':[coke_count,coke_stock_data]}
	# # print(len(coke_hits))
	
	# snap_stock_data = make_stock_list('SNAP') 
	# snap_hits = Hit.objects.filter(company='snap')
	# snap_count=len(tesla_hits)
	# snap_obj = {'snap':[snap_count,snap_stock_data]}
	# print(hits.objects)
	# print(hits)
	inner_obj = {'tesla':[tesla_stock_data, tesla_count_list, date_list],
				'coke': [coke_stock_data,coke_count_list, date_list],
				'snap': [snap_stock_data,snap_count_list, date_list]
				}
	final_obj = {'result':inner_obj}
	# final_obj = json.dumps(final_obj)
	return HttpResponse(json.dumps(final_obj))


def date_counter(name, date_list):
	count_list=[]
	# print('[[[[[[[[[[[[[]]]]]]]]]]]]]')
	# print(date_list)
	for date in date_list:
		# print('dateeeeeeeeeeeeeeeeeeeeeeeeeeee')
		# print(date)
		new_date = datetime.strptime(date, '%Y-%m-%d').date()
		hits = Hit.objects.filter(company=name, date_pub__contains=new_date)
		# print('counter hits')
		# print(hits)
		count_list.append(len(hits))
		# print('count list')
		# print(count_list)
	return count_list


def make_stock_list(tick):
	ticker = tick.upper()
	today = date.today()
	day = str(today.day)
	month = str(today.month-1)
	year = str(today.year)
	url = 'http://chart.finance.yahoo.com/table.csv?s='+ticker+'&a=2&b=1&c=2017&d='+month+'&e='+day+'&f='+year+'&g=d&ignore=.csv'
	s = requests.get(url).content
	dataframe = pd.read_csv(io.StringIO(s.decode('utf-8')))
	price_list = []
	date_list = []
	dataframe = dataframe.sort_index(axis=0, ascending=False)
	for index, row in dataframe.iterrows():
		price_list.append(row.Close)
		# print('++++++++++++++++++++++++++++++++++++++++++++++')
		# print(tick)
		# print

		date_list.append(row.Date)
	stock_product = {
			"company": ticker,
			"price_list": price_list,
			"date_list": date_list
	}
	# print('---------------------stock_product')
	# print(stock_product)
	return stock_product


#######################
######## takes news articles from scrapping and commits to db
################## 

def save_news_feed(request):
	if request.method == 'POST':
		print('feed')
		data=request.body.decode('utf-8')
		body=json.loads(data)
		# print(body)
		obj_list=body['result']
		for obj in obj_list:
			hit = Hit(
				
				company=obj['company'],
				source='News',
				link = obj['link'], 
				author = obj['author'],
				title = obj['title'],
				content = obj['content'],
				date_pub = obj['date_pub'],
				key_words = obj['company']
				)
			hit.save()
		print('news added')

		# print(request.GET)
		# print(data)

	return render(request, 'pulse/main.html',{})


##########################
########## takes tweets from scrapper and commits to db
##########################

def save_tweet_feed(request):
	if request.method == 'POST':
		print('feed')
		data=request.body.decode('utf-8')
		body=json.loads(data)
		# print(body)
		obj_list=body['result']
		for obj in obj_list:
			hit = Hit(
				
				company=obj['company'],
				source='Twitter',
				link = obj['link'], 
				author = obj['author'],
				title = obj['title'],
				content = obj['content'],
				date_pub = obj['date_pub'],
				key_words = obj['company']
				)
			hit.save()
		print('tweets added')

		# print(request.GET)
		# print(data)
	return render(request, 'pulse/main.html',{})	


def date_examples(request):
	print('example')
	data=request.GET
	print(data)
	# split = data.split('&')
	company=data['company']
	if company == 'tsla':
		company='tesla'
	if company == 'ko':
		company='cocacola'
	if company == 'snap':
		company='snap'
	print(company)
	date_len=len(data['date'])
	date2=data['date'][4:date_len-11]
	print(date2)
	date =datetime.strptime(date2, '%b %d %Y %H:%M:%S %Z').date()
	print(date)
	hits_news = Hit.objects.filter(company=company, date_pub__contains=date, source='News')
	hits_twit = Hit.objects.filter(company=company, date_pub__contains=date, source='Twitter')
	news_hit = hits_news.reverse()
	twit_hit = hits_twit.reverse()
	# print(hits[0].date_pub)
	# print(hits[4].date_pub)
	
	news_obj_list =[]
	twit_obj_list =[]
	fin_obj={}
	print('news hits')
	print(news_hit[0:5])

	for hit in news_hit:
		obj_news={}
		obj_news['company']=hit.company
		obj_news['source']=hit.source
		obj_news['link']=hit.link
		obj_news['author']=hit.author
		obj_news['title']=hit.title
		obj_news['content']=hit.content
		news_obj_list.append(obj_news)
		# print(obj_news)
	print('news hits')
	print(twit_hit)

	for hit in twit_hit:
		obj_twit={}
		obj_twit['content']=hit.content
		obj_twit['title']=hit.title
		obj_twit['author']=hit.author
		obj_twit['link']=hit.link
		obj_twit['source']=hit.source
		obj_twit['company']=hit.company
		twit_obj_list.append(obj_twit)
	# print(news_obj_list)
	fin_obj['news']=news_obj_list
	fin_obj['tweets']=twit_obj_list
	return HttpResponse(json.dumps(fin_obj))