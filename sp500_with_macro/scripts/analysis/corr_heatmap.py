import seaborn as sns
import matplotlib.pyplot as plt



def plot_correlation_heatmap(data, variables):
    """Plot correlation heatmap for selected variables"""
    corr_matrix = data[variables].corr()
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title("Feature Correlation Matrix")
    plt.xticks(rotation=30)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()

