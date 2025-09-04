import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def clean_market_data(data, drop_duplicates=True, plot_returns=False):
    # If DataFrame only has one column, assume it's the Date column'
    if data.shape[1] == 1:
        date_col = data.columns[0]
        data[date_col] = pd.to_datetime(data[date_col], errors='coerce',dayfirst=True)
        data = data.dropna().sort_values(by=date_col)
        data.set_index(date_col, inplace=True)
        #print("Only Date column found. Converted to datetime (dd-mm-yyyy), sorted, and returned.\n")
        data=data.reset_index()
        return data
    
    


    # Strip spaces in column names
    data.columns = [col.strip() for col in data.columns]

    # Rename known columns
    rename_map = {
        'Open': 'Open',
        'High': 'High',
        'high':'High',
        'low':'Low',
        'Low': 'Low',
        'Close': 'Close',
        'close':'Close',
        'c': 'Close',            # Polygon API Close
        'o': 'Open',             # Polygon API Open
        'h': 'High',             # Polygon API High
        'l': 'Low',              # Polygon API Low
        'v': 'Volume',
        'Close/Last': 'Close',
        'Adj Close': 'Adj Close',
        'AdjClose': 'Adj Close',
        'Adjusted Close': 'Adj Close',
        'Volume': 'Volume',
        'Vol': 'Volume',
        'vol':'Volume',
        'DATE': 'Date',
        'date': 'Date',
        't': 'Date',
        'timestamp':'Date'
    }
    data = data.rename(columns={col: rename_map[col] for col in data.columns if col in rename_map})

    # Convert 'Date' column to datetime and set as index
    if 'Date' in data.columns:
         data['Date'] = pd.to_datetime(data['Date'], errors='coerce', dayfirst=True)
         data = data.sort_values('Date')
         data = data.reset_index(drop=True)
    elif isinstance(data.index, pd.DatetimeIndex):
        data = data.sort_index()
        data = data.reset_index()   
        data.rename(columns={'index': 'Date'}, inplace=True)
        #data=data.reset_index()
    else:
        print("⚠️ No 'Date' column found and index is not datetime.\n")

    # Show null values
    null_counts = data.isnull().sum()
    #print(null_counts)

    if null_counts.any():
        total_cells = data.shape[0] * data.shape[1]
        total_nulls = null_counts.sum()
        null_percent = (total_nulls / total_cells) * 100

        '''print("Null values detected:")
        print(null_counts[null_counts > 0])'''

        if null_percent < 1:
            '''print(f"→ Missing data accounts for only {null_percent:.2f}% of dataset.")
            print("→ Removing rows with any null values...\n")'''
            data = data.dropna()
        else:
            '''print(f"⚠️ Warning: Missing data accounts for {null_percent:.2f}% of the dataset.")
            print("⚠️ Consider changing the data source or getting higher quality data.\n")'''
    

    # Handle duplicates
    if drop_duplicates:
        dup_count = data.duplicated().sum()
        total_rows = data.shape[0]
        dup_percent = (dup_count / total_rows) * 100

        

        if dup_percent >= 0.5:
           
            data = data.drop_duplicates()

        consecutive_dupes = data.shift(1) == data
        full_row_dupes = consecutive_dupes.all(axis=1)
        consecutive_dup_count = full_row_dupes.sum()

        if consecutive_dup_count > 0:
            '''print(f"→ {consecutive_dup_count} consecutive duplicate rows found.")
            print("→ Removing these rows...\n")'''
            data = data[~full_row_dupes]


    # Clean price columns
    price_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close']
    for col in price_cols:
        if col in data.columns:
            data[col] = data[col].astype(str).str.replace(r'[\$,]', '', regex=True)
            data[col] = pd.to_numeric(data[col], errors='coerce')

    # Adjust OHLC to match Adj Close
    if 'Adj Close' in data.columns:
        adjustment_factor = data['Adj Close'] / data['Close']
        for col in ['Open', 'High', 'Low']:
            if col in data.columns:
                data[col] = data[col] * adjustment_factor
        #print("→ OHLC columns adjusted using Adj Close.\n")

    # Convert Volume
    if 'Volume' in data.columns:
        data['Volume'] = pd.to_numeric(data['Volume'], errors='coerce')

    # Calculate returns
    if 'Adj Close' in data.columns:
        data['returns'] = data['Adj Close'].pct_change(fill_method=None)
    else:
        data['returns'] = data['Close'].pct_change(fill_method=None)

    # Remove outliers in returns
    if 'returns' in data.columns:
        mean_ret = data['returns'].mean()
        std_ret = data['returns'].std()
        z_scores = (data['returns'] - mean_ret) / std_ret
        outliers = np.abs(z_scores) > 3
        num_outliers = outliers.sum()

        if num_outliers > 0:
            data = data[~outliers]

    # Plot returns if requested
    if plot_returns and 'returns' in data.columns:
        plt.plot(data['returns'])
        plt.xlabel('Date')
        plt.ylabel('returns')
        plt.title('Total Returns')
        plt.grid()
        #plt.show()
    
    

    return data
