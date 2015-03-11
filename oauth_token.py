from twython import Twython
import config

def get_oauth_token():
    tw = Twython(app_key=config.APP_KEY, app_secret=config.APP_SECRET)
    auth_props = tw.get_authentication_tokens()
    print auth_props
    oauth_token = auth_props['oauth_token']
    oauth_token_secret = auth_props['oauth_token_secret']    
    f = open('oauth_token.txt', 'w+')
    f.write(oauth_token + "\n")
    f.write(oauth_token_secret)
    f.close()
    print 'Access token successfully written to access_token.txt'

get_oauth_token()