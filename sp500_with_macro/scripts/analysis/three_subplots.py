import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from config import settings




def plot_three_series_with_events(data, series_names, events=settings.EVENTS, title="Market Indicators"):
    """Plot three series with recession shading and events"""
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12), sharex=True)
    
    # Plot each series
    for ax, col, color in zip([ax1, ax2, ax3], series_names, ['#1f77b4', 'cyan', 'black']):
        ax.plot(data.index, data[col], color=color, alpha=0.8, label=col)
        ax.set_ylabel(col)
        ax.legend(loc='upper left')
        ax.grid(which='both', linestyle='--', alpha=0.3)
        
        # Add recession shading
        for start, end in settings.RECESSION_PERIODS:
            ax.axvspan(start, end, color='gray', alpha=0.15)
    
    # Format x-axis
    ax3.xaxis.set_major_locator(mdates.YearLocator(5))
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax3.set_xlim(datetime(1980, 1, 1), datetime(2021, 12, 31))

    for ax in [ax1, ax2, ax3]:
        for name, date in events.items():
            ax.axvline(date, color='red', linestyle=':', alpha= 0.3)
            if ax == ax1:  # Label only once
                ax.text(date, ax.get_ylim()[1]*0.9, name, 
                       rotation=90, va='top', ha='right', alpha=0.7)
    
    plt.suptitle(title)
    plt.tight_layout()
    plt.show()
