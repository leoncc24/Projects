# Data Analysis Projects Portfolio

*Proof of my **full-cycle analytics capabilities**:*
▸ Data cleaning & transformation  
▸ KPI development & tracking  
▸ Root-cause analysis  
▸ Executive-level storytelling  


---

## Power BI Dashboards

### 1. [Hotel Revenue Performance Dashboard](https://github.com/leoncc24/Projects/tree/main/Power_BI_Hotel_Revenue)
**Goal**: Analyze 3 months of booking data across multiple hotel properties to optimize hospitality KPIs.  
**Key Features**:
- Tracked **RevPAR** (Revenue Per Available Room), **ADR** (Average Daily Rate), and occupancy rates
- Dynamic filters for property/location comparisons
- Cancellation trend analysis with drill-down capabilities

**Skills**: DAX, data modeling, time intelligence functions  
**Insights**:
- Found opportunity in pricing strategy based on high occupany rate that can lead at least 7-15% Revenue
- Identified the root causes of the bad-performance hotels is mainly due to inflexible ADR pricing strategy

---

### 2. [Credit Card Customer Segmentation](https://github.com/leoncc24/Projects/tree/main/Power_BI_Credit_Card)
**Goal**: Profile 4,000 customers across 5 cities to identify high-value credit card users.  
**Key Features**:
- Occupation analysis
- Spending patterns targeting
- Customer spending trend

**Skills**: Clustering, Power Query transformations, page navigation
**Insights**:
- Identified target customer cluster since salaried IT Employees spend 130% more than the average spending among all occupation, while other occupation spend less than the average
- Target customer spending practice (e.g. Bills, Groceries and Electronics) to incentivize them to use credit card in these areas

---

### 3. [Personal Finance Dashboard](https://github.com/leoncc24/Projects/tree/main/Power_BI_Finance_Dashboard)
**Goal**: Visualize years of income/expense data for budgeting insights.  
**Key Features**:
- Monthly cash flow trends
- Expense category breakdowns
- Savings rate strategy

**Skills**: Time-series visualization
**Insights**:
- Recognized bad spending practice (e.g. spend more when earn more)
- Identified improvement of saving rate which was below the target rate most of the time (e.g. save first then spend)

---

## Python Analyses

### 1. [EMA Trading Signal Generator](https://github.com/leoncc24/Projects/tree/main/EMA_Trading_Signal)
Key Metrics:

Realised return: 46.52% (vs 12.57% buy-and-hold)

Maximum drawdown: 13.78%

Profit Factor: 2.6

Tech Stack: pandas, numpy, matplotlib



### 2. [S&P 500 Macroeconomic Analysis](https://github.com/leoncc24/Projects/tree/main/sp500_with_macro)
Methods:

-Correlation Analysis: Plots heatmaps to visualize relationships between variables.
-Cross-Correlation Function (CCF) Analysis: Examines lead-lag relationships.
-Granger Causality Tests: Identifies variables that help predict S&P 500 returns.
-Feature Selection: Finds the best combination of predictors for S&P 500 returns.
-VAR Modeling: Trains a Vector Autoregression model for multivariate time series forecasting.
-Visualization: Provides multi-series plots with event overlays.

Key Findings:

-Normalized GDP, D1_D12_log_CPI, and 10Y_yield_diff among all variables make the best prediction for SP500 Return in VAR model with RMSE 0.04099

-During non-recession period, only interest rates(10-year treasury yield) and personal saving rates at shorter lags(1-9months) to predict S&P500, indicating that monetary policy and consumer behavior dominate in stable markets

-Markets anticipate economic shifts, especially during downturns, markets react earlier (6-12 months) than the macro variables during and close to Recession Periods


Tech Stack: pandas, numpy, matplotlib, statsmodels, seaborn


## Projecct Structure
Projects/
├── Power_BI_Hotel_Revenue/
├── Power_BI_Credit_Card/
├── Power_BI_Finance_Dashboard/
├── EMA_Trading_Signal/
└── SP500_Macro/
