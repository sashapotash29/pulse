from django.shortcuts import render
import feedparser
from bs4 import BeautifulSoup
import requests
from datetime import datetime, date, timedelta

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
news_parse()




