import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import os

# Get current script directory
script_dir = os.path.dirname(__file__)

# # Construct path to data folder
# data_folder = os.path.join(script_dir, '..', 'data')

# # Define CSV path
# csv_path = os.path.join(data_folder, 'trading_data.csv')

# # Example usage
ticker = 'nq=F'  # NQ futures symbol for Yahoo Finance
# start_date = '2024-01-01'
# end_date = '2025-04-11'
# data = yf.download(ticker, start=start_date, end=end_date)
# data.columns = data.columns.droplevel(1)  # Fix multi-index columns if needed

# # Calculate indicators
# data["EMA_9"] = data["Close"].ewm(span=9, adjust=False).mean()
# data["EMA_21"] = data["Close"].ewm(span=21, adjust=False).mean()
# data['Signal'] = 0
# data['Signal'][9:] = (data['EMA_9'][9:] > data['EMA_21'][9:]).astype(int)
# data['Position'] = data['Signal'].diff()

# print(f"Saving data to {csv_path}...")
# data.to_csv(csv_path, index=False)


# Construct path
csv_path = os.path.abspath(os.path.join(
    script_dir, 
    '..', 
    'data', 
    'nq=F trading_data.csv'
))

# Read the file
df = pd.read_csv(csv_path)
data = pd.DataFrame (df)

def calculate_trades(data):
    """
    Generate trades DataFrame based on EMA crossover signals.
    Returns DataFrame with columns:
    ['EntryDate', 'Type', 'EntryPrice', 'ExitDate', 'ExitPrice', 'PnL', 'Return']
    """
    trades = []
    position = None
    entry_price = None
    entry_date = None

    for i in range(1, len(data)):
        pos = data['Position'].iloc[i]
        close = data['Close'].iloc[i]
        date = data['Date'].iloc[i]

        if pos == 1 and position is None:  # Long (buy) signal
            position = 'long'
            entry_price = close
            entry_date = date
        elif pos == -1 and position is None:  # Short (sell) signal
            position = 'short'
            entry_price = close
            entry_date = date

        elif pos == -1 and position == 'long':  # Close long (sell) signal
            pnl = close - entry_price
            trades.append({
                'EntryDate': entry_date,
                'Type': 'long',
                'EntryPrice': entry_price,
                'ExitDate': date,
                'ExitPrice': close,
                'PnL': pnl,
                'Return': (pnl / entry_price) * 100
            })
            position = None
            entry_price = None
            entry_date = None

        elif pos == 1 and position == 'short':  # Close short (buy) signal
            pnl = entry_price - close
            trades.append({
                'EntryDate': entry_date,
                'Type': 'short',
                'EntryPrice': entry_price,
                'ExitDate': date,
                'ExitPrice': close,
                'PnL': pnl,
                'Return': (pnl / entry_price) * 100
            })
            position = None
            entry_price = None
            entry_date = None

    return pd.DataFrame(trades) if trades else pd.DataFrame()



def calculate_equity_curve(data, trades, initial_balance=100000, contract_size=20):
    """
    Calculate equity curve for futures trading.
    contract_size: NQ futures multiplier ($20 per index point)
    """
    data = data.copy()
    data["Equity"] = initial_balance
    data["PositionValue"] = 0
    data["Drawdown"] = 0.0
    data["InPosition"] = False

    if not trades.empty:
        current_cash = initial_balance
        active_position = None
        entry_price = None
        trade_index = 0
        running_peak = initial_balance
        nq_point_value = contract_size

        for i in range(len(data)):
            current_date = data['Date'].iloc[i] if 'Date' in data.columns else data.index[i]
            current_close = data["Close"].iloc[i]

            if trade_index < len(trades):
                current_trade = trades.iloc[trade_index]

                if current_date == current_trade["EntryDate"]:
                    active_position = current_trade["Type"]
                    entry_price = current_trade["EntryPrice"]

                elif current_date == current_trade["ExitDate"]:
                    if active_position == 'long':
                        pnl = (current_trade["ExitPrice"] - entry_price) * nq_point_value
                    else:  # short
                        pnl = (entry_price - current_trade["ExitPrice"]) * nq_point_value

                    current_cash += pnl
                    active_position = None
                    entry_price = None
                    trade_index += 1

            if active_position == 'long':
                position_value = (current_close - entry_price) * nq_point_value
            elif active_position == 'short':
                position_value = (entry_price - current_close) * nq_point_value
            else:
                position_value = 0

            current_equity = current_cash + position_value
            data.at[i, 'Equity'] = current_equity
            data.at[i, 'PositionValue'] = position_value
            data.at[i, 'InPosition'] = active_position is not None

            if active_position is not None:
                running_peak = max(running_peak, current_equity)
                drawdown = (current_equity - running_peak) / running_peak * 100
            else:
                running_peak = current_equity
                drawdown = 0.0

            data.at[i, 'Drawdown'] = drawdown

    data["DailyReturn"] = data["Equity"].pct_change() * 100
    total_return = (data["Equity"].iloc[-1] / initial_balance - 1) * 100

    return data, total_return


