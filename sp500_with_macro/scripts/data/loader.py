import pandas as pd
from pathlib import Path
from config.paths import DATA_PATHS

def load_raw_data():
    """Load all raw data files"""
    try:
        df = pd.read_csv(DATA_PATHS['macro'])
        gdp = pd.read_csv(DATA_PATHS['gdp'])
        sp500 = pd.read_csv(DATA_PATHS['sp500'])
        return df, gdp, sp500
    except FileNotFoundError as e:
        print(f"Error loading files. Current working directory: {Path.cwd()}")
        print(f"Attempted paths:")
        for name, path in DATA_PATHS.items():
            print(f"{name}: {path} (exists: {path.exists()})")
        raise

def preprocess_data(df, gdp, sp500):
    """Clean and merge datasets"""
    # Column renaming
    df.columns = ['Date','Unemployment Rate', 'Personal Saving Rate', 'M2', 
                 'Real Disposable Personal Income','Personal Consumption Expenditures',
                 'Real Broad Exchange Rate', '10-Year Yield', 'Federal Funds Rate',
                 'Total Construction Spending', 'Industrial Production Index', 'CPI']
    
    gdp.columns = ['Date','Normalized GDP']
    sp500.columns = ['Date','Price','Change %']
    
    # Date parsing
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    gdp['Date'] = pd.to_datetime(gdp['Date'], format='%d/%m/%Y')
    sp500['Date'] = pd.to_datetime(sp500['Date'], format='%m/%d/%Y')
    
    # Merge data
    merged = df.merge(gdp, on='Date', how='inner').merge(sp500, on='Date', how='inner')
    
    # Additional preprocessing
    merged['Change %'] = merged['Change %'].apply(lambda x: float(x.strip('%')))/100
    merged['Price'] = merged['Price'].str.replace(',', '').astype(float)
    merged.set_index('Date', inplace=True)
    
    return merged