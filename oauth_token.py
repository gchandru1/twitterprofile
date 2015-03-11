from twython import Twython
import config

def get_oauth_token():
    print config.APP_KEY
    tw = Twython(app_key=config.APP_KEY, app_secret=config.APP_SECRET)
    auth_props = tw.get_authentication_tokens()
    print auth_props
    oauth_token = auth_props['oauth_token']
    oauth_token_secret = auth_props['oauth_token_secret']    
    twitter = Twython(config.APP_KEY, config.APP_SECRET,
                  oauth_token, oauth_token_secret)
    final_step = twitter.get_authorized_tokens('4708586')
    oauth_token1 = final_step['oauth_token']
    oauth_token1_secret = final_step['oauth_token_secret']
    f = open('oauth_token.txt', 'w+')
    f.write(oauth_token1 + "\n")
    f.write(oauth_token1_secret)
    f.close()
    print 'Access token successfully written to oauth_token.txt'

get_oauth_token()
