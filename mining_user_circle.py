from twython import Twython
import json 
import config
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

def compute_circle(follower_ids, friend_ids):
    return list(follower_ids.union(friend_ids))

def save_circle_names(circle):
    with open('user_names.txt', 'w') as nfile:
        nfile.write('\n'.join([user['screen_name'] for user in circle]))

def save_circle_info(circle):
    #keys that can be used for analysis
    #follow_request_sent, profile_use_background_image, verified, profile_location, followers_count, statuses_count, location, following, favourites_count, time_zone, protected, status['text'] 
    pass
    
def save_circle(screen_name):
    follower_ids = set(twitter.get_followers_ids(screen_name = screen_name)['ids'])
    friend_ids = set(twitter.get_friends_ids(screen_name = screen_name)['ids'])
    circle_ids = compute_circle(follower_ids, friend_ids)
    circle = get_user_circle(circle_ids)
    save_circle_names(circle)
    save_circle_info(circle)
    

save_circle('gchandru1991')
