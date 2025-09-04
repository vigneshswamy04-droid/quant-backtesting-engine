import pandas as pd
import numpy as np
import warnings 
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8-darkgrid')

def trade_metrics(trades):
    analytics = pd.DataFrame(index=['Strategy'])
    analytics['Total PnL'] = trades.PnL.sum() 

    #print("Total PnL: ", analytics['Total PnL'][0])
    long_count  = (trades['Position'] == 'Long').sum()
    short_count = (trades['Position'] == 'Short').sum()

    # decide which total to report
    if short_count == 0 and long_count > 0:
        analytics['total_trades'] = long_count
    elif long_count == 0 and short_count > 0:
        analytics['total_trades'] = short_count
    else:
        # mixed book or unknown labels
        analytics['total_trades'] = len(trades)
    
    # Profitable trades
    analytics['Number of Winners'] = len(trades.loc[trades.PnL>0])
    analytics['Number of Losers'] = len(trades.loc[trades.PnL<=0])
    analytics['Win (%)'] = 100 * analytics['Number of Winners'] / analytics.total_trades
    analytics['Loss (%)'] = 100 * analytics['Number of Losers'] / analytics.total_trades
    
    analytics['per_trade_PnL_winners'] = trades.loc[trades.PnL>0].PnL.mean()
    analytics['per_trade_PnL_losers'] = np.abs(trades.loc[trades.PnL<=0].PnL.mean())
    
    holding_period = trades['Exit Time'] - trades['Entry Time']
    avg_holding_days = holding_period.mean() / pd.Timedelta(days=1)
    analytics['Average holding time (days)'] = round(avg_holding_days, 2)
    
    analytics['Profit Factor'] = (
        (analytics['Win (%)'] / 100 * analytics['per_trade_PnL_winners']) /
        (analytics['Loss (%)'] / 100 * analytics['per_trade_PnL_losers'])
    )

    # 🔹 Convert DataFrame row to dictionary
    analytics_dict = analytics.iloc[0].to_dict()

    return analytics_dict
