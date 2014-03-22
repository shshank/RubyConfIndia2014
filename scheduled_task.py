import logging
import redis
import time
from apscheduler.scheduler import Scheduler

import process_tweet
import config
import twitter_wrapper

logging.basicConfig()

redis_client = redis.Redis(config.redis_server)


def run():
    search_results = twitter_wrapper.search(word=config.hashtag, since_id=int(redis_client.get('last_tweet_id')))
    print 'Fetched %s tweets'%len(search_results)
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

        redis_client.set('last_tweet_id', item.id)
        redis_client.set('last_updated_at', int(time.time()))


scheduler = Scheduler()
@scheduler.interval_schedule(seconds=200)
def startJob():
    run()

startJob()
scheduler.start()
while True:
    pass