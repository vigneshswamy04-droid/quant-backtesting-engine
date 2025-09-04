import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter(action='ignore', category=FutureWarning)
import talib as ta
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta, FR


def payday_effect_strategy(data):

    #data=data.reset_index()

    data['signal']=np.nan

    condition = data['Date'].dt.day == 16
    data['signal'] = np.where(condition, 1, 0)

    condition_1 = data['Date'].dt.day == 17
    condition_2 = data['signal'].shift(1) != 1
    data['signal'] = np.where(
    condition_1 & condition_2, 1,data['signal'])

    condition_1 = data['Date'].dt.day == 18
    condition_2 = data['signal'].shift(1) != 1
    condition_3 = data['signal'].shift(2) != 1
    data['signal'] = np.where(
    condition_1 & condition_2 & condition_3, 1, data['signal'])

    data.set_index('Date', inplace=True)

    current_position = 0
    entry_time = np.nan
    entry_price = np.nan
    trades = pd.DataFrame(columns=['Position', 'Entry Time', 'Entry Price', 'Exit Time', 'Exit Price', 'PnL'])

    def trade_details(time, entry_time, entry_price):
        pnl = round(data.loc[time,'Adj Close']-entry_price, 2)
        trading_cost = data.loc[time,'Adj Close'] * 0.0002 * 2
        pnl -= trading_cost
        return pd.DataFrame([{
            'Position': 'Long',
            'Entry Time': entry_time,
            'Entry Price': entry_price,
            'Exit Time': time,
            'Exit Price': data.loc[time,'Adj Close'],
            'PnL': pnl
        }])

    for time in data.index:
        pos = data.index.get_loc(time)
        if pos < len(data.index) - 1:
            next_time = data.index[pos + 1]
        else:
            break
        if (current_position == 0) and (data.loc[next_time, 'signal'] == 1):
            current_position = 1
            entry_time = time
            entry_price = data.loc[time,'Adj Close']
        elif current_position == 1:
            trades = pd.concat([trades, trade_details(time, entry_time, entry_price)], ignore_index=True)
            current_position = 0

    return data, trades
