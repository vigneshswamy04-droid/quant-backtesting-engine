import pandas as pd
import os
import requests

def load_local_datastocks(ticker, start_date, end_date, folder="/Users/vigneshswamynathan/Documents/quant__/MVPtd/data/STOCKANDETF/stocks", base_url=None):
    filepath = os.path.join(folder, f"{ticker}.csv")
    
    # Check if file exists locally
    if not os.path.exists(filepath):
        if base_url:
            print(f"Fetching {ticker} from {base_url}...")
            url = f"{base_url}/{ticker}.csv"
            df = pd.read_csv(url, parse_dates=['Date'], index_col='Date')
        else:
            raise FileNotFoundError(f"No local file and no base_url for {ticker}")
    else:
        df = pd.read_csv(filepath, index_col="Date", parse_dates=True)
    
    # Slice by date
    df = df.loc[start_date:end_date]
    return df
