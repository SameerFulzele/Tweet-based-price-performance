import tweepy
import pandas as pd

def get_tweets(consumer_key, consumer_secret, access_token, access_token_secret, \
    user_id, context):
    
    # Authorize our Twitter credentials
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    all_tweets = []

    #todo get id of last tweet of user
    oldest_id = '123'

    while True:
        tweets = api.user_timeline(screen_name=user_id, 
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = False,
                            max_id = oldest_id - 1,
                            # Necessary to keep full_text 
                            # otherwise only the first 140 words are extracted
                            tweet_mode = 'extended',
                            exclude_replies = False,
                            )
        if len(tweets) == 0:
            break
        oldest_id = tweets[-1].id
        all_tweets.extend(tweets)
        print(len(all_tweets),'tweets till now')

    tweet_list = [[tweet.id_str, 
            tweet.created_at, 
            tweet.favorite_count, 
            tweet.retweet_count, 
            tweet.full_text.encode("utf-8").decode("utf-8")] 
            for idx,tweet in enumerate(all_tweets)]
    df_all_tweets = pd.DataFrame(tweet_list,\
        columns=["id","created_at","favorite_count","retweet_count", "text"])

    df_filtered = _filter_tweets(df_all_tweets, context)
    df = _get_details(df_filtered)

    return df


def _filter_tweets(df_all_tweets,context):
    """
    This function will run a word search algorithm on all the tweets using the context 
    & filter out unnessary tweets
    """
    return df_all_tweets


def _get_details(df_filtered):
    """
    This function will get the focused coin name and token in each tweet
    & will also learn the sentiment if there is any
    It will also group the tweets based on individual coin
    """
    return df_filtered
