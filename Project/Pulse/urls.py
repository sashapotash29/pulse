from django.conf.urls import url
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
	url(r'^graph$',views.graphs, name="graphs"),
	url(r'^newsfeed$',csrf_exempt(views.save_news_feed), name="newsfeed"),
	url(r'^tweetfeed$',csrf_exempt(views.save_tweet_feed), name="tweetfeed"),

]