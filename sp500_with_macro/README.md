# S&P 500 with Macroeconomic Analysis

This project analyzes the relationship between S&P 500 returns and various macroeconomic indicators using time series econometric techniques. It loads, preprocesses, and merges financial and macroeconomic data, then applies statistical analyses and visualizations to uncover insights.

## Features

- **Data Loading & Preprocessing:** Reads and merges S&P 500, GDP, and macroeconomic CSV data.
- **Feature Engineering:** Creates additional features for analysis.
- **Correlation Analysis:** Plots heatmaps to visualize relationships between variables.
- **Cross-Correlation Function (CCF) Analysis:** Examines lead-lag relationships.
- **Granger Causality Tests:** Identifies variables that help predict S&P 500 returns.
- **Feature Selection:** Finds the best combination of predictors for S&P 500 returns.
- **VAR Modeling:** Trains a Vector Autoregression model for multivariate time series forecasting.
- **Visualization:** Provides multi-series plots with event overlays.

## Project Structure
```
sp500_with_macro/
├── data/
│   ├── macro_monthly.csv
│   ├── S&P 500 Historical Data.csv
│   ├── Normalized GDP.csv
│   └── merged.csv
└── scripts/
    ├── config/
    │   └── paths.py
    ├── data/
    │   └── loader.py
    ├── analysis/
    │   ├── granger.py
    │   ├── var_model.py
    │   ├── CCF_test.py
    │   ├── corr_heatmap.py
    │   ├── three_subplots.py
    │   ├── visualizations.py
    │   └── find_best_target_vars.py
    └── main.py
```

## Installation

1. **Clone the repository:**
git clone <repo-url> cd sp500_with_macro
2. **Install dependencies:**
pip install -r requirements.txt
   *(Make sure you have Python 3.8+ and pip installed.)*
3. **Prepare data:**
   - Place the required CSV files in the `data/` directory as shown above.

## Usage

Run the main analysis script:
python scripts/main.py
This will:
- Load and preprocess the data
- Generate correlation heatmaps and CCF plots
- Perform Granger causality tests
- Select the best predictive features
- Train a VAR model and plot results
- Save the merged dataset to `data/merged.csv`

## Configuration

- Data paths are managed in `scripts/config/paths.py`.
- Analysis settings (such as variable lists and events) are in `scripts/config/settings.py`.

## Output

- Processed data: `data/merged.csv`
- Plots and analysis results: Displayed or saved as configured in the analysis scripts.

## Requirements

- Python 3.8+
Standard Library
•	os
•	pathlib
•	datetime
•	itertools
•	warnings
•	typing
Third-Party Libraries
•	pandas
•	numpy
•	matplotlib
•	seaborn
•	statsmodels
