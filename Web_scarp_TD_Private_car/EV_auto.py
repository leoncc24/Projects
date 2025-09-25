import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import BytesIO
import re
from datetime import datetime

# Base URL for the site
BASE_URL = "https://www.td.gov.hk"

# URL of the index page
INDEX_URL = "https://www.td.gov.hk/en/transport_in_hong_kong/transport_figures/monthly_traffic_and_transport_digest/index.html"

def clean_label(label):
    """Remove Chinese characters and newlines, keep English."""
    if isinstance(label, str):
        return re.sub(r'[\u4e00-\u9fff]+\s*\n?', '', label).strip()
    return label

def get_monthly_urls(index_url):
    """
    Scrape the index page to get all available monthly digest URLs.
    """
    response = requests.get(index_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    
    monthly_urls = []
    links = soup.find_all('a', href=re.compile(r'/en/transport_in_hong_kong/transport_figures/monthly_traffic_and_transport_digest/\d{4}/\d{6}/index\.html'))
    
    for link in links:
        href = link['href']
        full_url = BASE_URL + href if href.startswith('/') else href
        match = re.search(r'(\d{4})/(\d{6})', href)
        if match:
            year = int(match.group(1))
            month_num = int(match.group(2)[-2:])  # Last two digits for month
            month_name = link.text.strip()
            monthly_urls.append({
                'url': full_url,
                'year': year,
                'month': month_num,
                'month_name': month_name
            })
    
    monthly_urls.sort(key=lambda x: (x['year'], x['month']), reverse=True)
    return monthly_urls

def read_excel_with_multiheader(xls, sheet_name, engine):
    """
    Read sheet with multi-level headers and index, clean labels, handle Total.
    """
    # Read with multi-level header and index, skipping first 4 rows
    df = pd.read_excel(
        xls,
        sheet_name=sheet_name,
        engine=engine,
        header=[0, 1],  # Fuel (level 0) and Body (level 1) after skiprows
        index_col=[0, 1],  # Make (level 0) and Status (level 1)
        skiprows=4
    )

    # Clean column MultiIndex
    df.columns = pd.MultiIndex.from_tuples([
        tuple(clean_label(level) for level in col) for col in df.columns
    ])

    # Identify and separate Total column
    total_col = None
    for col in df.columns:
        if 'Total' in col[1]:
            total_col = col
            break
    
    if total_col:
        df_total = df[total_col].astype(int, errors='ignore')
        df = df.drop(columns=[total_col])

    # Reset index to make Make and Status columns
    df = df.reset_index()
    df.columns = ['Make', 'Status'] + list(df.columns[2:])

    # Clean row index (Make and Status)
    df['Make'] = df['Make'].ffill().apply(clean_label)
    df['Status'] = df['Status'].apply(clean_label)

    # Filter valid Status rows (exclude footers)
    df = df[df['Status'].isin(['A', 'B', 'C1', 'C2', 'Others'])]

    # Convert numeric columns to int
    for col in df.columns[2:]:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    # Add Total back
    if total_col:
        df['Total'] = df_total.reindex(df.index).fillna(0).astype(int)

    return df

def download_and_extract_excel(monthly_url, year, month):
    """
    Find Excel link for Table 4.1(e), download, and return dict of DataFrames with Year/Month.
    """
    response = requests.get(monthly_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find Table 4.1(e) link
    rows = soup.find_all('tr', class_='TLevel4')
    excel_href = None
    for row in rows:
        tds = row.find_all('td')
        if len(tds) >= 3 and tds[0].text.strip() == 'Table 4.1 (e)':
            if 'First Registration of Private Cars' in tds[1].text:
                link = tds[2].find('a', href=re.compile(r'table41e\.(xls|xlsx)$'))
                if link:
                    excel_href = link['href']
                    break
                else:
                    link = tds[3].find('a', href=re.compile(r'table41e\.(xls|xlsx)$'))
                    if link:
                        excel_href = link['href']
                        break
    if not excel_href:
        print(f"No Excel link found for {year}-{month:02d}")
        return None
    
    excel_url = BASE_URL + excel_href if excel_href.startswith('/') else excel_href
    
    try:
        excel_response = requests.get(excel_url, timeout=10)
        excel_response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to download Excel for {year}-{month:02d}: {e}")
        return None
    
    file_ext = excel_href.split('.')[-1].lower()
    engine = 'xlrd' if file_ext == 'xls' else 'openpyxl'
    
    try:
        xls = pd.ExcelFile(BytesIO(excel_response.content), engine=engine)
        sheet_dfs = {}
        for sheet_name in xls.sheet_names:
            try:
                df = read_excel_with_multiheader(xls, sheet_name, engine)
                if not df.empty:
                    df['Year-Month'] = pd.Period(f"{year}-{month:02d}", freq='M')
                    sheet_dfs[sheet_name] = df
            except Exception as e:
                print(f"Error reading sheet '{sheet_name}' for {year}-{month:02d}: {e}")
                continue
        print(f"Extracted {len(sheet_dfs)} sheets for {year}-{month:02d}")
        return sheet_dfs
    except Exception as e:
        print(f"Error processing Excel for {year}-{month:02d}: {e}")
        return None

def combine_all_data(monthly_urls):
    """
    Combine all sheets from all months into one DataFrame.
    """
    all_dfs = []
    
    for entry in monthly_urls:
        sheet_dfs = download_and_extract_excel(entry['url'], entry['year'], entry['month'])
        if sheet_dfs:
            for sheet_name, df in sheet_dfs.items():
                df = df.reset_index(drop=True)  # Clean index for concat
                all_dfs.append(df)
    
    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        return combined_df
    return pd.DataFrame()

if __name__ == "__main__":
    print("Fetching monthly URLs...")
    monthly_urls = get_monthly_urls(INDEX_URL)
    print(f"Found {len(monthly_urls)} monthly digests.")
    
    print("Downloading and extracting data...")
    combined_df = combine_all_data(monthly_urls)
    
    if not combined_df.empty:
        print(f"Combined DataFrame shape: {combined_df.shape}")
        print("\nSample data:")
        print(combined_df.head())
        
        # Save to CSV and Excel
        combined_df.to_csv('hk_private_cars_registration_combined.csv', index=False)
        combined_df.to_excel('hk_private_cars_registration_combined.xlsx', index=False, engine='openpyxl')
        print("\nData saved to 'hk_private_cars_registration_combined.csv' and '.xlsx'")
        # Read the CSV file
        df = pd.read_csv('hk_private_cars_registration_combined.csv')  # Replace with your CSV file path

        # Clean and rename columns: handle MultiIndex, remove '\n', spaces, parentheses, and quotes
        df.columns = [
            col.replace(' ', '_').replace('(', '').replace(')', '').replace("'", '').replace(",", '').replace("_\n","_")
            for col in df.columns
        ]

        id_vars = ['Make', 'Status','Year-Month']
        df = pd.melt(
            df,
            id_vars=id_vars,
            value_vars=[col for col in df.columns if col not in id_vars],
            var_name='Fuel_Body',
            value_name='Registrations'
        )

        df.to_csv('hk_private_cars_registration_transformed.csv', index=False)
        print('Completed Transformation')
      