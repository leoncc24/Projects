# Hong Kong Private Car Registration Scraper


## Overview
This project is a Python-based web scraper designed to extract private car registration data from the Hong Kong Transport Department's Monthly Traffic and Transport Digest. 
It collects data from Table 4.1(e), processes Excel files with multi-level headers, and combines the data into a single DataFrame, which is saved as both CSV and Excel files. 
The data is also transformed into a long-format CSV for easier analysis


## Features

- Scrapes monthly digest URLs from the Hong Kong Transport Department website.
- Downloads and processes Excel files containing private car registration data.
- Handles multi-level headers and indices in Excel files.
- Cleans data by removing Chinese characters and standardizing labels.
- Combines data from multiple months into a single dataset.
- Saves output in CSV and Excel formats, with an additional transformed (melted) CSV for analysis.


## Requirements

- To run this project, you need the following Python libraries:
- requests
- beautifulsoup4
- pandas
- xlrd (for .xls files)
- openpyxl (for .xlsx files)

Install them using pip:
   ```bash
   pip install requests beautifulsoup4 pandas xlrd openpyxl
   ```

- Visual Studio (optional)

- Git (for cloning)


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/leoncc24/Web_scarp_TD_Private_car.git 
   cd Web_scarp_TD_Private_car
   ```

2. Run the script:
   ```bash
   python EV_auto.py
   ```

3. Output files:
   - hk_private_cars_registration_combined.csv: Combined raw data in wide format.
   - hk_private_cars_registration_combined.xlsx: Same data in Excel format.
   - hk_private_cars_registration_transformed.csv: Transformed data in long format (melted for easier analysis).


## How It Works

1. URL Scraping: The script fetches URLs for monthly digests from the Transport Department's index page.

2. Excel Download: For each month, it locates and downloads the Excel file for Table 4.1(e) (Private Car Registrations).

3. Data Extraction: Processes Excel sheets with multi-level headers, cleans labels, and standardizes data.

4. Data Combination: Combines data from all months into a single DataFrame.

5. Data Transformation: Melts the data into a long format, with columns for Make, Status, Year-Month, Fuel_Body, and Registrations.

6. Output: Saves the combined and transformed data to CSV and Excel files.


## File Structure

scraper.py: Main Python script containing the scraping and processing logic.

hk_private_cars_registration_combined.csv: Output file with raw combined data.

hk_private_cars_registration_combined.xlsx: Same as above, in Excel format.

hk_private_cars_registration_transformed.csv: Transformed data in long format.


## Notes

The script handles both .xls and .xlsx files using appropriate engines (xlrd for .xls, openpyxl for .xlsx).

Error handling is implemented to skip problematic files or sheets and continue processing.

The transformed CSV is ideal for analysis in tools like R, Python, or visualization software.

