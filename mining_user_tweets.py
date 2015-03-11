from twython import Twython
import json 
import csv
import config

def get_oauth_tokens():
    f = open('oauth_token.txt', 'r')
    return [token.strip('\n') for token in f.readlines()]

OAUTH_TOKEN, OAUTH_TOKEN_SECRET = get_oauth_tokens()

twitter = Twython(config.APP_KEY, config.APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def pretty_print(d):
    print json.dumps(d, indent = 4)
    
#get tweets for given user
def get_user_tweets(screen_name):
    results = twitter.get_user_timeline(screen_name = screen_name)
    return results

for r in get_user_tweets('madhuvishy'):
    print r['text']

def save_tweets():
    tweets = get_user_tweets()
    # pretty_print(tweets[0])
    # text, id, favorite_count, retweeted, retweet_count, entities['hastags'][i]['text'], 
    # user['verified'], user['followers_count'], created_at , possibly_sensitive 
    with open('tweet_data.csv', 'a+') as csvfile:
        writer = csv.writer(csvfile)
        for t in tweets:
            hashtags = [tag['text'] for tag in t['entities']['hashtags']]
            text = t['text'].encode('ascii', 'ignore')
            csvdata = [t['id'], text, t['favorite_count'], t['retweeted'],
                       t['retweet_count'], t['user']['verified'], t['user']['followers_count'], 
                       t['created_at'] , t.get('possibly_sensitive'), '|'.join(hashtags)]
            writer.writerow(csvdata)
