import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analyze_strategy_performance(data):
    performance_metrics = {}
    graphs = {}

    # === Step 1: Ensure signal column exists ===
    if 'signal' not in data.columns:
        raise ValueError("The data must contain a 'signal' column.")

    # === Step 2: Use Adj Close if available, else use Close ===
    if 'Adj Close' in data.columns:
        price_col = 'Adj Close'
    elif 'Close' in data.columns:
        price_col = 'Close'
    else:
        raise ValueError("The data must contain either 'Adj Close' or 'Close' column.")

    # === Step 3: Calculate Returns ===
    data['Market_Returns'] = data[price_col].pct_change().fillna(0)
    data['Position'] = data['signal']
    data['Strategy_Returns'] = data['Market_Returns'] * data['Position']
    data['Cumulative_Returns'] = (1 + data['Strategy_Returns']).cumprod()

    # === Step 4: Performance Metrics ===
    days = len(data['Cumulative_Returns'].dropna())
    if days > 0:
        cagr = (data['Cumulative_Returns'].iloc[-1]) ** (252 / days) - 1
        performance_metrics['CAGR'] = f"{cagr * 100:.2f}%"
    else:
        performance_metrics['CAGR'] = "N/A"

    volatility = data['Strategy_Returns'].std() * np.sqrt(252)
    performance_metrics['Annualised Volatility'] = f"{volatility * 100:.2f}%"

    risk_free_rate = 0.02 / 252
    sharpe = ((data['Strategy_Returns'].mean() - risk_free_rate) /
              data['Strategy_Returns'].std()) * np.sqrt(252)
    performance_metrics['Sharpe Ratio'] = round(sharpe, 2)

    # === Step 5: Drawdowns ===
    data['Peak'] = data['Cumulative_Returns'].cummax()
    data['Drawdown'] = (data['Cumulative_Returns'] - data['Peak']) / data['Peak']
    performance_metrics['Maximum Drawdown'] = f"{data['Drawdown'].min() * 100:.2f}%"

    # === Step 6: Graphs ===

    # 1. Equity Curve
    fig1, ax1 = plt.subplots(figsize=(15, 7))
    ax1.plot(data['Cumulative_Returns'], color='purple')
    ax1.set_title('Equity Curve', fontsize=14)
    ax1.set_ylabel('Cumulative Returns')
    ax1.set_xlabel('Date')
    graphs['equity_curve'] = fig1
   

    # 2. Histogram of Strategy Returns
    fig2, ax2 = plt.subplots(figsize=(15, 7))
    ax2.hist(data['Strategy_Returns'].dropna(), bins=50, color='royalblue')
    ax2.set_title('Histogram of Strategy Returns', fontsize=14)
    ax2.set_xlabel('Daily Returns')
    ax2.set_ylabel('Frequency')
    graphs['returns_histogram'] = fig2

    # 3. Drawdown Plot
    fig3, ax3 = plt.subplots(figsize=(15, 7))
    ax3.plot(data['Drawdown'], color='red')
    ax3.fill_between(data['Drawdown'].index, data['Drawdown'].values, color='red', alpha=0.3)
    ax3.set_title('Drawdowns for Strategy', fontsize=14)
    ax3.set_ylabel('Drawdown (%)')
    ax3.set_xlabel('Date')
    graphs['drawdown_plot'] = fig3

    return data,performance_metrics, graphs
