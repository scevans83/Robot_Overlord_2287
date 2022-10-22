from pydoc import text
#import boto3
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import re
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud 
import time
from keys import *

FILE_NAME = 'last_tweet.txt'

class auth_and_fetch(object):
    '''
    Class for managing twitter api authentication and fetching of twitter requests. anything that interacts with the twitter api is contained here.
    '''
    def __init__(self):
        '''
        authentication function
        '''
        try:
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
            self.api = tweepy.API(auth)

            self.client = tweepy.Client(consumer_key=CONSUMER_KEY,consumer_secret=CONSUMER_SECRET,access_token=ACCESS_KEY,access_token_secret=ACCESS_SECRET)
            '''
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
            '''
        except:
            print("Error: Authentication Failed")
            
    def retrieve_last_tweet(self, file_name):
        f_read = open(file_name, 'r')
        last_tweet = int(f_read.read().strip())
        f_read.close()
        return last_tweet

    def store_last_tweet(self, last_tweet, file_name):
        f_write = open(file_name, 'w')
        f_write.write(str(last_tweet))
        f_write.close()
        return
    
    def get_matching_tweets(self, query):
        query = '#robotoverlord2287 -is:retweet lang:en'
        last_tweet = self.retrieve_last_tweet(FILE_NAME)
        #paginator = tweepy.Paginator(
        tweets = self.client.get_users_mentions(id=1094749359495888897, expansions='author_id', since_id=last_tweet, user_auth=True),                           # Some argument for this method
        # max_results=100,                       # How many tweets per page
        #limit=10                               # How many pages to retrieve
        #)
    
        tweet_list = []

        for tweet in tweets: #paginator.flatten(): # Total number of tweets to retrieve
            tweet_list.append(tweet)
            print(tweet)
    
    '''def reply_to_tweets(self):
        # 1578484349825318912
        last_tweet = self.retrieve_last_tweet(FILE_NAME)
        mentions = self.client.get_users_mentions(id=1094749359495888897, expansions='author_id', since_id=last_tweet, user_auth=True)
        if (mentions.data != None):
            for mention in mentions.data:
                    last_tweet = mention['id']
                    self.store_last_tweet(last_tweet, FILE_NAME)
                    if '#robotoverlord' in mention['text']:
                        user1id = mention['author_id']
                        user1 = self.client.get_user(id=user1id,user_auth=True)
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
                        self.client.create_tweet(text=response, in_reply_to_tweet_id=mention['id'])
                        print('response successfully transmitted', flush=True)
                        time.sleep(1)
                        print('')
        else: 
            time.sleep(3)
            print('no matching tweets found. please stand by.')'''

    def get_twitter_keys() -> dict:
        """Retrieve secrets from Parameter Store."""
        # Create our SSM Client.
        aws_client = boto3.client('ssm')

        # Get our keys from Parameter Store.
        parameters = aws_client.get_parameters(
            Names=[
                'twitter_api_key',
                'twitter_api_secret',
                'twitter_access_token',
                'twitter_access_secret'
            ],
            WithDecryption=True
        )

        # Convert list of parameters into simpler dict.
        keys = {}
        for parameter in parameters['Parameters']:
            keys[parameter['Name']] = parameter['Value']

        return keys

    def get_tweets(self, query, count = 10):
        '''
        function to fetch tweets and parse them into a list
        '''
        # empty list to store parsed tweets
        tweets = []
 
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search_tweets(q = query, count = count)
 
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
                
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = process_tweets.get_tweet_sentiment(process_tweets, tweet.text)
 
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            # return parsed tweets
            tweet_list_df = pd.DataFrame(tweets)
            #tweet_list_df = pd.DataFrame(tweet_list_df['text'])

            #print(tweet_list_df.head(5))
            #print('')
            return tweet_list_df
            #return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

