from django.shortcuts import render
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
	print('graphsssss')
	today=date.today()
	print(today)
	tesla_stock_data = make_stock_list('TSLA') 
	tesla_date_list = tesla_stock_data['date_list']
	tesla_hits = Hit.objects.filter(date_pub__contains=today)
	# tesla_count=len(tesla_hits)
	tesla_count=date_counter('cocacola', tesla_date_list)
	# print(len(tesla_hits))
	tesla_obj = {'tesla':[tesla_count,tesla_stock_data]}
	
	# tesla

	coke_stock_data = make_stock_list('KO') 
	coke_date_list = coke_stock_data['date_list']
	coke_hits = Hit.objects.filter(company='cocacola')
	coke_count=len(tesla_hits)
	coke_obj = {'coke':[coke_count,coke_stock_data]}
	# print(len(coke_hits))
	
	snap_stock_data = make_stock_list('SNAP') 
	snap_hits = Hit.objects.filter(company='snap')
	snap_count=len(tesla_hits)
	snap_obj = {'snap':[snap_count,snap_stock_data]}
	# print(hits.objects)
	# print(hits)
	final_obj = {'results':[tesla_obj, ] }
	final_obj
	return 

def date_counter(name, date_list):
	count_list=[]
	print('[[[[[[[[[[[[[]]]]]]]]]]]]]')
	print(date_list)
	for date in date_list:
		print('dateeeeeeeeeeeeeeeeeeeeeeeeeeee')
		print(date)
		new_date = datetime.strptime(date, '%Y-%m-%d').date()
		hits = Hit.objects.filter(company=name, date_pub__contains=new_date)
		print(hits)
		count_list.append(len(hits))
	return count_list


def make_stock_list(tick):
	ticker = tick.upper()
	today = date.today()
	day = str(today.day)
	month = str(today.month-1)
	year = str(today.year)
	url = 'http://chart.finance.yahoo.com/table.csv?s='+ticker+'&a=2&b=7&c=2017&d='+month+'&e='+day+'&f='+year+'&g=d&ignore=.csv'
	s = requests.get(url).content
	dataframe = pd.read_csv(io.StringIO(s.decode('utf-8')))
	price_list = []
	date_list = []
	dataframe = dataframe.sort_index(axis=0, ascending=False)
	for index, row in dataframe.iterrows():
		price_list.append(row.Close)
		# print('++++++++++++++++++++++++++++++++++++++++++++++')
		# print(type(row.Date))

		date_list.append(row.Date)
	stock_product = {
			"company": ticker,
			"price_list": price_list,
			"date_list": date_list
	}
	print('---------------------stock_product')
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
				source='News',
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