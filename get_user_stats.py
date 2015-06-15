from nltk import *
from pandas import *
from nltk.tokenize import RegexpTokenizer
import json
from pprint import pprint


def pretty_print(d):
    print json.dumps(d, indent = 4)

def lexical_diversity(text):
	return float(len(set(text)))/len(text)

def analyse_text(tweet):
	tweet_token = word_tokenize(tweet["text"])
	tweet_text = Text(tweet_token)
	fdist = FreqDist(tweet_text)
	counthashtag = fdist['#']	#1
	countmentions = fdist['@']	#2
	noofwords = len(tweet_text)	#3
	noofchars = len(tweet["text"]) #4
	is_link = (tweet["entities"]["urls"] != []) * 1 #5
	favcount = tweet["favorite_count"] if tweet["text"][:2] != 'RT' else 0 #6
	rtcount = tweet["retweet_count"] if tweet["text"][:2] != 'RT' else 0 #7
	lex_diversity = lexical_diversity(tweet_text) #8
	return [tweet["user"].get("screen_name"), 
			counthashtag, countmentions, noofwords, noofchars,
			is_link, favcount, rtcount, lex_diversity]


def get_user_stats(tweets):
	column_names = ['user', 'counthastag', 'countmentions',
					'noofwords', 'noofchars', 'is_link', 'favcount',
					'rtcount', 'lex_diversity']
	user_collated = DataFrame(columns=column_names)
	for i, tweet in enumerate(tweets):
		count_values = analyse_text(tweet)
		user_collated.loc[i] = count_values
	user_grouped = user_collated.groupby(['user'])
	user_grouped_values = user_grouped.mean().iloc[0].values.tolist()
	user_lvl_list = [tweets[0]["user"].get("screen_name")]
	user_lvl_list.extend(user_grouped_values)
	user_lvl_list.extend([len(user_collated)])
	return user_lvl_list

def collate_user_stats():
	column_names = ['user', 'avghastagscount', 'avgmentioncount',
					'avgwordcount', 'avgcharcount', 'avglinkcount', 
					'avgfavcount', 'avgrtcount', 'lex_diversity', 
					'tweetcount']
	all_circle_stats = DataFrame(columns=column_names)
	with open('/Users/Chandru/Documents/projects/twitterprofile/all_circle_tweets.json') as tfile:
		data = json.load(tfile)
	for user, tweets in data.iteritems():
		try:
			stats  = dict(zip(column_names, get_user_stats(tweets)))
			all_circle_stats = all_circle_stats.append(stats, ignore_index=True)
		except Exception as e:
			print "No tweets for " + user + " in file"
	print all_circle_stats

collate_user_stats()











