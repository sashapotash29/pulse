from django.shortcuts import render
import json
from .models import *
# Create your views here.

def graphs(request):
	print('graphsssss')
	hits = Hit.objects.filter(company='tesla')
	print(len(hits))
	# print(hits.objects)
	# print(hits)
	return render(request, 'pulse/main.html',{})

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


		# print(request.GET)
		# print(data)
	


	return render(request, 'pulse/main.html',{})


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


		# print(request.GET)
		# print(data)
	


	return render(request, 'pulse/main.html',{})	