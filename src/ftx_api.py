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