# Data Analysis Projects Portfolio

**Proof of my full-cycle analytics capabilities:**
- Data cleaning & transformation
- KPI development & tracking  
- Root-cause analysis  
- Executive-level storytelling  

**Skills Involved:**
- SQL
- R
- Python
- Power BI
- Tableau

---
## SQL Analysis

### 1. [World_Layoff_Data_Cleaning_EDA](https://github.com/leoncc24/Projects/tree/main/SQL_world_layoff)

**Goal**:
- Import and clean data from a csv file, then do Exploratory Data Analysis with aggregation function to find trend or insights from the data

Data Cleaning:
1. Remove Duplicates
2. Standardize the Data format
3. Handle Null values or blank values
4. Romve useless columns

Exploratory Data Analysis:
Dive deep into data to see below findings
- The most impacted industries
- The most impacted coutries
- World monthly laid off trend and pattern during data period
- Top 5 companies with most laid off each year

Tech Stack: 
- SQL, MySQL, Date_Format, CTE, Window Function

---

## Python Analysis

### 1. [Web scrap of HK Private Car Registration data](https://github.com/leoncc24/Projects/tree/main/Web_scarp_TD_Private_car)

**Goal**:
- Extract monthly data pf First Registration of Private Cars by Make, First Registration Vehicle Status, Fuel Type and Body Type from HK Transport Department (2018 to 2025)
- Extract the useful parts of the tables and combine the sheets into one single long format of table
- Data cleaning by reconstruct, rename, string stripping
- Write into new csv and excel for further analysis

Methods:
- Combine requests and bs4 to loop thought each monthly data pages to download the data tables
- Parse webpages HTML and use regular expression to identify the herfs
- Use Pandas to read multi-level index, reshape them into single level headers
- Combine all sheets into one table using concat
- Use melt to unpivot the table into long format

Tech Stack: 
- pandas, requests, bs4(BeautifulSoup), io , re(regular expression), datetime


### 2. [EMA Trading Signal Generator](https://github.com/leoncc24/Projects/tree/main/EMA_Trading_Signal)

**Goal**:
- Using typical exponential moving average crossover as trading strategy to test the return on trading nasdaq future

Key Metrics:
- Realised return: 46.52% (vs 12.57% buy-and-hold)
- Maximum drawdown: 13.78%
- Profit Factor: 2.6

Tech Stack: 
- pandas, numpy, matplotlib


### 3. [S&P 500 Macroeconomic Analysis](https://github.com/leoncc24/Projects/tree/main/sp500_with_macro)

**Goal**:
- Extract S&P500 price and US Macroeconomic data from 1981 to 2021
- Analyze their relationship, lead-lag dynamics, and prediction power
- Highlighting the potential insights and implications for financial forecasting

Methods:
- Correlation Analysis: Plots heatmaps to visualize relationships between variables.
- Cross-Correlation Function (CCF) Analysis: Examines lead-lag relationships.
- Granger Causality Tests: Identifies variables that help predict S&P 500 returns.
- Feature Selection: Finds the best combination of predictors for S&P 500 returns.
- VAR Modeling: Trains a Vector Autoregression model for multivariate time series forecasting.
- Visualization: Provides multi-series plots with event overlays.

Key Findings:
- Normalized GDP, D1_D12_log_CPI, and 10Y_yield_diff among all variables make the best prediction for SP500 Return in VAR model with RMSE 0.04099
- During non-recession period, only interest rates(10-year treasury yield) and personal saving rates at shorter lags(1-9months) to predict S&P500, indicating that monetary policy and consumer behavior dominate in stable markets
- Markets anticipate economic shifts, especially during downturns, markets react earlier (6-12 months) than the macro variables during and close to Recession Periods

Tech Stack: 
- pandas, numpy, matplotlib, statsmodels, seaborn

---

## R Analysis

### 1. [Bellabeat Smart Device Usage Analysis](https://github.com/leoncc24/Projects/tree/main/R_Bellabeat_Case_Study)

**Goal**:
- Analyze FitBit Fitness Tracker Data to identify trends in smart device usage and provide recommendations for improving Bellabeat’s marketing strategy

Key Findings:
- Sleep Patterns: ~50% of days showed average sleep below the recommended 7 hours.
- Physical Activity: >50% of users classified as low active or sedentary (<7,500 steps/day); ~33% of days below recommended step count.
- Device Engagement: 6% of users frequently used devices (21–31 days), 69% regular (10–20 days), 26% occasional (<10 days).

