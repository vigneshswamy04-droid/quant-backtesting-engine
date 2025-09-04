import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter(action='ignore', category=FutureWarning)
import talib as ta
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta, FR


def option_expiry_strategy(data):
    data.set_index('Date', inplace=True)

    def getexpiry(dt):
        return dt+relativedelta(weekday=FR(3))

    min_year = data.index.min().year
    max_year = data.index.max().year

    option_expiration_days = []
    for year in range(min_year, max_year + 1):
        for month in range(1, 13):
            option_expiration_days.append(getexpiry(date(year, month, 1)))

    condition1=(data.index+timedelta(4)).isin(option_expiration_days)
    condition2=(data.index+timedelta(3)).isin(option_expiration_days)
    condition3=(data.index+timedelta(2)).isin(option_expiration_days)
    condition4=(data.index+timedelta(1)).isin(option_expiration_days)

    data['signal']=np.where(condition1|condition2|condition3|condition4,1,0)

    current_position = 0
    entry_time = np.nan
    entry_price = np.nan
    trades = pd.DataFrame(columns=['Position', 'Entry Time', 'Entry Price', 'Exit Time', 'Exit Price', 'PnL'])

    def trade_details(time, entry_time, entry_price):
        pnl = round(data.loc[time, 'Adj Close'] - entry_price, 2)
        trading_cost = data.loc[time, 'Adj Close'] * 0.0002 * 2
        pnl -= trading_cost
        return pd.DataFrame([{
            'Position': 'Long',
            'Entry Time': entry_time,
            'Entry Price': entry_price,
            'Exit Time': time,
            'Exit Price': data.loc[time, 'Adj Close'],
            'PnL': pnl
        }])

    for time in data.index:
        if (current_position == 0) and (data.loc[time, 'signal'] == 1):
            current_position = 1
            entry_time = time
            entry_price = data.loc[time,'Open']
        elif current_position == 1:
            pos = data.index.get_loc(time)
            if pos < len(data.index) - 1:
               next_time = data.index[pos + 1]
               if data.loc[next_time,'signal']==0:
                  trades = pd.concat([trades, trade_details(time, entry_time, entry_price)], ignore_index=True)
                  current_position = 0
            else:
               break

    return data, trades
