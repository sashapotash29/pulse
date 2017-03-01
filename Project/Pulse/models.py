from django.db import models
from django.utils import timezone

# Create your models here.


class Company(models.Model):
	name = models.CharField(max_length=30)
	positive_count = models.IntegerField(default=0)
	negative_count = models.IntegerField(default=0)
	total_count = models.IntegerField(default=0)

	def __str__(self):
		return self.name


class Hit(models.Model):
	company = models.ForeignKey(Company)
	source = models.CharField(max_length=50)
	content = models.TextField()
	date_pub = models.DateTimeField(default=timezone.now)
	key_words = models.CharField(max_length=30)

	def __strs__(self):
		return self.source