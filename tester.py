from django.shortcuts import render
import feedparser
from bs4 import BeautifulSoup
import requests
from models import *

# Create your views here.


def news_parse():
	name_list = ['tesla', 'snap', 'cocacola']

	for name in name_list:
	    news_url= "https://news.google.com/news?q="+name+"&output=rss"


	    feed = feedparser.parse(news_url)['entries']

	    print(name)
	    print(' ')

	    print('Length is ' + str(len(feed)))
	    for feed_bit in feed:
	        print(feed_bit['title'])
	        print(feed_bit['link'])
	        print(feed_bit['summary_detail']['value'])

	        print(' ')

	    print(' ')


def tweet_parse():
	name_list=['tferriss']
	for name in name_list:
		url = 'https://twitrss.me/twitter_user_to_rss/?user='+name
		soup = requests.get(url).content
		# feed = feedparser.parse(url)
		# print(soup2)
		x=BeautifulSoup(soup,'html.parser')
		
		# z=0
		for item in x.findAll('item'):
			title=item.title.string
			if 'life' in title or 'Life' in title: 
				print(item.title.string)
				print(item.pubdate.string)
				date=item.pubdate.string
				print(item.link.string)
				link=item.link.string
				author=item.findAll('dc:creator')
				print(author[0].string)
			else:
				pass
				# print('nothing')
			# print(y.creator)
			# if item.name=='dc:creator':
				# print(item.string)
				# pass
			# else:
				# pass
				# if ' media' in str(y):
				# 	# print(y.string)
				# 	pass
				# else:
				# 	pass
		# print(z)
tweet_parse()