from data.loader import load_raw_data,preprocess_data
from data.preprocessor import create_features
from analysis.granger import perform_granger_tests
from analysis.var_model import train_var_model
from analysis.CCF_test import plot_ccf_analysis
from analysis.corr_heatmap import plot_correlation_heatmap
from analysis.three_subplots import plot_three_series_with_events
from analysis.visualizations import plot_granger_results, plot_var_results
from analysis.find_best_target_vars import find_best_target_vars
from datetime import datetime
from config import paths, settings
import pandas as pd

def main():
    # 1. Data Loading and Preparation
    print("Loading and preprocessing data...")
    df, data, gdp = load_raw_data()
    merged = preprocess_data(df, data, gdp)
    merged = create_features(merged)
    merged.to_csv(paths.DATA_PATHS['output'])
    
    # 2. Correlation Analysis
    print("\nPlotting correlation heatmap...")
    plot_correlation_heatmap(
        merged, 
        ['SP500_returns'] + settings.TRANSFORMED_VARS
    )
    
    # 3. CCF Analysis
    print("\nRunning CCF analysis...")
    plot_ccf_analysis(
        merged,
        target_var='SP500_returns',
        features=settings.TRANSFORMED_VARS
    )
    
    # 4. Granger Causality
    print("\nPerforming Granger causality tests...")
    variables, p_values = perform_granger_tests(
        merged[['SP500_returns'] + settings.TRANSFORMED_VARS],
        'SP500_returns'
    )
    plot_granger_results(variables, p_values)


    # 5. Find the best combination of the features that minimizes RMSE for predicting S&P 500 returns
    if merged.index.inferred_freq is None:
        merged = merged.asfreq('M')
    sp500_col = 'SP500_returns'
    candidate_vars = [col for col in merged.columns if col != sp500_col]
    features = ['Unemployment Rate', 'Normalized GDP', 'IP_growth', 'FX_returns',
    'M2_pct_change', 'Income_growth', 'Consumption_growth', 'CPI_adj',
    'D1_D12_log_CPI', 'Construction_growth', 'FFR_diff', '10Y_yield_diff',
    'Personal_Saving_Rate']

    best_targets = find_best_target_vars(merged, sp500_col, candidate_vars, features, top_n=4)
    print(best_targets)


    # 6. VAR Modeling
    print("\nTraining VAR model...")
    var_results = train_var_model(
        merged,
        target_var='SP500_returns',
        features=['Unemployment Rate', 'Normalized GDP', 'CPI_adj']
    )
    plot_var_results(var_results)
    
    # 7. Multi-Series Visualization
    print("\nGenerating multi-series plot...")
    
    
    merged = merged.reset_index()  

    merged = merged.rename(columns={'index': 'Date'})
    
    if 'Date' in merged.columns:
        merged.set_index('Date', inplace=True)
        plot_three_series_with_events(
            merged,
            series_names=['SP500_returns', 'IP_growth', '10Y_yield_diff'],
            events=settings.EVENTS,
            title="Market Indicators with Recession Periods")
    else:
        print("The 'Date' column is missing from the merged DataFrame.")
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()

    # Results:
    # [{'features': ('Normalized GDP', 'D1_D12_log_CPI', '10Y_yield_diff'), 'rmse': np.float64(0.04099475382251843), 'nrmse': np.float64(0.13439137507569202)}, 
    #  {'features': ('Normalized GDP', 'CPI_adj', '10Y_yield_diff'), 'rmse': np.float64(0.04099941115466643), 'nrmse': np.float64(0.13440664301154215)}, 
    #  {'features': ('Normalized GDP', 'CPI_adj', 'D1_D12_log_CPI'), 'rmse': np.float64(0.041002265263963694), 'nrmse': np.float64(0.13441599951785843)}, 
    #  {'features': ('Unemployment Rate', 'Normalized GDP', 'CPI_adj'), 'rmse': np.float64(0.04101122214331036), 'nrmse': np.float64(0.13444536247822642)}]

    # [{'features': ('Normalized GDP', 'CPI_adj', 'D1_D12_log_CPI', '10Y_yield_diff'), 'rmse': np.float64(0.04101039308649295), 'nrmse': np.float64(0.13444264461617533)}, 
    #  {'features': ('Unemployment Rate', 'Normalized GDP', 'CPI_adj', 'D1_D12_log_CPI'), 'rmse': np.float64(0.04101186104117359), 'nrmse': np.float64(0.13444745695018603)}, 
    #  {'features': ('Unemployment Rate', 'Normalized GDP', 'CPI_adj', '10Y_yield_diff'), 'rmse': np.float64(0.04101808141118665), 'nrmse': np.float64(0.13446784892724617)}, 
    #  {'features': ('Unemployment Rate', 'Normalized GDP', 'D1_D12_log_CPI', '10Y_yield_diff'), 'rmse': np.float64(0.04102701628732116), 'nrmse': np.float64(0.13449713975541033)}]
