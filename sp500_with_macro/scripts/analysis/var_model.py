import numpy as np
import pandas as pd
from statsmodels.tsa.api import VAR
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot as plt

def train_var_model(data, target_var, features):
    """Train and evaluate VAR model"""
    # Prepare data
    data = data.dropna()
    split_date = data.index[int(0.8*len(data))]
    train = data.loc[:split_date, [target_var] + features]
    test = data.loc[split_date:, [target_var] + features]

    # Model selection
    model = VAR(train)
    lag_order = model.select_order(maxlags=1)
    best_lag = lag_order.aic  # Or bic/hqic
    print(f"Optimal lags: {best_lag}")
    
    # Model fitting
    var_model = VAR(train)
    results = var_model.fit(best_lag)
    
    # Forecasting
    lagged_values = train.values[-best_lag:]
    predictions = []
    actuals = test[target_var].tolist()
    
    for t in range(len(test)):
        yhat = results.forecast(y=lagged_values, steps=1)[0, 0]
        predictions.append(yhat)
        lagged_values = np.vstack([lagged_values[1:], test.iloc[t].values])
    
    pred_series = pd.Series(predictions, index=test.index)
    
    # Evaluation
    rmse = np.sqrt(mean_squared_error(actuals, predictions))
    nrmse = rmse / (data[target_var].max() - data[target_var].min())
    
    return {
        'model': results,
        'predictions': pred_series,
        'actuals': test[target_var],
        'train': train[target_var],
        'rmse': rmse,
        'nrmse': nrmse,
        'best_lag': best_lag
    }

def plot_var_results(results):
    """Plot VAR model results"""
    plt.figure(figsize=(12, 6))
    plt.plot(results['train'], label='Train')
    plt.plot(results['actuals'], label='Actual')
    plt.plot(results['predictions'], label='Predicted', linestyle='--')
    plt.title(f'S&P 500 Returns Prediction (RMSE={results["rmse"]:.4f})')
    plt.legend()
    plt.show()
