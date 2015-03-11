from twython import Twython
import config

def get_oauth_tokens():
    # First get authentication tokens
    tw = Twython(app_key=config.APP_KEY, app_secret=config.APP_SECRET)
    auth_props = tw.get_authentication_tokens()
    oauth_token = auth_props['oauth_token']
    oauth_token_secret = auth_props['oauth_token_secret']    

    # Prompt user to find PIN by click oauth url
    print "Authorize app on ", auth_props['auth_url']
    verifier = raw_input("Enter PIN Number : ")

    # Make another twython object and get the final oauth tokens 
    # using the supplied oauth_verifier PIN
    twitter = Twython(config.APP_KEY, config.APP_SECRET,
                  oauth_token, oauth_token_secret)
    final_step = twitter.get_authorized_tokens(oauth_verifier = verifier)
    oauth_token1 = final_step['oauth_token']
    oauth_token1_secret = final_step['oauth_token_secret']

    # Write the final tokens to file
    f = open('oauth_token.txt', 'w+')
    f.write(oauth_token1 + "\n")
    f.write(oauth_token1_secret)
    f.close()
    print 'Access token successfully written to oauth_token.txt'

get_oauth_tokens()
