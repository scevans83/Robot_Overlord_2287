#Created by Sophia Evans (https://github.com/scevans83/Robot_Overlord_2287)

import time
import tweepy
import pandas as pd
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import nltk
nltk.download('vader_lexicon')

import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

from keys import *

#region
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
#endregion

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

client = tweepy.Client(consumer_key=CONSUMER_KEY,
                       consumer_secret=CONSUMER_SECRET,
                       access_token=ACCESS_KEY,
                       access_token_secret=ACCESS_SECRET)

counter = 0

FILE_NAME = 'last_tweet.txt'

def get_matching_tweets(query):
    query = '#robotoverlord2287 -is:retweet lang:en'
    last_tweet = retrieve_last_tweet(FILE_NAME)
    #paginator = tweepy.Paginator(
    tweets = client.get_users_mentions(id=1094749359495888897, expansions='author_id', since_id=last_tweet, user_auth=True),                           # Some argument for this method
       # max_results=100,                       # How many tweets per page
        #limit=10                               # How many pages to retrieve
    #)
    
    tweet_list = []

    for tweet in tweets: #paginator.flatten(): # Total number of tweets to retrieve
        tweet_list.append(tweet)
        print(tweet)
    '''    
    tweet_list_df = pd.DataFrame(tweet_list)
    tweet_list_df = pd.DataFrame(tweet_list_df['text'])
    tweet_list_df.head(5)
    
    cleaned_tweets = []

    for tweet in tweet_list_df['text']:
        cleaned_tweet = preprocess_tweet(tweet)
        cleaned_tweets.append(cleaned_tweet)

    tweet_list_df['cleaned'] = pd.DataFrame(cleaned_tweets)
    tweet_list_df.head(5)
    
    tweet_list_df[['polarity', 'subjectivity']] = tweet_list_df['cleaned'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))
    for index, row in tweet_list_df['cleaned'].iteritems():
        score = SentimentIntensityAnalyzer().polarity_scores(row)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']
        if comp <= -0.05:
            tweet_list_df.loc[index, 'sentiment'] = "negative"
        elif comp >= 0.05:
            tweet_list_df.loc[index, 'sentiment'] = "positive"
        else:
            tweet_list_df.loc[index, 'sentiment'] = "neutral"
        tweet_list_df.loc[index, 'neg'] = neg
        tweet_list_df.loc[index, 'neu'] = neu
        tweet_list_df.loc[index, 'pos'] = pos
        tweet_list_df.loc[index, 'compound'] = comp
    tweet_list_df.head(5)
'''

def preprocess_tweet(sen):
    '''Cleans text data up, leaving only 2 or more char long non-stepwords composed of A-Z & a-z only
    in lowercase'''
    
    sentence = sen.lower()

    # Remove RT
    sentence = re.sub('RT @\w+: '," ", sentence)

    # Remove special characters
    sentence = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", sentence)

    # Single character removal
    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)  # When we remove apostrophe from the word "Mark's", the apostrophe is replaced by an empty space. Hence, we are left with single character "s" that we are removing here.

    # Remove multiple spaces
    sentence = re.sub(r'\s+', ' ', sentence)  # Next, we remove all the single characters and replace it by a space which creates multiple spaces in our text. Finally, we remove the multiple spaces from our text as well.

    return sentence


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
    if (mentions.data != None):
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
    else: 
        time.sleep(3)
        print('no matching tweets found. please stand by.')
        
        
while True:
    if counter <= 1:
        print('')
        print('searching for matching tweets...', flush=True)
        get_matching_tweets('query')
        #reply_to_tweets()
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