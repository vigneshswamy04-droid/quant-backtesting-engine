import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.dataoperations.loadlocaldataSTOCK import load_local_datastocks
from src.dataoperations.datacleaning import clean_market_data
from src.strategies.E_breakoutstrategy import breakout_strategy
from src.strategies.E_feddaystrategyfinal import feddaystrategy
from src.metrics.Performancemetrics import analyze_strategy_performance
from src.metrics.trademetrics import trade_metrics  
from src.strategies.E_optionexpiryfinal import option_expiry_strategy
from src.strategies.E_paydayeffectfinal import payday_effect_strategy
from src.strategies.E_turnofthemonthfinal import turn_of_month
from src.strategies.FI_auctioneffectfinal import treasury_auction_strategy
from src.strategies.FI_endofmonthfinal import turn_of_monthFI
from src.dataoperations.loadlocaldataETF import load_local_dataetf
from src.strategies.V_decemebreffectfinal import christmas_short_vix_strategy
from src.strategies.V_futuresexpiryeffectfinal import vixyfutureexpiry

import os

st.set_page_config(layout="wide")
st.title("📊 Quant Strategy Dashboard")

# --- Sidebar ---
st.sidebar.header("Configuration")

# Step 0: Select asset type
asset_type = st.sidebar.radio("Select Asset Type", ["Stocks", "ETFs"])

# Step 1: Select ticker based on asset type
def list_available_tickers(folder):
    return [f.replace(".csv", "") for f in os.listdir(folder) if f.endswith(".csv")]

if asset_type == "Stocks":
    available_tickers = list_available_tickers("data/STOCKANDETF/stocks")
    ticker = st.sidebar.selectbox("Select Stock Ticker", options=available_tickers)
else:
    available_tickers = list_available_tickers("data/STOCKANDETF/etfs")
    ticker = st.sidebar.selectbox("Select ETF Ticker", options=available_tickers)

# Step 2: Date range
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2010-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2020-12-31"))

# Step 3: Strategy choice — includes all strategies directly
strategy_choice = st.sidebar.selectbox(
    "Select Strategy",
    [
        "Breakout Strategy",
        "Fed Day Strategy",
        "Option Expiry Strategy",
        "Payday Effect Strategy",
        "Turn Of Month Strategy",
        "Auction Effect Strategy",
        "Turn Of Month FI Strategy",
        "Christmas VIXY Strategy",
        "Future Expiry Strategy"
    ]
)

run_strategy = st.sidebar.button("Run Strategy")

# --- Execution Pipeline ---
if run_strategy:
    st.subheader(f"Running {strategy_choice} on {ticker} ({start_date} to {end_date})")

    try:
        # Step 1: Load local CSV data
        st.info("Loading local market data...")
        if asset_type == "Stocks":
            raw_data = load_local_datastocks(ticker, str(start_date), str(end_date))
        else:
            raw_data = load_local_dataetf(ticker, str(start_date), str(end_date))

        # Step 2: Clean data
        st.info("Cleaning market data...")
        data = clean_market_data(raw_data, drop_duplicates=True, plot_returns=False)
        

        # Step 3: Run selected strategy
        st.info(f"Running {strategy_choice}...")
        if strategy_choice == "Breakout Strategy":
            data, trades = breakout_strategy(data)
        elif strategy_choice == "Fed Day Strategy":
            data, trades = feddaystrategy(data)
        elif strategy_choice == "Option Expiry Strategy":
            data, trades = option_expiry_strategy(data)
        elif strategy_choice == "Payday Effect Strategy":
            data, trades = payday_effect_strategy(data)
        elif strategy_choice == "Turn Of Month Strategy":
            data, trades = turn_of_month(data)
        elif strategy_choice == "Auction Effect Strategy":
            data, trades = treasury_auction_strategy(data)
        elif strategy_choice == "Turn Of Month FI Strategy":
            data, trades = turn_of_monthFI(data)
        elif strategy_choice == "Christmas VIXY Strategy":
            data, trades = christmas_short_vix_strategy(data)
        elif strategy_choice == "Future Expiry Strategy":
            data, trades = vixyfutureexpiry(data)

        # Step 4: Show Trade Book
        st.subheader("📘 Trade Book")
        st.dataframe(trades)

        # Step 5: Show Trade Book Metrics in KPI format
        st.subheader("📊 Trade Book Metrics")
        trade_stats = trade_metrics(trades)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total PnL", f"{trade_stats['Total PnL']:.2f}")
        col2.metric("Total Trades", trade_stats['total_trades'])
        col3.metric("Win %", f"{trade_stats['Win (%)']:.2f}%")
        col4.metric("Loss %", f"{trade_stats['Loss (%)']:.2f}%")

        col5, col6, col7 = st.columns(3)
        col5.metric("Avg Holding Time (days)", f"{trade_stats['Average holding time (days)']:.2f}")
        col6.metric("Profit Factor", f"{trade_stats['Profit Factor']:.2f}")
        col7.metric("Avg PnL Winners", f"{trade_stats['per_trade_PnL_winners']:.2f}")

        # Step 6: Analyze performance
        st.info("Calculating performance metrics...")
        data, metrics, graphs = analyze_strategy_performance(data)

        # --- Display Performance Metrics ---
        st.subheader("📈 Performance Metrics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("CAGR", metrics["CAGR"])
        col2.metric("Volatility", metrics["Annualised Volatility"])
        col3.metric("Sharpe Ratio", metrics["Sharpe Ratio"])
        col4.metric("Max Drawdown", metrics["Maximum Drawdown"])

        st.write("Strategy Returns and Cumulative Returns")
        st.dataframe(data.loc[data['signal'].isin([1, -1]), ['Strategy_Returns', 'Cumulative_Returns']])

        # --- Display Graphs from Performance Metrics ---
        for name, fig in graphs.items():
            st.subheader(name)
            st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error running strategy: {e}")
