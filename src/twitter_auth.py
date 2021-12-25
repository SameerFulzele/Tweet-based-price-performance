import warnings
from pandas.core.common import SettingWithCopyWarning
import pandas as pd
import re
import tweepy

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

def get_tweets(consumer_key, consumer_secret, access_token, access_token_secret,
    user_id, context, complete_history):
    
    # Authorize our Twitter credentials
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    tweets = api.user_timeline(screen_name=user_id, 
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = False,
                            # Necessary to keep full_text 
                            # otherwise only the first 140 words are extracted
                            tweet_mode = 'extended'
                            )

    all_tweets = []
    all_tweets.extend(tweets)
    oldest_id = tweets[-1].id

    while complete_history:
        tweets = api.user_timeline(screen_name=user_id, 
                            count=200,
                            include_rts = False,
                            max_id = oldest_id - 1,
                            tweet_mode = 'extended',
                            exclude_replies = False,
                            )
        if len(tweets) == 0:
            break
        oldest_id = tweets[-1].id
        all_tweets.extend(tweets)
        print(f'{len(all_tweets)} tweets fetched till now')

    tweet_list = [[tweet.id_str, 
            tweet.created_at, 
            tweet.favorite_count, 
            tweet.retweet_count, 
            tweet.full_text.encode("utf-8").decode("utf-8")] 
            for idx,tweet in enumerate(all_tweets)]
    df_all_tweets = pd.DataFrame(tweet_list,\
        columns=["id","created_at","favorite_count","retweet_count", "text"])
    
    print(f' Total number of tweets fetched for the user is {len(df_all_tweets)}')
    df_all_tweets.to_csv('data/all_tweets.csv')
    df_filtered = _filter_tweets(df_all_tweets, context)
    df = _get_details(df_filtered)
    return df


def _filter_tweets(df_all_tweets,context):
    """
    This function will run a word search algorithm on all the tweets using the context 
    & filter out unnessary tweets
    """
    df_filtered = df_all_tweets[df_all_tweets['text'].str.contains(context)]
    print(f'{len(df_filtered)} number of tweets matched the context filter')
    return df_filtered


def _get_details(df_filtered):
    """
    This function will get the focused coin name and token in each tweet
    & will also learn the sentiment if there is any
    It will also group the tweets based on individual coin
    """
    df_filtered.loc[:, 'coin'] = df_filtered['text'].apply(lambda s : s[s.find('(')+1:s.find(')')])
    return df_filtered
