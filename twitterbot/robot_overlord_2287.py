#Created by Sophia Evans (https://github.com/scevans83/Robot_Overlord_2287)

import tweepy
import time

from keys import *

print('')
print('')
print('starting up...', flush=True)
#time.sleep(2)
print('starting up...', flush=True)
#time.sleep(2)
print('')
print('bringing twitterbot "Robot Overlord 2287" online...', flush=True)
#time.sleep(0.8)
print('twitterbot "Robot Overlord 2287" now online', flush=True)
#time.sleep(1)
print('')
print('beginning search through @robot_2287 mentions...', flush=True)
#time.sleep(2)
print('')


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

client = tweepy.Client(consumer_key=CONSUMER_KEY,
                       consumer_secret=CONSUMER_SECRET,
                       access_token=ACCESS_KEY,
                       access_token_secret=ACCESS_SECRET)

counter = 0

FILE_NAME = 'last_tweet.txt'



def retrieve_last_tweet(file_name):
    f_read = open(file_name, 'r')
    last_tweet = int(f_read.read().strip())
    f_read.close()
    return last_tweet

def store_last_tweet(last_tweet, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_tweet))
    f_write.close()
    return

def reply_to_tweets():
    # 1578484349825318912
    last_tweet = retrieve_last_tweet(FILE_NAME)
    mentions = client.get_users_mentions(id=1094749359495888897, expansions='author_id', since_id=last_tweet, user_auth=True)
    if mentions:
        for mention in mentions.data:
                last_tweet = mention['id']
                store_last_tweet(last_tweet, FILE_NAME)
                if '#robotoverlord' in mention['text']:
                    user1id = mention['author_id']
                    user1 = client.get_user(id=user1id,user_auth=True)
                    user1username = user1.data['username']
                    print('')
                    print(user1)
                    print('')
                    print('found (1) matching tweet from @' + user1username, flush=True)
                    time.sleep(0.5)
                    print('')
                    print(str(mention['id']) + ' - ' + mention['text'], flush=True)
                    time.sleep(1)
                    print('')
                    print('generating response...', flush=True)
                    response = '@' + user1username + ' This is an automated response from your friendly Robot Overlord #2287'
                    client.create_tweet(text=response, in_reply_to_tweet_id=mention['id'])
                    print('response successfully transmitted', flush=True)
                    time.sleep(1)
                    print('')

while True:
    if counter <= 1:
        print('searching for matching tweets...', flush=True)
        reply_to_tweets()
        time.sleep(5)
        counter = counter + 1
    else:
        print('')
        print('process completed. going offline')
        print('')
        print('')
        time.sleep(2)
        #print('shutting down...')
        break