import numpy as np
import pandas as pd
from config.settings import RECESSION_PERIODS

def create_features(df):
    """Create derived features"""
    df = df.copy()
    
    # Returns and growth calculations
    df['SP500_returns'] = np.log(df['Price']).diff()
    df['Consumption_growth'] = np.log(df['Personal Consumption Expenditures']).diff()
    df['Income_growth'] = np.log(df['Real Disposable Personal Income']).diff()
    df['Personal_Saving_Rate'] = np.log(df['Personal Saving Rate']).diff()
    df['M2_pct_change'] = df['M2'].pct_change()
    df['IP_growth'] = np.log(df['Industrial Production Index']).diff()
    df['Construction_growth'] = np.log(df['Total Construction Spending']).diff()
    df['FX_returns'] = np.log(df['Real Broad Exchange Rate']).diff()
    df['10Y_yield_diff'] = df['10-Year Yield'].diff()
    df['FFR_diff'] = df['Federal Funds Rate'].diff()

    # CPI calculations
    df['CPI_adj'] = np.where(
        df.index.year < 1990,
        df['CPI'].pct_change(1),
        df['CPI'].pct_change(2)
    )
    df['D1_D12_log_CPI'] = np.log(df['CPI']).diff(12).diff(1)

    return df

def mark_recession_periods(df):
    """Add recession indicator column"""
    df['Recession'] = 0
    for start, end in RECESSION_PERIODS:
        mask = (df['Date'] >= pd.to_datetime(start)) & (df['Date'] <= pd.to_datetime(end))
        df.loc[mask, 'Recession'] = 1
    return df