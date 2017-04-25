from django.shortcuts import render
# from django.utils import simplejson
from django.http import HttpResponse
import json
from .models import *
from datetime import datetime, date, timedelta
import requests
import io
import pandas as pd

print('views');
# Create your views here.

##################
##### renders home page
#############

def home(request):
	print('getting home')
	return render(request, 'pulse/main.html',{})

###################
###### for graph info
################

def graphs(request):
	print('graphsssss')
	# print(today)
	date_list = make_date()
	
	tesla_stock_prod = make_stock_list('TSLA') 
	tesla_stock_data = fix_dates(date_list, tesla_stock_prod) 
	
	
	coke_stock_prod = make_stock_list('Ko') 
	coke_stock_data = fix_dates(date_list, coke_stock_prod) 
	

	snap_stock_prod = make_stock_list('SNAP') 
	snap_stock_data = fix_dates(date_list, snap_stock_prod) 
	# tesla_date_list = tesla_stock_data['date_list']
	
	date_list = [str(date) for date in date_list]
	
	tesla_count_list=date_counter('tesla', date_list)
	
	coke_count_list=date_counter('cocacola', date_list)
	
	snap_count_list=date_counter('snap', date_list)
	

	inner_obj = {'tesla':[tesla_stock_data, tesla_count_list, date_list],
				'coke': [coke_stock_data,coke_count_list, date_list],
				'snap': [snap_stock_data,snap_count_list, date_list]
				}
	final_obj = {'result':inner_obj}
	# final_obj = json.dumps(final_obj)
	print('finished graphs')
	return HttpResponse(json.dumps(final_obj))


def date_counter(name, date_list):
	count_list=[]
	# print('[[[[[[[[[[[[[]]]]]]]]]]]]]')
	# print(date_list)
	for date in date_list:
		# print('dateeeeeeeeeeeeeeeeeeeeeeeeeeee')
		# print(date)
		new_date = datetime.strptime(date, '%Y-%m-%d').date()
		hits = Hit.objects.filter(company=name, date_pub__contains=new_date).distinct('link')
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
	url = 'http://chart.finance.yahoo.com/table.csv?s='+ticker+'&a=2&b=13&c=2017&d='+month+'&e='+day+'&f='+year+'&g=d&ignore=.csv'
	print(url)
	s = requests.get(url).content
	dataframe = pd.read_csv(io.StringIO(s.decode('utf-8')))
	price_list = []
	date_list = []
	dataframe = dataframe.sort_index(axis=0, ascending=False)
	c=0
	for index, row in dataframe.iterrows():
		c+=1
		if c % 5 == 0:
			price_list.append(row.Close)
			# price_list.append(row.Close)
			# price_list.append(row.Close)
		else:
			price_list.append(row.Close)
		# print('++++++++++++++++++++++++++++++++++++++++++++++')
		# print(tick)
		date_obj = datetime.strptime(row.Date, '%Y-%m-%d').date()
		date_list.append(date_obj)

	# price_list=price_list[::-1]
	# print('date_list')
	# print(date_list)
	# print(len(date_list))
	stock_product = {
			"company": ticker,
			"price_list": price_list,
			"date_list": date_list
	}
	# print('---------------------stock_product')
	# print(price_list)
	# print(len(price_list))
	# print(stock_product)

	return stock_product


def make_date():
	today=date.today()
	# print('--------------------today')
	# print(today)
	start_day = '2017-03-12'
	start=datetime.strptime(start_day, '%Y-%m-%d').date()
	# print(start)
	num_days=(today-start).days
	date_list = [today-timedelta(days=x) for x in range(0,num_days)]
	# print('========dates')
	# print(date_list)
	# print(len(date_list))
	date_list = date_list[::-1]
	return date_list

def fix_dates(date_list, stock_product):
	
	l = len(date_list)
	l2 = len(stock_product['date_list'])
	x=l-l2
	# new_price_list=[]
	# new_date_list =[]
	i=0
	stock_product['date_list'] += x*[None] 
	print('starting while')
	while len(stock_product['price_list']) < l:
		
		if stock_product['date_list'][i] == date_list[i]:
			print('yes')
			i+=1
		else:
			print('no')
			# new_date_list.append(date_list[i])
			stock_product['price_list'].insert(i,stock_product['price_list'][i-1])
			stock_product['date_list'].insert(i,date_list[i])
	
	stock_product['date_list'] = [str(date) for date in stock_product['date_list']]	
	# date_list = [str(date) for date in date_list]	
	print(stock_product['price_list'])		
	print(stock_product)
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