Tech Stack: 
- R, tidyverse, janitor, lubridate, dplyr, ggplot2, tidyr, scales

---

## Tableau Dashboard

### 1. [Hong Kong Auto Market and comparison between TESLA and BYD](https://github.com/leoncc24/Projects/tree/main/Tableau_Tesla_BYD_HK_EV_Market)
Remark:
Data used is from the Python Project - Web scrab of HK Prviate Car Registration data

**Goal**:
-Summarize and visualize Hong Kong Private Car Registration data, identify the distribution and trend of the market

-Dive deep into Tesla and BYD, comparing, both revenue, sale and market share

Feature:
- Sankey extension to show overall private car, fuel, body, brand distribution
- Line chart show yearly petrol vs electric trend
- Year filter to interact with the charts
- Dual axis line and circle chart to highlight min/max
- Nagviation Page Buttons

  
### 2. [Private Project - Company Product Ticket Dashboard]

Remark:
Data is not completly anonymized, therefore this repo is only limited access

**Goal**:
-Summarize and visulaize ticket data, identify the highly frequent and long handling hour problem, to improve service operations and product reliability

Feature:
- Overall issue ticket card summary
- Line chart show monthly ticket trend
- Map with color density show ticket density and locations
- Visualizes aggregated metrics by ticket category
- In-depth level charts to see the number of tickets and handling hours due to differen levels of product faulty
- Nagviation Page Buttons 

---

## Power BI Dashboards

### 1. [Hotel Revenue Performance Dashboard](https://github.com/leoncc24/Projects/tree/main/Power_BI_Hotel_Revenue)
**Goal**: 
-Analyze 3 months of booking data across multiple hotel properties to optimize hospitality KPIs

**Key Features**:
- Tracked **RevPAR** (Revenue Per Available Room), **ADR** (Average Daily Rate), and occupancy rates
- Dynamic filters for property/location comparisons
- Cancellation trend analysis with drill-down capabilities

**Skills**: 
DAX, data modeling, time intelligence functions  

**Insights**:
- Found opportunity in pricing strategy based on high occupany rate that can lead at least 7-15% Revenue
- Identified the root causes of the bad-performance hotels is mainly due to inflexible ADR pricing strategy


### 2. [Credit Card Customer Segmentation](https://github.com/leoncc24/Projects/tree/main/Power_BI_Credit_Card)
**Goal**: 
-Profile 4,000 customers across 5 cities to identify high-value credit card users 

**Key Features**:
- Occupation analysis
- Spending patterns targeting
- Customer spending trend

**Skills**: 
Clustering, Power Query transformations, page navigation

**Insights**:
- Identified target customer cluster since salaried IT Employees spend 130% more than the average spending among all occupation, while other occupation spend less than the average
- Target customer spending practice (e.g. Bills, Groceries and Electronics) to incentivize them to use credit card in these areas


### 3. [Personal Finance Dashboard](https://github.com/leoncc24/Projects/tree/main/Power_BI_Finance_Dashboard)
**Goal**: 
Visualize years of income/expense data for budgeting insights

**Key Features**:
- Monthly cash flow trends
- Expense category breakdowns
- Savings rate strategy

**Skills**: 
-Time-series visualization

**Insights**:
- Recognized bad spending practice (e.g. spend more when earn more)
- Identified improvement of saving rate which was below the target rate most of the time (e.g. save first then spend)


### 3. [Digital Marketing Dashboard](https://github.com/leoncc24/Projects/tree/main/Power_BI_Digital_Marketing_Performance_Dasboard)
**Goal**: 
Visualize 3 years of E-commerce digital marketing data for marketing and service improvement insights

**Key Features**:
- Monthly performace trends
- Customer review rating and sentiment breakdowns
- Key metircs by product analysis

**Skills**: 
-Time-series visualization

**Insights**:
- Recognized high-performance prodcut categories, suggest implement seasonal promotions during peak months (Januray & September)
- Address mixed and negative feedback, analyze those reviews to identift common issues, aiming to move average rating to 4.0 target
  
---

```
## Project Files Structure
Projects/
├── Power_BI_Hotel_Revenue/
├── Power_BI_Credit_Card/
├── Power_BI_Finance_Dashboard/
├── Power_BI_Digital_Marketing_Performance_Dasboard
├── EMA_Trading_Signal/
├── SP500_Macro/
├── SQL_world_layoff/
├── Tableau_Tesla_BYD_HK_EV_Market
├── Web_scarp_TD_Private_car
└── R_Bellabeat_Case_Study/
```
