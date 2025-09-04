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
def treasury_auction_strategy(data):

    # --- Step 1: Preprocessing ---
    auctionexpiry=pd.read_csv("/Users/vigneshswamynathan/Documents/quant__/MVPtd/data/STOCKANDETF/expiry_Dates/treasuryauctiondates.csv")
    auctionexpiry=clean_market_data(auctionexpiry)
    #auctionexpiry['Date'] = pd.to_datetime(auctionexpiry['Date'], dayfirst=True)

    condition_1 = (data['Date'] - BDay(1)).isin(auctionexpiry['Date'])
    condition_2 = (data['Date'] - BDay(2)).isin(auctionexpiry['Date'])
    data['signal'] = np.where(condition_1 | condition_2, 1, 0)

    data.set_index('Date', inplace=True)

    # --- Step 2: Trade logic ---
    current_position = 0
    entry_time = np.nan
    entry_price = np.nan
    trades = pd.DataFrame(columns=['Position', 'Entry Time', 'Entry Price', 'Exit Time', 'Exit Price', 'PnL'])

    def trade_details(time, entry_time, entry_price):
        pnl = round(data.loc[time, 'Close'] - entry_price, 2)
        trading_cost = data.loc[time, 'Close'] * 0.0002 * 2
        pnl -= trading_cost
        return pd.DataFrame([{
            'Position': 'Long',
            'Entry Time': entry_time,
            'Entry Price': entry_price,
            'Exit Time': time,
            'Exit Price': data.loc[time, 'Close'],
            'PnL': pnl
        }])

    for time in data.index:
        if (current_position == 0) and (data.loc[time, 'signal'] == 1):
            current_position = 1
            entry_time = time
            entry_price = data.loc[time, 'Open']
        elif current_position == 1 and data.loc[time, 'signal'] == 1:
            trades = pd.concat([trades, trade_details(time, entry_time, entry_price)], ignore_index=True)
            current_position = 0

    # --- Step 3: Analyze performance ---

    return data, trades
