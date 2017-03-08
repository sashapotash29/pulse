from django.shortcuts import render
# from django.db import transactions
import feedparser
from bs4 import BeautifulSoup
import requests
from datetime import datetime, date, timedelta
from django.shortcuts import render
import json
import time
from celery import Celery

app = Celery('tasks', backend='amqp', broker='amqp://localhost:5672/')

# from models import *

# Create your views here.


def news_parse():
	news_counter = 0
	name_list = ['tesla', 'snap', 'cocacola']

	for name in name_list:
	    news_url= "https://news.google.com/news?q="+name+"&output=rss"


	    news_feed = requests.get(news_url).content

	    news_soup = BeautifulSoup(news_feed,'html.parser')
	    # print(news_soup)
	    for item in news_soup.findAll():
	    	print(item)
	    	# x = item.title.string
	    	# y = x.split(' - ')
	    	# z = len(y)
	    	# title = y[0]
	    	# author = y[z-1]
	    	# if z>2:
	    	# 	author = y[1] + ' ' + y[2]
	    	# print(title)
	    	# print(author)
	    	# print(item.title.string.split(' - '))
	    	# print("^^=======================^^")
	    	# news_title = item.title.string
	    	# print(news_title)
	    	# news_link = item.link.string
	    	# print(news_link)
	    	# news_date = item.pubdate.string
	    	# date_news = ''
	    	# for index in range(5, len(news_date)):
	    	# 	date_news += news_date[index]

	    	# datetime_object = datetime.strptime(date_news, '%d %b %Y %H:%M:%S %Z')
	    	# print(datetime_object)
	    	# print("**=======================**")




@app.task
def news_parse():
	while True:
		print('news parse started')
		news_counter = 0
		name_list = ['tesla', 'snap', 'cocacola']
		final_obj={}
		data_list=[]
		for name in name_list:
		    news_url= "https://news.google.com/news?q="+name+"&output=rss"


		    news_feed = requests.get(news_url).content

		    news_soup = BeautifulSoup(news_feed,'html.parser')
		    for item in news_soup.findAll('item'):
		    	
		    	news_date = item.pubdate.string
		    	print(news_date)
		    	
		    	news_date = news_date[5:len(news_date)]
		    	print(news_date)
		    	
		    	date_time_object=datetime.strptime(news_date, '%d %b %Y %H:%M:%S %Z')
		    	# print(date_news)
		    	
		    	today=datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
		    	date_object=datetime.strptime(news_date, '%d %b %Y %H:%M:%S %Z').replace(hour=0, minute=0, second=0, microsecond=0)
		    	print(date_object)
		    	if today == date_object:
		    		print('yes')
		    		
			    	# print("^^=======================^^")
			    	soup_title = item.title.string
			    	title_list = soup_title.split(' - ')
			    	list_len = len(title_list)
			    	title = title_list[0]
			    	author = title_list[list_len-1]
			    	if list_len>2:
			    		author = title_list[1] + ' ' + title_list[2]
			    	# print(title)
			    	# print(author)
			    	news_title = item.title.string
			    	data={'company':name, 'source':'News', 'link' : str(item.link.string),
			    	'author' : author, 'title' : title, 'content' : str(item.description.string),
			    	'date_pub' : str(date_time_object), 'key_word' : name}
			    	# print(data)
			    	data_list.append(data)
			    	# print(data_list)
		final_obj['result']=data_list
		# print(final_obj)
		data=json.dumps(final_obj)

		print(data)
		r = requests.post('http://127.0.0.1:8000/newsfeed',data=data)
		print(r.status_code, r.reason)
		time.sleep(86400)
			    	
	    	