trades = calculate_trades(data)

equity_data, total_return = calculate_equity_curve(data, trades)

## Perfomrance metrics
num_trades = len(trades)
win_rate = 0
avg_trade_return = 0
profit_factor = np.inf
max_drawdown = 0

if num_trades > 0:
    win_rate = len(trades[trades['PnL'] > 0]) / num_trades * 100
    avg_trade_return = trades['Return'].mean()
    max_drawdown = equity_data['Drawdown'].min()

    losing_trades = trades[trades['PnL'] < 0]
    if len(losing_trades) > 0:
        profit_factor = (-trades[trades['PnL'] > 0]['PnL'].sum() / losing_trades['PnL'].sum())





def plot_strategy_performance(data, trades, equity_data, ticker, total_return, max_drawdown, 
                             win_rate, num_trades, avg_trade_return, profit_factor):
    """
    Plots the strategy performance with:
    - Price and indicators
    - Trade entries/exits
    - Equity curve
    - Drawdown
    """
    # Ensure 'Date' is datetime and set as index
    data['Date'] = pd.to_datetime(data['Date'])
    equity_data['Date'] = pd.to_datetime(equity_data['Date'])
    data.set_index('Date', inplace=True)
    equity_data.set_index('Date', inplace=True)
    

    # Also, ensure trades EntryDate/ExitDate are datetime
    if not trades.empty:
        trades['EntryDate'] = pd.to_datetime(trades['EntryDate'])
        trades['ExitDate'] = pd.to_datetime(trades['ExitDate'])


    plt.figure(figsize=(14, 10))
    plt.suptitle(f"{ticker} EMA Crossover Strategy Performance", y=1.02, fontsize=14)

    # Price and signals
    ax1 = plt.subplot(3, 1, 1)
    ax1.plot(data['Close'], label='Price', color='navy', alpha=0.8)
    ax1.plot(data['EMA_9'], label='EMA_9', color='blue', alpha=0.7, linewidth=1.5)
    ax1.plot(data['EMA_21'], label='EMA_21', color='darkorange', alpha=0.7, linewidth=1.5)

    # Plot trades
    if not trades.empty:
        for trade in trades.itertuples():
            color = 'green' if trade.PnL > 0 else 'red'
            ax1.plot([trade.EntryDate, trade.ExitDate],
                    [trade.EntryPrice, trade.ExitPrice],
                    color=color, alpha=0.3, linewidth=2)
            ax1.scatter(trade.EntryDate, trade.EntryPrice,
                       marker='^' if trade.Type == 'long' else 'v',
                       color=color, s=100)
            ax1.scatter(trade.ExitDate, trade.ExitPrice,
                       marker='o', color=color, s=50)
            ax1.text(trade.EntryDate, trade.EntryPrice, f'{trade.EntryPrice:.2f}',
                    fontsize=9, color='black', ha='center', va='bottom')
            ax1.text(trade.ExitDate, trade.ExitPrice, f'{trade.ExitPrice:.2f}',
                    fontsize=9, color='black', ha='center', va='bottom')

    ax1.set_ylabel('Price')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)

    # Equity curve
    ax2 = plt.subplot(3, 1, 2)
    ax2.plot(equity_data['Equity'], label='Equity Curve', color='purple', linewidth=2)
    ax2.fill_between(equity_data.index, 10000, equity_data['Equity'],
                    where=(equity_data['Equity'] >= 10000),
                    facecolor='green', alpha=0.2)
    ax2.fill_between(equity_data.index, 10000, equity_data['Equity'],
                    where=(equity_data['Equity'] < 10000),
                    facecolor='red', alpha=0.2)
    ax2.axhline(10000, color='black', linestyle='--', linewidth=0.8)
    ax2.set_ylabel('Account Balance ($)')
    ax2.grid(True, alpha=0.3)

    # Drawdown
    ax3 = plt.subplot(3, 1, 3)
    ax3.fill_between(equity_data.index, equity_data['Drawdown'], 0,
                    color='red', alpha=0.3)
    ax3.set_ylabel('Drawdown (%)')
    ax3.set_xlabel('Date')
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()

    # Performance summary
    metrics_text = (
        f"Performance Metrics:\n"
        f"Total Return: {total_return:.2f}%\n"
        f"Max Drawdown: {max_drawdown:.2f}%\n"
        f"Win Rate: {win_rate:.2f}%\n"
        f"Number of Trades: {num_trades}\n"
        f"Avg Trade Return: {avg_trade_return:.2f}%\n"
        f"Profit Factor: {profit_factor:.2f}"
    )
    plt.figtext(0.15, 0.85, metrics_text, bbox=dict(facecolor='white', alpha=0.5))
    plt.show()


plot_strategy_performance(data, trades, equity_data, ticker, total_return, max_drawdown, 
                             win_rate, num_trades, avg_trade_return, profit_factor)