import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter(action='ignore', category=FutureWarning)
import talib as ta
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta, FR




def breakout_strategy(data,stop_loss_multiple=2, take_profit_multiple=3):
    """
    Bollinger Band Breakout Strategy with ATR-based Stop Loss and Take Profit.

    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame containing 'High', 'Low', 'Adj Close' columns with DateTime index.
    stop_loss_multiple : int, optional
        Multiplier for ATR to calculate stop loss. Default = 2
    take_profit_multiple : int, optional
        Multiplier for ATR to calculate take profit. Default = 3

    Returns:
    --------
    data : pd.DataFrame
        Original DataFrame with signals added.
    trades : pd.DataFrame
        Trade log with entry/exit details and PnL.
    """

    # === Bollinger Bands ===
    data['upperband'], data['middleband'], data['lowerband'] = ta.BBANDS(data['Adj Close'], timeperiod=20)

    # Bandwidth & Conditions
    data['bandwidth'] = (data['upperband'] - data['lowerband']) / data['middleband']
    data['rolling_bandwidth'] = data['bandwidth'].rolling(21).mean()
    data['cond1'] = data['bandwidth'] > data['rolling_bandwidth']
    data['cond2'] = data['High'] > data['upperband']

    # Initial long signal
    data['lsignal'] = np.where(data['cond1'] & data['cond2'], 1, np.nan)
    data['lsignal'] = np.where(data['Low'] < data['middleband'], 0, data['lsignal'])
    data['lsignal'].fillna(method='ffill', inplace=True)

    # ATR for stop loss / take profit
    data['ATR'] = ta.ATR(data['High'], data['Low'], data['Adj Close'], timeperiod=14)

    # Trade variables
    data.set_index(data['Date'], inplace=True)
    current_position = 0
    entry_time = np.nan
    entry_price = np.nan
    stop_loss = None
    take_profit = None
    trades = pd.DataFrame(columns=['Position', 'Entry Time', 'Entry Price',
                                   'Exit Time', 'Exit Price', 'PnL'])

    # Helper to log trades
    def trade_details(time, entry_time, entry_price):
        pnl = round(data.loc[time,'Adj Close'] - entry_price, 2)
        trading_cost = data.loc[time,'Adj Close'] * 0.0002 * 2  # round trip cost
        pnl -= trading_cost
        return pd.DataFrame([{
            'Position': 'Long',
            'Entry Time': entry_time,
            'Entry Price': entry_price,
            'Exit Time': time,
            'Exit Price': data.loc[time,'Adj Close'],
            'PnL': pnl
        }])

    # Backtest loop
    for time in data.index:
        if (current_position == 0) and (data.loc[time, 'lsignal'] == 1):
            current_position = 1
            entry_time = time
            entry_price = data.loc[time,'Adj Close']
            stop_loss = entry_price - data.loc[time, 'ATR'] * stop_loss_multiple
            take_profit = entry_price + data.loc[time, 'ATR'] * take_profit_multiple

        elif current_position == 1:
            if data.loc[time,'Adj Close'] < stop_loss or data.loc[time,'Adj Close'] > take_profit:
                trades = pd.concat([trades, trade_details(time, entry_time, entry_price)], ignore_index=True)
                current_position = 0

    # Build the signal column for analysis
    data['signal'] = np.nan
    data.loc[data.index.isin(trades['Entry Time']), 'signal'] = 1
    data.loc[data.index.isin(trades['Exit Time']), 'signal'] = 0
    data['signal'].fillna(method='ffill', inplace=True)
    data['signal'] = data['signal'].shift(1)  # prevent look-ahead bias


    return data,trades



