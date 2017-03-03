from django.shortcuts import render
import feedparser
from bs4 import BeautifulSoup
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
	name_list=[]
	for name in name_list:
		url = 'https://twitrss.me/twitter_user_to_rss/?user='+name
		feed = feedparser.parse(url)
		print(feed)