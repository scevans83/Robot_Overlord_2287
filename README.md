# Robot_Overlord_2287
This is a project for EC 601.

The goal for this project was to create a twitter bot to provide a concise summary of twitter users' sentiments towards a given query. When a user tweets at the bot (@robot_2287) with their query, the bot collects the most recent 5000 tweets matching that query and determines whether each tweet is positive, negative, or neutral in sentiment. The bot then collates the text of all 5000 tweets into a single string, removes common and short words (i.e. is, a, the) and creates a wordcloud image of the 100 most-found words in that string. Finally, the bot responds to the initial tweet with the percent of tweets that fell into each sentiment category, and attaches the wordcloud image.

___

To create your own Robot Overlord:
1. clone the repository

2. create a new twitter account and a corresponding twitter developer account and project for your new Robot Overlord

3. create a file called "keys.py" in the twitterbot folder with the following structure:


      ```python
      myid = '1094749359495888897'
      CONSUMER_KEY = 'AAAAAAAAAA'
      CONSUMER_SECRET = 'BBBBBBBBBBB'
      ACCESS_KEY = 'CCCCCCCCCCCCC'
      ACCESS_SECRET = 'DDDDDDDDDDDDD'
      bearer_token = 'EEEEEEEEEEEEEE'
      ```
      Note: replace the above strings with your Robot Overlord's authentication keys from the twitter developer hub



4. replace the id in line 249 of twitterbot/auth.py with the same string you set as myid above

5. Tweet at your twitterbot from a separate account with the following structure: 
      @[your bot] query

6. in your console, navigate to the twitterbot folder and run the following (for bash/linux consoles):
      python3 auth.py
      
7. Your twitterbot will search for new mentions every 20 seconds for 30 cycles. When it finds your tweet, it will perform the analysis and respond!


## Example:

[link to tweet and response](https://twitter.com/_NodeOfRanvier_/status/1583847242964037634)

<kbd>
<img width="595" alt="example of a tweet to @robot_2287" src="https://user-images.githubusercontent.com/60391096/197348715-5e53e6dd-e8cb-4391-8f0a-5390a8ecedb8.png">
</kbd>


https://user-images.githubusercontent.com/60391096/197348744-107e60e2-386a-4e88-82fd-b24cda0b2dc6.mov

<kbd>
<img width="594" alt="response tweet from @robot_2287" src="https://user-images.githubusercontent.com/60391096/197348673-b7a7f97c-ec9b-4c63-9b49-604124ca209b.png">
</kbd>
      

      
