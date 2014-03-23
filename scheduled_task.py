import logging
import redis
import time
import json
from apscheduler.scheduler import Scheduler

import process_tweet
import config
import twitter_wrapper

logging.basicConfig()

redis_client = redis.Redis(config.redis_server)

redis_client.flushall()
redis_client.set('last_tweet_id', config.first_tweet_id)

repeat_time = 60

def run():
    global repeat_time

    search_results = twitter_wrapper.search(word=config.hashtag, since_id=int(redis_client.get('last_tweet_id')))
    print 'Fetched %s tweets'%len(search_results)
    tweet_ids = []
    for item in search_results:
        username = item.user.screen_name

        redis_client.zincrby('users', username, 1)
        redis_client.rpush('usertweets_%s'%username, item.id)
        for user in item.user_mentions:
            redis_client.zincrby('user_mentions', user.screen_name, 1)


        keywords = process_tweet.getFeatureVector(item.GetText())

        [[redis_client.zincrby('userwords_%s'%username, keyword, 1),
            redis_client.rpush('wordtweets_%s'%keyword, item.id), 
            redis_client.zincrby('words', keyword, 1)] for keyword in keywords]
        tweet_ids.append(item.id)

    redis_client.set('last_updated_at', int(time.time()))

    print len(tweet_ids), len(list(set(tweet_ids)))
    redis_client.set('last_tweet_id', max(tweet_ids))

def cache_response():
    updated_at = int(redis_client.get('last_updated_at'))

    total_tweet_count = 0

    top_usernames = redis_client.zrevrange('users', 0, 9)
    top_users = [twitter_wrapper.get_user_dict(username) for username in top_usernames]
    for user in top_users: #
        user['top_words'] = list(redis_client.zrevrange('userwords_%s'%user['username'], 0, 5))
        user['tweet_count'] = int(redis_client.zscore('users', user['username']))
        total_tweet_count += user['tweet_count']


    top_mention_usernames = redis_client.zrevrange('user_mentions', 0, 9)
    top_mention_users = [twitter_wrapper.get_user_dict(username) for username in top_mention_usernames]
    for user in top_mention_users: #
        user['mention_count'] = int(redis_client.zscore('user_mentions', user['username']))

    top_words = redis_client.zrevrange('words', 0, 9)
    top_words = [dict([('word', word), ('count', int(redis_client.zscore('words', word)))]) for word in top_words]

    response = json.dumps({
                'top_users':top_users,
                'top_mentions':top_mention_users,
                'top_keywords':top_words,
                'user_count':int(redis_client.zcard('users')),
                'mention_count':int(redis_client.zcard('user_mentions')),
                'keyword_count':int(redis_client.zcard('words')),
                'tweet_count':total_tweet_count,
                'updated_at': updated_at,
                'status': 1
                }, indent=4)

    redis_client.hset('cache', 'last_updated', updated_at)
    redis_client.hset('cache', 'response', response)


scheduler = Scheduler()
@scheduler.interval_schedule(seconds=repeat_time)
def startJob():
    run()
    cache_response()

startJob()
scheduler.start()
while True:
    pass