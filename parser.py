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

app = Celery('parser', backend='amqp', broker='amqp://')

# from models import *

# Create your views here.

# Create your views here.



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
		    	# print(news_date)
		    	
		    	news_date = news_date[5:len(news_date)]
		    	# print(news_date)
		    	
		    	date_time_object=datetime.strptime(news_date, '%d %b %Y %H:%M:%S %Z')
		    	# print(date_news)
		    	
		    	today=datetime.utcnow()
		    	compare = today - timedelta(hours=1)
		    	print('compare')
		    	print(compare)
		    	date_object=datetime.strptime(news_date, '%d %b %Y %H:%M:%S %Z')
		    	print('date_object')
		    	print(date_object)
		    	if compare < date_object:
		    		print('time check passed')
		    		
			    	# print("^^=======================^^")
			    	soup_title = item.title.string
			    	title_list = soup_title.split(' - ')
			    	list_len = len(title_list)
			    	titles = title_list[0]
			    	title = titles.replace("&apos;","'")
			    	author = title_list[list_len-1]
			    	if list_len>2:
			    		author = title_list[1] + ' ' + title_list[2]
			    	# print(title)
			    	# print(author)
			    	news_title = item.title.string
			    	data={'company':name, 'source':'News', 'link' : str(item.link.string),
			    	'author' : author, 'title' : title, 'content' : str(item.description.string),
			    	'date_pub' : str(date_time_object), 'key_word' : name, 'source_type':'professional'}
			    	print(name + 'news found')
			    	data_list.append(data)
			    	# print(data_list)
		final_obj['result']=data_list
		# print(final_obj)
		data=json.dumps(final_obj)
		if len(data_list) > 0:
			# print(data)
			r = requests.post('http://127.0.0.1:8000/newsfeed',data=data)
			print(r.status_code, r.reason,'news finish')
		else:
			print('no news to send')
		time.sleep(3600)
			    	
	    	


@app.task
def tweet_parse():
	while True:
		start_time = datetime.now()
		print('tweet parse started')
		tweet_counter = 0
		tweeters_list=['WarrenBuffet','Carl_C_Icahn', 'ReformedBroker',
		 'Schuldensuehner', 'katie_martin_fx', 'StockCats', 'KevinBCook', 
		 'TheStalwart', 'ZacksResearch','John_Hempton', 'pkedrosky','GoldmanSachs', 
		 'EddyElfenbein', 'ritholtz', 'howardlindzon', 'EnisTaner', 'IvantheK', 'mebfaber',
		 'dvolatility', 'AswathDamodaran', 'RyanDetrick', 'zerohedge', 'sspencer_smb','JohnArnoldFndtn',
		 'richardbranson','realDonaldTrump','JeffBezos','fredwilson','carlquintanilla','IamSimonHhill',
		 'davidfaber','Kyle_L_Wiggers','steveliesman','GoogleTrends','kitjuckes', 'Lavorgnanomics', 
		 'TMTanalyst', 'DavidSchawel', 'davidjpowell24', 'TheSkeptic21', 'conorsen', 'allstarcharts', 
		 'RiskReversal', 'InterestArb', 'mark_dow', 'auaurelija', 'MarketPlunger', 'barnejek', 
		 'ericjackson', 'brianmlucey', 'fwred', 'muddywatersre', 'groditi', 'kiffmeister', 
		 'Fullcarry', 'mbusigin', 'prchovanec', 'michaelkitces','BI_Advertising', 'Stalingrad_Poor',
		  'MrScottEddy', 'FoxBusiness','businessinsider', 'markets', 'elonmusk','pulseisgood',
		  'AbnormalReturns', 'ResearchPuzzler', 'FarnamStreet', 'ZywaveFP', 'CM_eXchange', 'Reuters']
		data_list=[]
		final_obj={}
		z=0
		for tweeter in tweeters_list:
			url = 'https://twitrss.me/twitter_user_to_rss/?user='+tweeter
			soup = requests.get(url).content
			print('checking '+tweeter)
			z+=1
			print(z)
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
					compare = now-timedelta(minutes=10)
					# print('now')
					# print(now)
					# print ('compare')
					# print (compare)
				
					if date_time_object>=compare:
						print('time check good')
						# print(date_time_object)
						# if item.date_pub==0:
					# 	pass
					
						titles=item.title.string
						title=titles.replace("&apos;","'")
						if 'Tesla' in title or 'tesla' in title: 
							print('TESLA')
							print(item.title.string)
							print(item.pubdate.string)
							date=item.pubdate.string
							# print(item.link.string)
							link=item.link.string
							author=item.find('dc:creator').string
							print(author)
							tweet_counter +=1
							# print(item.link.string)

							data={'company':'tesla', 'source':'Twitter', 'link' : str(item.link.string),
							'author' : str(author), 'title' : title, 'content' : title,
							'date_pub' : str(date_time_object), 'key_word' : 'Tesla, tesla', 
							'source_type': 'professional'}
							print('tesla hit found')
							data_list.append(data)
						if 'coke' in title or 'coca' in title or 'Coca' in title:
							print('COCA COLA')
							print(item.title.string)
							print(item.pubdate.string)
							date=item.pubdate.string
							# print(item.link.string)
							link=item.link.string
							author=item.find('dc:creator').string
							print(author)
							tweet_counter +=1
							data={'company':'cocacola', 'source':'Twitter', 'link' : str(item.link.string),
							'author' : str(author), 'title' : title, 'content' : title,
							'date_pub' : str(date_time_object), 'key_word' : 'Coke, coca, Coca',
							'source_type': 'professional'}
							print('coke hit found')
							data_list.append(data)
						if 'Snap' in title or 'snap' in title:
							print('SNAPCHAT')
							print(item.title.string)
							print(item.pubdate.string)
							date=item.pubdate.string
							# print(item.link.string)
							link=item.link.string
							author=item.find('dc:creator').string
							print(author)
							tweet_counter +=1

							data={'company':'snap', 'source':'Twitter', 'link' : str(item.link.string),
							'author' : str(author), 'title' : title, 'content' : title,
							'date_pub' : str(date_time_object), 'key_word' : 'snap, Snap',
							'source_type': 'professional'}
							print('snap hit found')
							data_list.append(data)
						else:
							pass
							print(tweeter + " had nothing to offer us.")
						# print(tweet_counter)
		
		final_obj['result']=data_list
		# print(final_obj)
		if len(data_list)>0:
			data=json.dumps(final_obj)
			# print(data)
			r = requests.post('http://127.0.0.1:8000/tweetfeed',data=data)
			print(r.status_code, r.reason,'tweet finished')
		else:
			print('no tweets to add')
		finish_time = datetime.now()
		run_time = (finish_time-start_time).seconds
		# print(run_time.seconds)
		time.sleep(600-run_time)	




# FUNCTION TESTING AREA
# tweet_parse()
# news_parse()