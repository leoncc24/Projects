
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_ccf
from config import settings

def plot_ccf_analysis(data, target_var, features):
    """Plot Cross-Correlation for multiple features against target"""
    for var in features:
        # Align data
        aligned_data = data[[target_var, var]].dropna()
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 4))
        plot_ccf(aligned_data[target_var], aligned_data[var], 
                lags=settings.MAX_LAG, alpha=settings.SIGNIFICANCE_LEVEL, ax=ax)
        ax.set_title(f'CCF: {var} vs {target_var}')
        ax.grid(True)
        plt.tight_layout()
        plt.show()
