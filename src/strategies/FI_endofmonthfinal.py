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

import numpy as np
import pandas as pd

def turn_of_monthFI(data):
    """
    Generates signals based on the last or second-last trading day of the month.
    Executes trades when signal is 1 and exits on the next signal.
    
    Parameters:
        data (pd.DataFrame): Cleaned market data with 'Date' as index and 'Open'/'Close' columns.

    Returns:
        data (pd.DataFrame): DataFrame with added 'signal' column.
        trades (pd.DataFrame): Trade log with entry/exit details and PnL.
    """
      # Ensure 'Date' is a column

    # Signal: last or second last day of the month
    condition_1 = data['Date'].dt.month != data['Date'].shift(-1).dt.month
    condition_2 = data['Date'].dt.month != data['Date'].shift(-2).dt.month
    data['signal'] = np.where(condition_1 | condition_2, 1, 0)

    data.set_index('Date', inplace=True)

    # Initialize trade variables
    current_position = 0
    entry_time = np.nan
    entry_price = np.nan
    trades = pd.DataFrame(columns=['Position', 'Entry Time', 'Entry Price', 'Exit Time', 'Exit Price', 'PnL'])

    # Trade generation
    for time in data.index:
        if current_position == 0 and data.loc[time, 'signal'] == 1:
            current_position = 1
            entry_time = time
            entry_price = data.loc[time, 'Open']
        elif current_position == 1 and data.loc[time, 'signal'] == 1:
            pnl = round(data.loc[time, 'Adj Close'] - entry_price, 2)
            trading_cost = data.loc[time, 'Adj Close'] * 0.0002 * 2
            pnl -= trading_cost
            trades = pd.concat([trades, pd.DataFrame([{
                'Position': 'Long',
                'Entry Time': entry_time,
                'Entry Price': entry_price,
                'Exit Time': time,
                'Exit Price': data.loc[time, 'Adj Close'],
                'PnL': pnl
            }])], ignore_index=True)
            current_position = 0

    return data, trades
