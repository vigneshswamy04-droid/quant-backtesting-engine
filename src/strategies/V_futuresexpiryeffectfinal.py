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

def vixyfutureexpiry(vixyprices):
    

    # === your original data loads ===
    vixy1m = pd.read_csv(
        "/Users/vigneshswamynathan/Documents/quant__/Trading_engine/data/vix_2005_jan_2023_dec.csv",
        index_col='Date', parse_dates=True
    )
    vixy3m = pd.read_csv(
        "/Users/vigneshswamynathan/Documents/quant__/Trading_engine/data/vix3m_2005_jan_2023_dec.csv",
        index_col='Date', parse_dates=True
    )
    vixyexpiry = pd.read_csv(
        "/Users/vigneshswamynathan/Documents/quant__/Trading_engine/data/STOCKANDETF/expiry_Dates/vixyfuturesexpiry.csv"
    )

    # vixyprices.reset_index(drop=False, inplace=True)
    vixy1m = clean_market_data(vixy1m, True, False)
    vixy3m = clean_market_data(vixy3m, True, False)
    vixyexpiry = clean_market_data(vixyexpiry, True, False)

    mergedvixy=pd.merge(vixy1m[['Close']],vixy3m[['Close']],how='inner',left_index=True,right_index=True)
    nmergedvixy=pd.merge(vixyprices,mergedvixy,how='left',left_index=True,right_index=True)
    #nmergedvixy.reset_index(inplace=True)
    condition_1 = vixyprices['Date'].shift(-1).isin(vixyexpiry['Date'])
    condition_2 = vixyprices['Date'].shift(-2).isin(vixyexpiry['Date'])

    # keep your intent; add a tiny fallback so it works with either suffix style
    try:
        condition_3 = nmergedvixy['Close_x'] < nmergedvixy['Close_y']
    except KeyError:
        condition_3 = nmergedvixy['Close_3M'] < nmergedvixy['Close_1M']

    vixyprices['signal'] = np.where((condition_1 | condition_2) & condition_3, -1, 0)

    print(vixyprices.loc[vixyprices['signal'] == -1])

    vixyprices.set_index('Date', inplace=True)
    # pd.set_option('display.max_rows', None)
    # print(vixyprices.loc[vixyprices['signal']==-11])

    current_position = 0
    entry_time = np.nan
    entry_price = np.nan
    trades = pd.DataFrame(
        columns=['Position', 'Entry Time', 'Entry Price', 'Exit Time', 'Exit Price', 'PnL']
    )

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
        if (current_position == 0) and (vixyprices.loc[time, 'signal'] == -1):
            current_position = 1
            entry_time = time
            entry_price = vixyprices.loc[time, 'Open']

        elif current_position == 1 and vixyprices.loc[time, 'signal'] == -1:
            trades = pd.concat([trades, trade_details(time, entry_time, entry_price)],
                               ignore_index=True)
            current_position = 0

    return vixyprices, trades
