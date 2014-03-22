import redis
import json
from flask import Flask, jsonify, request, make_response

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
	response = redis_client.hget('cache', 'response')

	return jsonify(json.loads(response))

if __name__ == '__main__':
	app.run('0.0.0.0', 80)