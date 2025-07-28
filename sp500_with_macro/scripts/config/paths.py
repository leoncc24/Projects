from pathlib import Path

# Get the root directory (two levels up from config folder)
ROOT_DIR = Path(__file__).parent.parent.parent

DATA_PATHS = {
    'macro': ROOT_DIR / 'data' / 'macro_monthly.csv',
    'sp500': ROOT_DIR / 'data' / 'S&P 500 Historical Data.csv',
    'gdp': ROOT_DIR / 'data' / 'Normalized GDP.csv',
    'output': ROOT_DIR / 'data' / 'merged.csv'
}