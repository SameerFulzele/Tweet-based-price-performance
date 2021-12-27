import pandas as pd
import requests
import time
from datetime import datetime


def get_historical_data(base_currency,
                        quote_currency,
                        start_time,
                        end_time,
                        min_interval,
                        ):
    endpoint_url = 'https://ftx.com/api/markets'
    request_url = f'{endpoint_url}/{base_currency}/{quote_currency}'
    # Get the historical market data as JSON
    historical = requests.get(
        f'{request_url}/candles?resolution={min_interval}&start_time={start_time}&end_time={end_time}'
    ).json()

    if not historical['success'] or len(historical['result']) == 0:
        return None
    
    df_hist = pd.DataFrame(historical['result'])

    df_hist['time'] = pd.to_datetime(df_hist['time'], unit='ms')

    df_hist = df_hist.rename(columns={
                            'open': 'open_price',
                            'high': 'high_price',
                            'low': 'low_price',
                            'close': 'close_price',})

    df_hist = df_hist[['open_price','high_price','low_price','close_price','volume','time']]

    return df_hist

        

    

def fetch_price_from_ftx(df_tweets):
    #FTX Fetch prices
    df_ftx = pd.DataFrame()
    for i in range(len(df_tweets)):
        df_temp = df_tweets.iloc[i,:]
        tweet_time = df_temp['created_at']
        base_currency = df_temp['coin']
        quote_currency = 'USD'
        
        min_interval=str(60)
        
        
        tweet_time = pd.to_datetime(tweet_time)
        start_date = datetime.timestamp(tweet_time)
        
        end_datetime = tweet_time + pd.DateOffset(hours=12)
        end_date = datetime.timestamp(end_datetime)    

        

        

        df_hist_of_coin = pd.DataFrame(historical['result'])

        
        df_hist_of_coin['coin_pair'] = base_currency + quote_currency
        print(base_currency + quote_currency,len(df_hist_of_coin))
        df_ftx = df_ftx.append(df_hist_of_coin, ignore_index= True)
    df_ftx.to_csv('data/price_data_ftx.csv',index = False)
    print('Prices data fetched from FTX has been saved in data folder')
