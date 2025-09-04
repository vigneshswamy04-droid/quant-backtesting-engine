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

## 📷 Screenshots

_Add screenshots or a short GIF of your Streamlit UI here._

---

## 🛠️ Roadmap

- [ ] Add more pre-built strategies  
- [ ] Integrate live market data APIs  
- [ ] Add machine learning-based strategy selection  
- [ ] Extend portfolio optimization module  
- [ ] Deploy demo app online