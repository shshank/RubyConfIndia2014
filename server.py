import redis
import json
from flask import Flask, jsonify


import config
import twitter_wrapper

redis_client = redis.Redis(config.redis_server)


app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True

@app.route('/', methods=['GET'])
def home():
	
	response = jsonify({
						'me':{'name':'Shashank Shekhar',
								'github':'shshank',
								'twitter':'shashankssh',
								'where':'New Delhi, India'},
						'site':'UnlinkedList.com, My blog',
						'status':'Yet to go Live',
					})
	return response



@app.route('/rubyconfindia2014', methods=['GET'])
def rubyconf():
	last_known_update = redis_client.hget('cache', 'last_updated')
	if last_known_update:
		last_known_update = int(last_known_update)
	else:
		last_known_update = 0

	updated_at = int(redis_client.get('last_updated_at'))

	if last_known_update<updated_at:

		total_tweet_count = 0

		top_usernames = redis_client.zrevrange('users', 0, 10)
		top_users = [twitter_wrapper.get_user_dict(username) for username in top_usernames]
		for user in top_users: #
			user['top_words'] = list(redis_client.zrevrange('userwords_%s'%username, 0, 5))
			user['tweet_count'] = int(redis_client.zscore('users', user['username']))
			total_tweet_count += user['tweet_count']

		top_mention_usernames = redis_client.zrevrange('user_mentions', 0, 10)
		top_mention_users = [twitter_wrapper.get_user_dict(username) for username in top_mention_usernames]
		for user in top_mention_users: #
			user['mention_count'] = int(redis_client.zscore('user_mentions', user['username']))

		top_words = redis_client.zrevrange('words', 0, 10)
		top_words = [dict([(word, int(redis_client.zscore('words', word)))]) for word in top_words]

		response = json.dumps({
					'top_users':top_users,
					'top_mentions':top_mention_users,
					'top_keywords':top_words,
					'user_count':int(redis_client.zcard('users')),
					'mention_count':int(redis_client.zcard('user_mentions')),
					'keyword_count':int(redis_client.zcard('words')),
					'tweet_count':total_tweet_count,
					'updated_at': updated_at
					}, indent=4)

		redis_client.hset('cache', 'last_updated', updated_at)
		redis_client.hset('cache', 'response', response)

	else:
		response = redis_client.hget('cache', 'response')

	return jsonify(json.loads(response))

if __name__ == '__main__':
	app.run('0.0.0.0', 80)