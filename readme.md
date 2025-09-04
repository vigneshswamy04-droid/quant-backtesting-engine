# Quant Backtesting Engine

A modular Python project for backtesting event-driven trading strategies.  
This engine includes multiple market effect strategies, trade and performance metrics, data loading/cleaning modules, and a Streamlit-based frontend to make results interactive and easy to explore.

---

## 📂 Project Structure

quant-backtesting-engine/
│
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
│
├── src/
│ ├── data/
│ │ ├── loadlocaldataETF.py
│ │ ├── loadlocaldataSTOCK.py
│ │ └── datacleaning.py
│ │
│ ├── strategies/
│ │ ├── E_breakoutstrategy.py
│ │ ├── E_turnofthemonthfinal.py
│ │ ├── E_paydayeffectfinal.py
│ │ ├── E_optionexpiryfinal.py
│ │ ├── E_feddaystrategyfinal.py
│ │ ├── V_futuresexpiryeffectfinal.py
│ │ ├── V_decemebreffectfinal.py
│ │ ├── FI_endofmonthfinal.py
│ │ └── FI_auctioneffectfinal.py
│ │
│ ├── metrics/
│ │ ├── trademetrics.py
│ │ └── Performancemetrics.py
│ │
│ └── ui/
│ └── frontendfinal.py # main entry point
│
├── sample_data/
│ └── sample_prices.csv
│
└── tests/
└── test_smoke.py

## 📊 Features

- **Strategies**
  - Breakout strategy
  - Turn-of-the-month effect
  - Payday effect
  - Option expiry effect
  - Fed day strategy
  - Futures expiry effect
  - December effect
  - Auction effect
  - End-of-month effect

- **Data Modules**
  - Local ETF loader
  - Local Stock loader
  - Data cleaning utilities

- **Metrics**
  - Trade-level metrics (PnL, win rate, exposure)
  - Performance metrics (Sharpe ratio, CAGR, drawdown)

- **Frontend**
  - Streamlit app for easy interaction
  - Run strategies, view backtests, and analyze metrics visually

---

## 📸 GIFS::

![Alt text](https://github-production-user-asset-6210df.s3.amazonaws.com/230210682/485786483-fff6f1cb-297a-4bea-8187-2598103121b1.gif?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20250904%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250904T173411Z&X-Amz-Expires=300&X-Amz-Signature=dcca934ef396f0034a04c3cc6279d01fe9a19189fbf9251cd5c4d6d32b8ed987&X-Amz-SignedHeaders=host)








---

## 🛠️ Roadmap

- [ ] Add core technical indicators (EMA, MACD, RSI, Bollinger Bands, etc.)  
- [ ] Build new strategies leveraging these indicators (trend-following, mean reversion, momentum)  
- [ ] Integrate financial time series models (ARIMA, GARCH, VAR) for return and volatility forecasting  
- [ ] Apply machine learning models (Random Forest, SVM, Neural Networks) combining technical indicators + time-series features to predict price movements  
- [ ] Expand evaluation framework with ML backtests and model comparison metrics  
- [ ] Implement portfolio construction methods:  
  - Equally weighted portfolios  
  - Volatility-based (minimum variance) portfolios  
  - Mean-variance optimization (Markowitz framework)  
- [ ] Extend portfolio optimization module with Sharpe ratio maximization and risk-parity strategies  
- [ ] Deploy demo app online with interactive dashboards
