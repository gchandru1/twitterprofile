from twython import Twython
import json 
import config
import csv
PER_REQUEST_COUNT = 100

def get_oauth_tokens():
    f = open('oauth_token.txt', 'r')
    return [token.strip('\n') for token in f.readlines()]

OAUTH_TOKEN, OAUTH_TOKEN_SECRET = get_oauth_tokens()
twitter = Twython(config.APP_KEY, config.APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def pretty_print(d):
    print json.dumps(d, indent = 4)
    
def user_lookup(uid_list):
    return twitter.lookup_user(user_id = uid_list)

def get_user_circle(circle_ids):
    circle = []
    while len(circle_ids) > 0:
        uid_list = circle_ids[:PER_REQUEST_COUNT]
        circle.extend(user_lookup(uid_list))
        circle_ids = circle_ids[PER_REQUEST_COUNT:]
    return circle

def save_circle_names(circle):
    with open('user_names.txt', 'w') as nfile:
        nfile.write('\n'.join([user['screen_name'] for user in circle]))

def save_circle_info(circle):
    #keys that can be used for analysis
    #follow_request_sent, profile_use_background_image, verified, profile_location, followers_count, 
    #statuses_count, location, following, favourites_count, time_zone, protected, status['text'] 
    with open('circle_info.csv', 'w') as f:
        writer = csv.writer(f)
        for user in circle:
            user_status = user.get('status').get('text').encode('ascii', 'ignore') if user.get('status') else None
            user_location = user.get('location').encode('ascii', 'ignore')
            user_info = [user.get('screen_name'), user.get('follow_request_sent'), user.get('profile_use_background_image'),
                         user.get('verified'), user.get('profile_location'), user.get('followers_count'),
                         user.get('statuses_count'), user_location, user.get('following'),
                         user.get('favourites_count'), user.get('time_zone'), user.get('protected'),
                         user_status]
            #print user_info
            writer.writerow(user_info)
    print 'Circle info written to file'

    
def save_circle(screen_name):
    follower_ids = set(twitter.get_followers_ids(screen_name = screen_name)['ids'])
    friend_ids = set(twitter.get_friends_ids(screen_name = screen_name)['ids'])
    circle_ids = list(follower_ids.union(friend_ids))
    circle = get_user_circle(circle_ids)
    #pretty_print(circle)
    save_circle_names(circle)
    save_circle_info(circle)
    

save_circle('gchandru1991')
