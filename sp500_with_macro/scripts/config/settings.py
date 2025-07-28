from datetime import datetime

# Analysis parameters
MAX_LAG = 12
SIGNIFICANCE_LEVEL = 0.05
TRAIN_TEST_SPLIT = 0.8

# Recession periods
RECESSION_PERIODS = [
    (datetime.strptime('01/01/1980', '%d/%m/%Y'), datetime.strptime('30/06/1980', '%d/%m/%Y')),
    (datetime.strptime('01/07/1981', '%d/%m/%Y'), datetime.strptime('30/11/1982', '%d/%m/%Y')),
    (datetime.strptime('01/07/1990', '%d/%m/%Y'), datetime.strptime('31/10/1990', '%d/%m/%Y')),
    (datetime.strptime('01/04/2001', '%d/%m/%Y'), datetime.strptime('31/10/2001', '%d/%m/%Y')),
    (datetime.strptime('01/12/2007', '%d/%m/%Y'), datetime.strptime('30/06/2009', '%d/%m/%Y')),
    (datetime.strptime('01/02/2020', '%d/%m/%Y'), datetime.strptime('31/03/2020', '%d/%m/%Y'))
]

# Variable definitions
TRANSFORMED_VARS = [
    'Unemployment Rate', 'Normalized GDP', 'IP_growth', 'FX_returns',
    'M2_pct_change', 'Income_growth', 'Consumption_growth', 'CPI_adj',
    'D1_D12_log_CPI', 'Construction_growth', 'FFR_diff', '10Y_yield_diff',
    'Personal_Saving_Rate'
]

COLOR_MAP = {
    'Unemployment Rate': 'blue',
    'Normalized GDP': 'orange',
    'IP_growth': 'brown',
    'FX_returns': 'pink',
    'M2_pct_change': 'green',
    'Income_growth': 'orange',
    'Consumption_growth': 'blue',
    'CPI_adj': 'red',
    'D1_D12_log_CPI': 'purple',
    'Construction_growth': 'cyan',
    'FFR_diff': 'gold',
    '10Y_yield_diff': 'grey',
    'Personal_Saving_Rate': 'black'
}

EVENTS = {
    'Black Monday': datetime(1987,10,19),
    'Russian crisis': datetime(1998,8,1),
    'Dot-com Peak': datetime(2000,3,10),
    'Lehman Collapse': datetime(2008,9,15),
    'COVID Crash': datetime(2020,3,23)
}
