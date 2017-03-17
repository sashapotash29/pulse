from parser import news_parse
from tweet_parse import tweet_parse

news_parse.delay()
tweet_parse.delay()
