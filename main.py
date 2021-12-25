import os
from dotenv import load_dotenv
from src import binance_api, twitter_auth
import pandas as pd

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
complete_history = False

df_tweets = twitter_auth.get_tweets(consumer_key, consumer_secret, 
                                    access_token, access_token_secret,
                                    user_id, context, complete_history)
print(df_tweets)

df = pd.DataFrame()

for i in range(len(df_tweets)):
    df_temp = df_tweets.iloc[i, : ]
    coin = df_temp['coin']
    tweet_time = df_temp['created_at']

    # todo: need a method to find trading pair in the exchange
    coin_pair = coin + 'USDT'   

    df_hist_of_coin = binance_api.get_historical_data(
                        api_key= binance_api_key, 
                        api_secret= binance_api_secret,
                        coin_pair = coin_pair, 
                        tweet_time = str(tweet_time),
                        min_interval ='1m',
                        kline_type = 'SPOT'
                        )
    df_hist_of_coin['coin_pair'] = coin_pair
    df = df.append(df_hist_of_coin, ignore_index= True)
    
df.to_csv('data/price_data.csv',index = False)

print('Tweets and Prices data has been saved in data folder')


