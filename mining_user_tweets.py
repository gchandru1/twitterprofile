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

def get_user_followers(screen_name):
    return twitter.get_followers_ids(screen_name = screen_name)
    
def get_user_friends(screen_name):
    return twitter.get_friends_ids(screen_name = screen_name)
    
def user_lookup(uid_list):
    user_details = twitter.lookup_user(user_id = uid_list)
    return user_details

subarraysize = 100

#print list of followers
follower_id_list = get_user_followers('madhuvishy')['ids']
follower_names = []
for i in range((len(follower_id_list)/subarraysize) +1):
    uid_list = follower_id_list[i*subarraysize:((i+1)*subarraysize-1)]
    follower_names.append(user_lookup(uid_list))

#print list of friends
friend_id_list = get_user_friends('madhuvishy')['ids']
friend_names = []
for i in range((len(friend_id_list)/subarraysize) +1):
    uid_list = friend_id_list[i*subarraysize:((i+1)*subarraysize-1)]
    friend_names.append(user_lookup(uid_list))


#keys that can be used for analysis
#follow_request_sent, profile_use_background_image, verified, profile_location, followers_count, statuses_count, location, following, favourites_count, time_zone, protected, status['text'] 


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