@app.task
def tweet_parse():
	while True:
		print('tweet parse started')
		tweet_counter = 0
		tweeters_list=['WarrenBuffet','Carl_C_Icahn', 'ReformedBroker',
		 'Schuldensuehner', 'katie_martin_fx', 'StockCats', 'KevinBCook', 
		 'TheStalwart', 'ZacksResearch','John_Hempton', 'pkedrosky','GoldmanSachs', 
		 'EddyElfenbein', 'ritholtz', 'howardlindzon', 'EnisTaner', 'IvantheK', 'mebfaber',
		 'dvolatility', 'AswathDamodaran', 'RyanDetrick', 'zerohedge', 'sspencer_smb','JohnArnoldFndtn',
		 'richardbranson','realDonaldTrump','JeffBezos','fredwilson','carlquintanilla','IamSimonHhill',
		 'davidfaber','Kyle_L_Wiggers','steveliesman','GoogleTrends']
		data_list=[]
		final_obj={}

		for tweeter in tweeters_list:
			url = 'https://twitrss.me/twitter_user_to_rss/?user='+tweeter
			soup = requests.get(url).content
			if soup == None:
				print("Something Broke...")
				pass
			else:
				tweet_soup = BeautifulSoup(soup,'html.parser')
				# ITERATE THROUGH TWEET OBJECTS
				for item in tweet_soup.findAll('item'):
					# print('item')
					# print(item)
					tweet_datetime=item.pubdate.string
					tweet_datetime = tweet_datetime[5:len(tweet_datetime)-6]
					# print('tweet_datetime')
					# print(tweet_datetime)
					
					date_time_object=datetime.strptime(tweet_datetime, '%d %b %Y %H:%M:%S')
					# print('date_time_object')
					# print(date_time_object)
					
					# print(date_news)
					now = datetime.utcnow()
					# now=datetime.strptime(now, '%d %b %Y %H:%M:%S %z')
					compare=now-timedelta(minutes=10)
					# print('now')
					# print(now)
					# print ('compare')
					# print (compare)
				
					if date_time_object>=compare:
						print('yes')
						# print(date_time_object)
						# if item.date_pub==0:
					# 	pass
					
						title=item.title.string
						if 'Tesla' in title or 'tesla' in title: 
							print('TESLA')
							print(item.title.string)
							print(item.pubdate.string)
							date=item.pubdate.string
							# print(item.link.string)
							link=item.link.string
							author=item.findAll('dc:creator')
							# print(author[0].string)
							tweet_counter +=1
							# print(item.link.string)

							data={'company':'tesla', 'source':'Twitter', 'link' : str(item.link.string),
							'author' : author, 'title' : title, 'content' : title,
							'date_pub' : str(date_time_object), 'key_word' : 'Tesla, tesla'}
							print(data)
							data_list.append(data)
						if 'coke' in title or 'coca' in title or 'Coca' in title:
							print('COCA COLA')
							print(item.title.string)
							print(item.pubdate.string)
							date=item.pubdate.string
							for index in range(5, len(news_date)):
								date_news += news_date[index]
							datetime_object = datetime.strptime(date_news, '%d %b %Y %H:%M:%S %Z')
							print(datetime_object)
							# print(item.link.string)
							link=item.link.string
							author=item.findAll('dc:creator')
							# print(author[0].string)
							tweet_counter +=1
							data={'company':'cocacola', 'source':'Twitter', 'link' : str(item.link.string),
							'author' : author, 'title' : title, 'content' : title,
							'date_pub' : str(date_time_object), 'key_word' : 'Coke, coca, Coca'}
							print(data)
							data_list.append(data)
						if 'Snap' in title or 'snap' in title:
							print('SNAPCHAT')
							print(item.title.string)
							print(item.pubdate.string)
							date=item.pubdate.string
							# print(item.link.string)
							link=item.link.string
							author=item.findAll('dc:creator')
							# print(author[0].string)
							tweet_counter +=1

							data={'company':'snap', 'source':'Twitter', 'link' : str(item.link.string),
							'author' : author, 'title' : title, 'content' : title,
							'date_pub' : str(date_time_object), 'key_word' : 'snap, Snap'}
							print(data)
							data_list.append(data)
						else:
							pass
							print(tweeter + " had nothing to offer us.")
						print(tweet_counter)
		
		final_obj['result']=data_list
		# print(final_obj)
		data=json.dumps(final_obj)
		# print(data)
		r = requests.post('http://127.0.0.1:8000/tweetfeed',data=data)
		print(r.status_code, r.reason)
		time.sleep(600)	




# FUNCTION TESTING AREA
# tweet_parse()
news_parse()





