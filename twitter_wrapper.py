import twitter
import keys

api = twitter.Api(access_token_secret = keys.access_token_secret,
                access_token_key = keys.access_token_key,
                consumer_secret = keys.consumer_secret,
                consumer_key = keys.consumer_key)

def search(word, since_id):
	print word,since_id
	return api.GetSearch(word, since_id=since_id, count=100, result_type='recent')

def get_tweet(tweet_id):
	return api.GetStatus(tweet_id)

def get_user_dict(screen_name):
	user = api.GetUser(screen_name=screen_name)
	return {'username':user.screen_name, 'name':user.GetName(), 'profile_image':user.GetProfileImageUrl()}
