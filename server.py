import redis
import json
from flask import Flask, jsonify, render_template

import config

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


@app.route('/rubyconfindia2014/test', methods=['GET'])
def rubyconftest():
	response = redis_client.hget('cache', 'response')
	response = json.loads(response)
	ctop_keywords = [['keywords', 'frequence of occurence']] + [[item['word'], item['count']] for item in response['top_keywords']]
	ctop_mentions = [['users', 'Number of times mentioned']] + [['@%s'%item['username'], item['mention_count']] for item in response['top_mentions']]
	ctop_users = [['users', 'Number of tweets']] + [['@%s'%item['username'], item['tweet_count']] for item in response['top_users']]
	return render_template('charts.html',
							ctop_keywords = json.dumps(ctop_keywords),
							ctop_mentions = json.dumps(ctop_mentions),
							ctop_users = json.dumps(ctop_users)
							)



@app.route('/rubyconfindia2014', methods=['GET'])
def rubyconf():
	response = redis_client.hget('cache', 'response')
	response = json.loads(response)
	print response
	return jsonify(response)

if __name__ == '__main__':
	app.run('0.0.0.0', 80)