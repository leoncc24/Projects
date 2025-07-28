import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import grangercausalitytests
from config.settings import TRANSFORMED_VARS, COLOR_MAP, MAX_LAG, SIGNIFICANCE_LEVEL

def perform_granger_tests(data, target_var, maxlag=MAX_LAG):
    """Perform Granger causality tests for multiple variables"""
    p_values = []
    variables = []
    
    for var in TRANSFORMED_VARS:
        if var == target_var:
            continue
            
        test_data = data[[target_var, var]].dropna()
        test_result = grangercausalitytests(test_data, maxlag=maxlag, verbose=False)
        
        lag_p_values = [test[0]['ssr_chi2test'][1] for test in test_result.values()]
        p_values.append(lag_p_values)
        variables.append(var)
    
    return variables, p_values

def plot_granger_results(variables, p_values, significance_level=SIGNIFICANCE_LEVEL):
    """Plot Granger causality test results"""
    plt.figure(1,figsize=(12, 6))
    for i, var in enumerate(variables):
        color = COLOR_MAP.get(var, 'black')
        plt.plot(range(1, MAX_LAG + 1), p_values[i], marker='o', color=color, label=var)

    plt.axhline(y=significance_level, color='r', linestyle='--', 
                label=f'Significance Level ({significance_level})')
    plt.title('Granger Causality Test P-Values')
    plt.xlabel('Lag')
    plt.ylabel('P-Value')
    plt.xticks(range(1, MAX_LAG + 1))
    plt.ylim(0, 0.2)
    plt.legend()
    plt.grid()
    plt.show(block=False)
