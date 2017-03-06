from django.db import models
from django.utils import timezone

# Create your models here.


class Company(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30)
	positive_news_count = models.IntegerField(default=0)
	negative_news_count = models.IntegerField(default=0)
	total_news_count = models.IntegerField(default=0)
	positive_tweet_count = models.IntegerField(default=0)
	negative_tweet_count = models.IntegerField(default=0)
	total_tweet_count = models.IntegerField(default=0)

	def __str__(self):
		return self.name


class Hit(models.Model):
	id = models.AutoField(primary_key=True)
	company_id = models.ForeignKey(Company)
	company = models.CharField(max_length=50)
	source = models.CharField(max_length=50)
	link = models.TextField()
	author = models.CharField(max_length=100)
	title = models.TextField()
	content = models.TextField()
	date_pub = models.DateTimeField()
	key_words = models.CharField(max_length=100)

	def __strs__(self):
		return self.source