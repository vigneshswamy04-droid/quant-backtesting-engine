import numpy as np
import pandas as pd
from src.dataoperations.datacleaning import clean_market_data


def feddaystrategy(data):
    """
    Fed day strategy:
    Buys SPY if the next day after a Fed expiry date is above its 100-day moving average.
    
    Parameters:
    - data: DataFrame containing SPY data with 'Date' and 'Adj Close'.

    Returns:
    - data: DataFrame with signals and performance metrics.
    - trades: DataFrame trade book with Entry/Exit details and PnL.
    - metrics: Strategy performance metrics.
    - graphs: Performance plots (e.g., equity curve).
    """

    # Clean SPY data

    # --- Load and clean Fed expiry dates directly inside ---
    fed = pd.read_csv("/Users/vigneshswamynathan/Documents/quant__/MVPtd/data/STOCKANDETF/expiry_Dates/fedexpiry.csv")
    fed = clean_market_data(fed, drop_duplicates=True, plot_returns=False).reset_index()

    # Strategy logic: Buy if next day is a fed expiry and price > 100-day MA
    condition1 = data['Date'].isin(fed['Date'])
    data['lmavg'] = data['Adj Close'].rolling(100).mean()
    condition3 = data['Adj Close'] > data['lmavg'].shift(1)
    data['signal'] = np.where(condition1 & condition3, 1, 0)

    # Backtest loop
    data.set_index('Date', inplace=True)
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
        pos = data.index.get_loc(time)
        if pos < len(data.index) - 1:
            next_time = data.index[pos + 1]
        else:
            break

        if (current_position == 0) and (data.loc[next_time, 'signal'] == 1):
            current_position = 1
            entry_time = time
            entry_price = data.loc[time, 'Adj Close']

        elif current_position == 1:
            trades = pd.concat([trades, trade_details(time, entry_time, entry_price)], ignore_index=True)
            current_position = 0

    # Analyze performance
    

    return data, trades
