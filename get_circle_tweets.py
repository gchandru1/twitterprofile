from twython import Twython, TwythonAuthError, TwythonRateLimitError
import json 
import config
import time

def file_to_list(filename):
    f = open(filename, 'r')
    return [line.strip('\n') for line in f.readlines()]

def get_oauth_tokens():
    return file_to_list('oauth_token.txt')

OAUTH_TOKEN, OAUTH_TOKEN_SECRET = get_oauth_tokens()
twitter = Twython(config.APP_KEY, config.APP_SECRET, 
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

#get tweets for given user
def get_user_tweets(screen_name):
    try:
        results = twitter.get_user_timeline(screen_name = screen_name, 
                                            count = 200, 
                                            exclude_replies = True ,
                                            include_rts = True)
        return [result['text'] for result in results]
    except TwythonAuthError:
        print "Tweets are protected for " + screen_name

def save_json(tweet_json):
    try:
        with open('all_circle_tweets.json') as tfile:
            saved_tweets = json.load(tfile)
    except IOError:
        saved_tweets = {}
    saved_tweets.update(tweet_json)
    with open('all_circle_tweets.json', 'w') as outfile:
        json.dump(saved_tweets, outfile)
        
def save_unames(circle_name):
    with open('user_names.txt', 'w') as nfile:
        nfile.write('\n'.join([user for user in circle_name]))


def save_tweets():
    circle_names = file_to_list('user_names.txt')
    circle_tweet_data = {}
    index_seen = 0
    try:
        for index, uname in enumerate(circle_names):
            user_tweets = get_user_tweets(uname)
            circle_tweet_data[uname] = user_tweets
            index_seen = index
    except TwythonRateLimitError:
        print 'Twitter request limit exceeded.'
        save_unames(circle_names[index_seen+1:])
        print 'User_name.txt has users from %d', (index_seen + 1)
        save_json(circle_tweet_data)
        print 'Json upto user %d saved', index_seen
        return True
    save_json(circle_tweet_data)
    open('user_names.txt', 'w').close()
    print 'All user tweets saved'
    return False

def run():
    while save_tweets():
        time.sleep(900)
    print "Done"

time.sleep(900)
run()