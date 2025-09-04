import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
from pandas.tseries.offsets import BDay

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter(action='ignore', category=FutureWarning)
import talib as ta
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta, FR
from datetime import date, timedelta
from pandas.tseries.offsets import BDay
from src.dataoperations.datacleaning import clean_market_data

def christmas_short_vix_strategy(vixyprices):
    

    vixy1m = pd.read_csv("/Users/vigneshswamynathan/Documents/quant__/MVPtd/data/vix_2005_jan_2023_dec.csv",index_col='Date',parse_dates=True)
    vixy3m = pd.read_csv("/Users/vigneshswamynathan/Documents/quant__/MVPtd/data/vix3m_2005_jan_2023_dec.csv",index_col='Date',parse_dates=True)
    vixyexpiry = pd.read_csv("/Users/vigneshswamynathan/Documents/quant__/MVPtd/data/STOCKANDETF/expiry_Dates/vixyfuturesexpiry.csv")
   

    
    #vixyprices.reset_index(drop=False, inplace=True)
    vixy1m = clean_market_data(vixy1m, True, False)
    vixy3m = clean_market_data(vixy3m, True, False)
    vixyexpiry=clean_market_data(vixyexpiry,True,False)

    nmergedvixy = pd.merge(vixy3m, vixy1m, how='outer', on='Date', suffixes=('_3M', '_1M'))
    vixyprices = pd.merge(vixyprices, nmergedvixy[['Date', 'Close_1M', 'Close_3M']], how='left', on='Date')

    condition_1 = vixyprices['Date'].shift(-2).isin(vixyexpiry['Date'])
    condition_2 = vixyprices['Date'].dt.month == 12
    condition_3 = vixyprices['Close_1M'] < vixyprices['Close_3M']
    vixyprices['signal'] = np.where(condition_1 & condition_2 & condition_3, -1, np.nan)
    pd.set_option("display.max_columns", None)
    print(vixyprices.tail())
    #print(vixyprices.loc[vixyprices['signal'] == -1])

    years = vixyexpiry.Date.dt.year.unique()
    def get_date(year, bus_days_offset):
        return date(year, 12, 25) + BDay(bus_days_offset)
    func = np.vectorize(get_date)
    bus_days_aft_xmas = np.append(func(years, 1), func(years, 2))
    vixyprices['signal'] = np.where(vixyprices['Date'].isin(bus_days_aft_xmas), 0, vixyprices['signal'])

    vixyprices.fillna(method='ffill', inplace=True)
    vixyprices['signal'].fillna(0.0, inplace=True)
    vixyprices.set_index('Date',inplace=True)
    current_position = 0
    entry_time = np.nan
    entry_price = np.nan
    trades = pd.DataFrame(columns=['Position', 'Entry Time', 'Entry Price', 'Exit Time', 'Exit Price', 'PnL'])

    def trade_details(time, entry_time, entry_price):
        pnl = round(entry_price - vixyprices.loc[time, 'Close'], 2)
        trading_cost = vixyprices.loc[time, 'Close'] * 0.0002 * 2
        pnl -= trading_cost
        return pd.DataFrame([{
            'Position': 'Short',
            'Entry Time': entry_time,
            'Entry Price': entry_price,
            'Exit Time': time,
            'Exit Price': vixyprices.loc[time, 'Close'],
            'PnL': pnl
        }])

    for time in vixyprices.index:
        pos = vixyprices.index.get_loc(time)
        if pos < len(vixyprices.index) - 1:
            next_time = vixyprices.index[pos + 1]
        else:
            break
        if current_position == 0 and vixyprices.loc[time, 'signal'] == -1:
            current_position = 1
            entry_time = time
            entry_price = vixyprices.loc[time, 'Open']
        elif current_position == 1 and vixyprices.loc[next_time, 'signal'] == 0:
            trades = pd.concat([trades, trade_details(time, entry_time, entry_price)], ignore_index=True)
            current_position = 0
    
    


    return vixyprices, trades
