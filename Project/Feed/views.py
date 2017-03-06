from django.shortcuts import render
# from django.db import transactions
import feedparser
from bs4 import BeautifulSoup
import requests
from datetime import datetime, date, timedelta
from . import models
from .models import Hit
from django.shortcuts import render

# from models import *

# Create your views here.

# Create your views here.




def news_parse(request):
	news_counter = 0
	name_list = ['tesla', 'snap', 'cocacola']

	for name in name_list:
	    news_url= "https://news.google.com/news?q="+name+"&output=rss"


	    news_feed = requests.get(news_url).content

	    news_soup = BeautifulSoup(news_feed,'html.parser')
	    for item in news_soup.findAll('item'):
	    	news_date = item.pubdate.string
	    	
	    	news_date = news_date[5:len(news_date)]
	    	print(news_date)
	    	# print(date_news)
	    	
	    	today=datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
	    	date_object=datetime.strptime(news_date, '%d %b %Y %H:%M:%S %Z').replace(hour=0, minute=0, second=0, microsecond=0)
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
		    	Hit(company=name,source='News' ,link = item.link.string ,author = author ,title = title ,content = item.description.string ,date_pub = date_object ,key_word = name)
		    	print(Hit)
		    	# Hit.save()
		    	# print(news_title)
		    	# news_link = item.link.string
		    	# print(news_link)

	    	# print(datetime_object)
	    	# print(date_news)
	    	# print(datetime.today())
	    	# print("**=======================**")
	    	



def tweet_parse():
	tweet_counter = 0
	tweeters_list=['WarrenBuffet','Carl_C_Icahn', 'ReformedBroker',
	 'Schuldensuehner', 'katie_martin_fx', 'StockCats', 'KevinBCook', 
	 'TheStalwart', 'ZacksResearch','John_Hempton', 'pkedrosky','GoldmanSachs', 
	 'EddyElfenbein', 'ritholtz', 'howardlindzon', 'EnisTaner', 'IvantheK', 'mebfaber',
	 'dvolatility', 'AswathDamodaran', 'RyanDetrick', 'zerohedge', 'sspencer_smb']

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
				title=item.title.string
				if 'Tesla' in title or 'tesla' in title: 
					print('TESLA')
					print(item.title.string)
					print(item.pubdate.string)
					date=item.pubdate.string
					print(item.link.string)
					link=item.link.string
					author=item.findAll('dc:creator')
					print(author[0].string)
					tweet_counter +=1
				if 'coke' in title or 'coca' in title or 'Coca' in title:
					print('COCA COLA')
					print(item.title.string)
					print(item.pubdate.string)
					date=item.pubdate.string
					for index in range(5, len(news_date)):
						date_news += news_date[index]
					datetime_object = datetime.strptime(date_news, '%d %b %Y %H:%M:%S %Z')
					print(datetime_object)
					print(item.link.string)
					link=item.link.string
					author=item.findAll('dc:creator')
					print(author[0].string)
					tweet_counter +=1
				if 'Snap' in title or 'snap' in title:
					print('SNAPCHAT')
					print(item.title.string)
					print(item.pubdate.string)
					date=item.pubdate.string
					print(item.link.string)
					link=item.link.string
					author=item.findAll('dc:creator')
					print(author[0].string)
					tweet_counter +=1
				else:
					print(tweeter + " had nothing to offer us.")
		




# FUNCTION TESTING AREA
# tweet_parse()
# news_parse(request)