class process_tweets(object):
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(process_tweets.clean_tweet(process_tweets, tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    
    def get_tweet_text(self, tweetlist):
        """this is a function that takes a dataframe with a list of tweets and cleans it up to return only the relevant text.

        Args:
            tweetlist (_type_): _description_
        """
        tweets=tweetlist['text'].values
 
        # Converting the text column as a single string for wordcloud
        tweet_text=str(tweets)
  
        # Converting the whole text to lowercase
        tweet_text = tweet_text.lower()
 
        # Removing the twitter usernames from tweet string
        tweet_text=re.sub(r'@\w+', ' ', tweet_text)
 
        # Removing the URLS from the tweet string
        tweet_text=re.sub(r'http\S+', ' ', tweet_text)
 
 
        # Deleting everything which is not characters
        tweet_text = re.sub(r'[^a-z A-Z]', ' ',tweet_text)
 
        # Deleting any word which is less than 3-characters mostly those are stopwords
        tweet_text = re.sub(r'\b\w{1,2}\b', '', tweet_text)
 
        # Stripping extra spaces in the text
        tweet_text= re.sub(r' +', ' ', tweet_text)
 
        return tweet_text

class analysis(object):
    def wordcloud(self, tweet_text):
        wordcloudimage = WordCloud(
                          max_words=100,
                          max_font_size=500,
                          font_step=2,
                          background_color='white',
                          width=1000,
                          height=720
                          ).generate(tweet_text)
        wordcloudimage.to_file('wordcloud.png')
        
        '''plt.figure(figsize=(15,7))
        plt.axis("off")
        #plt.imshow(wordcloudimage)
        #wordcloudimage
        #plt.show()
        plt.savefig(f'wordcloud.png',
                    dpi = 300)'''
        #return wordcloudimage



def main():
    # 1582956639547977728
    api = auth_and_fetch()
    pcs = process_tweets()
    anl = analysis() 
    last_tweet = api.retrieve_last_tweet(FILE_NAME)
    mentions = api.client.get_users_mentions(id=1094749359495888897, expansions='author_id', since_id=last_tweet, user_auth=True)
    if (mentions.data != None):
            for mention in mentions.data:
                    last_tweet = mention['id']
                    api.store_last_tweet(last_tweet, FILE_NAME)
                    if 0 == 0: #'#robotoverlord' in mention['text']:
                        user1id = mention['author_id']
                        user1 = api.client.get_user(id=user1id,user_auth=True)
                        user1username = user1.data['username']
                        print('')
                        #print(user1)
                        print('')
                        print('found (1) matching tweet from @' + user1username, flush=True)
                        time.sleep(0.5)
                        print('')
                        print(str(mention['id']) + ' - ' + mention['text'], flush=True)
                        time.sleep(1)
                        print('')
                        print('generating response...', flush=True)
                        
                        tweets = api.get_tweets(query = mention['text'].replace("@robot_2287 ",""), count = 5000)
                        tweet_text = pcs.get_tweet_text(tweets)
                        anl.wordcloud(tweet_text)
                        #print("TWEET: ", tweet)
                        
                        
                        
                        percentiments = tweets['sentiment'].value_counts(normalize=True) * 100
                        
                        # picking positive tweets from tweets
                        #ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
                        # percentage of positive tweets
                        #print("Positive tweets percentage: {} %".format(round(percentiments['positive'],2)), flush=True)
                        # picking negative tweets from tweets
                        #ntweets = [tweet for tweet in tweets if tweet[2] == 'negative']
                        # percentage of negative tweets
                        #print("Negative tweets percentage: {} %".format(round(percentiments['negative'],2)))
                        # percentage of neutral tweets
                        #print("Neutral tweets percentage: {} %".format(round(percentiments['neutral'],2)))

                        response = '@' + user1username + ' Query: "' + mention['text'].replace("@robot_2287 ","") + '" Responses were {}% \
                            '.format(round(percentiments['positive'],2)) 
                        response += 'positive, {}% '.format(round(percentiments['negative'],2))
                        response += 'negative, and {}% '.format(round(percentiments['neutral'],2)) + 'neutral.'
                            
                        if len(response) < 230: response += (' Bow down to your local Robot Overlord #2287!')

                        media = api.api.media_upload(filename="./wordcloud.png")
                        api.client.create_tweet(text=response, media_ids=[media.media_id_string], in_reply_to_tweet_id=mention['id'])
                        
                        
                        #api.client.create_tweet(text=response, in_reply_to_tweet_id=mention['id'])
                        print('response successfully transmitted', flush=True)
                        time.sleep(1)
                        print('')
                        
                        
                        '''# printing first 5 positive tweets
                        print("\n\nPositive tweets:")
                        for tweet in ptweets[:10]:
                            print(tweet[1])
                            print("-------------------")
            
                        # printing first 5 negative tweets
                        print("\n\nNegative tweets:")
                        for tweet in ntweets[:10]:
                            print(tweet[1])'''
    else: 
            time.sleep(3)
            print('no matching tweets found. please stand by.')


#def lambda_handler(event, context):  
def twitterbot(): 
    counter = 0
    #region
    print('')
    print('')
    print('starting up...', flush=True)
    time.sleep(2)
    print('starting up...', flush=True)
    time.sleep(2)
    print('')
    print('bringing twitterbot "Robot Overlord 2287" online...', flush=True)
    time.sleep(0.8)
    print('twitterbot "Robot Overlord 2287" now online', flush=True)
    time.sleep(1)
    print('')
    print('beginning search through @robot_2287 mentions...', flush=True)
    time.sleep(2)
    print('')
    #endregion
    while True:
        if counter <= 30:
            print('')
            print('searching for matching tweets...', flush=True)
            main()
            #reply_to_tweets()
            time.sleep(15)
            counter = counter + 1
        else:
            print('')
            print('process completed. going offline')
            print('')
            print('')
            time.sleep(2)
            print('shutting down...')
            break


if __name__ == "__main__":
        # calling main function
        twitterbot()
    