from src import binance_api, ftx_api
import pandas as pd
from datetime import datetime
import re

def fetch_price_from_binance(df_tweets,binance_api_key,binance_api_secret):
    df_binance = pd.DataFrame()

    for i in range(len(df_tweets)):
        df_temp = df_tweets.iloc[i, : ]
        coin = df_temp['coin']
        tweet_time = df_temp['created_at']

        start_datetime = pd.to_datetime(tweet_time)

        # I am fetching only 12 hours of data as of now
        end_datetime = start_datetime + pd.DateOffset(hours=15)

        coin_pair = coin + 'USDT'
        df_hist_of_coin = binance_api.get_historical_data(
                            api_key= binance_api_key, 
                            api_secret= binance_api_secret,
                            coin_pair = coin_pair, 
                            start_time = str(tweet_time),
                            end_time = str(end_datetime),
                            min_interval ='1m',
                            kline_type = 'SPOT'
                            )
        if df_hist_of_coin is None:
            print(f'Prices for {coin_pair} not available in Binance')
            continue

        df_hist_of_coin['coin_pair'] = coin_pair
        print(coin_pair,len(df_hist_of_coin))
        df_binance = df_binance.append(df_hist_of_coin, ignore_index= True)
    
    df_binance.to_csv('data/price_data_binance.csv',index = False)
    print('Prices data fetched from Binance has been saved in data folder')

    return df_binance


def fetch_price_from_ftx(df_tweets):
    #FTX Fetch prices
    df_ftx = pd.DataFrame()
    for i in range(len(df_tweets)):
        df_temp = df_tweets.iloc[i,:]
        tweet_time = df_temp['created_at']
        base_currency = df_temp['coin']
        quote_currency = 'USD'
        coin_pair = base_currency + quote_currency
        min_interval=str(60)
        
        tweet_time = pd.to_datetime(tweet_time)
        start_timestamp = datetime.timestamp(tweet_time)
        
        # fetching only 12 hours of data from the time of tweet
        end_datetime = tweet_time + pd.DateOffset(hours=12)
        end_timestamp = datetime.timestamp(end_datetime) 

        df_hist_of_coin = ftx_api.get_historical_data(
                            base_currency = base_currency, 
                            quote_currency = quote_currency, 
                            start_time = start_timestamp,
                            end_time = end_timestamp,
                            min_interval = min_interval,
                            )   

        if df_hist_of_coin is None:
            print(f'Prices for {coin_pair} not available in FTX')
            continue

        df_hist_of_coin['coin_pair'] = base_currency + quote_currency
        print(coin_pair,len(df_hist_of_coin))
        df_ftx = df_ftx.append(df_hist_of_coin, ignore_index= True)
    df_ftx.to_csv('data/price_data_ftx.csv',index = False)
    print('Prices data fetched from FTX has been saved in data folder')

    return df_ftx

def get_price_change_at_intervals(df, interval_list):
    df_price_diff = pd.DataFrame()
    coin_pair_list = df['coin_pair'].unique()
    for coin in coin_pair_list:
        df_temp = df.loc[df['coin_pair'] == coin].copy()
        row_dict = {}
        row_dict['coin_pair'] = coin
        base_price = df_temp.loc[df_temp['time'] == df_temp['time'].min(),'open_price']
        base_price = float(base_price)

        for i in range(len(interval_list)):
            tunit = re.sub(r'[0-9]', '', interval_list[i])
            value = re.sub('[^0-9,]', "", interval_list[i])
            diff_time = df_temp['time'].min() + pd.Timedelta(int(value),tunit)
            current_price = df_temp.loc[df_temp['time'] == diff_time,'close_price']
            current_price = float(current_price)
            price_diff = ((current_price - base_price)/base_price)*100
            print(price_diff)
            row_dict[interval_list[i]] = price_diff
        df_price_diff = df_price_diff.append(row_dict, ignore_index = True)    
    return df_price_diff


