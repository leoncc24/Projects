import matplotlib.pyplot as plt
import pandas as pd
from config import settings

def plot_granger_results(variables, p_values):
    """Plot Granger causality test results"""
    plt.figure(figsize=(12, 6))
    for var, p_vals in zip(variables, p_values):
        plt.plot(range(1, settings.MAX_LAG+1), p_vals, 
                marker='o', label=var, color=settings.COLOR_MAP.get(var, 'black'))
    
    plt.axhline(y=settings.SIGNIFICANCE_LEVEL, color='r', linestyle='--', 
                label=f'Significance Level ({settings.SIGNIFICANCE_LEVEL})')
    plt.title('Granger Causality Test Results')
    plt.xlabel('Lag')
    plt.ylabel('P-Value')
    plt.legend()
    plt.grid()
    plt.show()

def plot_var_results(results):
    """Plot VAR model predictions vs actual"""
    plt.figure(figsize=(12, 6))
    plt.plot(results['train'], label='Train')
    plt.plot(results['actuals'], label='Actual')
    plt.plot(results['predictions'], label='Predicted', linestyle='--')
    plt.title(f'VAR Model Results (RMSE={results["rmse"]:.4f})')
    plt.legend()
    plt.grid()
    plt.show()
