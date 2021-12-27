import os
from dotenv import load_dotenv
from src import base, twitter_auth, ftx_api
import pandas as pd
import datetime
import requests
import time

load_dotenv()

consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')

binance_api_key = os.getenv('binance_api_key')
binance_api_secret = os.getenv('binance_api_secret')
ftx_api_key = os.getenv('ftx_api_key')
ftx_api_secret = os.getenv('ftx_api_secret')


user_id = "binance"
context = "Binance Will List"
complete_history = True
start_time = datetime.datetime(2021, 11, 24, 0, 0, tzinfo=datetime.timezone.utc)


df_tweets = twitter_auth.get_tweets(consumer_key, consumer_secret, 
                                    access_token, access_token_secret,
                                    user_id, context, complete_history,start_time)

print(df_tweets)

base.fetch_price_from_binance(df_tweets, binance_api_key, binance_api_secret)
ftx_api.fetch_price_from_ftx(df_tweets)





