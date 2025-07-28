# S&P 500 with Macroeconomic Analysis

This project analyzes the relationship between S&P 500 returns and various US macroeconomic indicators using time series econometric techniques. It loads, preprocesses, and merges financial and macroeconomic data, then applies statistical analyses and visualizations to uncover insights.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [File Structure](#file-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Data Preparation](#data-preparation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Output](#output)

## Overview
This project starts with three csv files downloaded from reliable sources which include the S&P500 historical price with 12 other US macroeconomic metrics. The data is first processed into stationary form which is prerequisite for the below analysis. 

Then the data is fed into different functions or tests using time series econometric techniques, and applies statistical analyses (e.g., Granger causality, VAR modeling, cross-correlation) via scripts to find their relationship, pattern or predictive power to each other. 

Visualizations (e.g., correlation heatmaps, time series plots) are generated using matplotlib and seaborn.
For detailed visualizations and analysis, see the PowerPoint in the folder [sp500&marco.pptx](sp500&macro.pptx)


## Features

- **Data Loading & Preprocessing:** Reads and merges S&P 500, GDP, and macroeconomic CSV data.
- **Feature Engineering:** Creates additional features for analysis.
- **Correlation Analysis:** Plots heatmaps to visualize relationships between variables.
- **Cross-Correlation Function (CCF) Analysis:** Examines lead-lag relationships.
- **Granger Causality Tests:** Identifies variables that help predict S&P 500 returns.
- **Feature Selection:** Finds the best combination of predictors for S&P 500 returns.
- **VAR Modeling:** Trains a Vector Autoregression model for multivariate time series forecasting.
- **Visualization:** Provides multi-series plots with event overlays.


## File Structure
```
sp500_with_macro/
├── sp500_with_macro.sln
├── .gitignore
├── sp500&marco.pptx
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


## Requirements

- Python 3.8+

Standard Library
-os
-pathlib
-datetime
-itertools
-warnings
-typing

Third-Party Libraries
-pandas
-numpy
-matplotlib
-seaborn
-statsmodels

- Visual Studio (optional, for `sp500_with_macro.sln`)

- Git (for cloning)


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/leoncc24/sp500_with_macro.git 
   cd sp500_with_macro
   ```

2. Install dependencies:
   ```bash
   pip install pandas numpy matplotlib yfinance seaborn statsmodels
   *(Make sure you have Python 3.8+ and pip installed.)*
   ```

3. Prepare data:
   ```bash
   - Place the required CSV files in the `data/` directory as shown above.
   ```


## Data Preparation

-Composite Leading Indicators Reference Series (GDP) Normalized for United States:
https://fred.stlouisfed.org/series/USALORSGPNOSTSAM

-USA Key Economic Indicators: 
https://www.kaggle.com/datasets/calven22/usa-key-macroeconomic-indicators

-S&P 500 (SPX): 
https://www.investing.com/indices/us-spx-500-historical-data


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

