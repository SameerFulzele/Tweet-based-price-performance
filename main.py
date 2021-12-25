import os
from dotenv import load_dotenv
from src import binance_api, twitter_auth

load_dotenv()

consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')

binance_api_key = os.getenv('binance_api_key')
binance_api_secret = os.getenv('binance_api_secret')
kucoin_api_key = os.getenv('kucoin_api_key')
kucoin_api_secret = os.getenv('kucoin_api_secret')


user_id = "MadNews_io"
context = "Binance Will List"
exchange_preference = ['binance','kucoin']


# todo test the working and write other functions
# df_tweets = twitter_auth.get_tweets(consumer_key, consumer_secret, \
#                                     access_token, access_token_secret,\
#                                     user_id, context)

# for tweet in len(df_tweets):
    
#     if pair_exists:

 
df = binance_api.get_historical_data(
                    api_key= binance_api_key, 
                    api_secret= binance_api_secret,
                    coin_pair = 'XRPUSDT', 
                    tweet_time = "2021-12-24 16:17:00",
                    min_interval ='1m', 
                    kline_type = 'SPOT'
                    )
print(df.iloc[0])

