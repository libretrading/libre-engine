import os
import pytz
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# General Configuration
TICKERS = ['QQQE', 'EFA', 'TLT', 'UUP', 'IEI']
DATA_CSV_PATH = 'historical_data/historical_data.csv'
LAST_UPDATE_LOG = 'historical_data/last_update_log.txt'

# DATABASE MAINTENANCE: Download data if not exists, or update it TEST PASSED
def get_last_update():
    """Reads the last update date from the log file."""
    if os.path.exists(LAST_UPDATE_LOG):
        with open(LAST_UPDATE_LOG, 'r') as f:
            last_update = f.read().strip()
            return pd.Timestamp(last_update)
    return None


def set_last_update(date):
    """Writes the last update date to the log file."""
    with open(LAST_UPDATE_LOG, 'w') as f:
        f.write(date.strftime('%Y-%m-%d'))


def update_database():
    # Get timezone-aware current time
    now = datetime.now(pytz.timezone('America/New_York'))
    today = now.strftime('%Y-%m-%d')
    one_year_ago = now - timedelta(days=365)
    
    last_update = get_last_update()
    
    if last_update is None:
        # First time running, download one year of data
        print("No previous updates found. Downloading one year of data...")
        data = yf.download(TICKERS, start=one_year_ago, end=today)['Close']
        data.to_csv(DATA_CSV_PATH)
        set_last_update(now)  # Set last update to today
    else:
        # Check if last_update is timezone-naive and localize it
        if last_update.tzinfo is None:
            last_update = last_update.tz_localize('America/New_York')
        else:
            # If it's already timezone-aware, convert it
            last_update = last_update.tz_convert('America/New_York')
        
        # Calculate the start date for the missing data
        last_update_date = last_update.strftime('%Y-%m-%d')
        missing_days = (now - last_update).days

        if missing_days > 0:
            # If there are missing days, download the missing data
            print(f"Fetching data from {last_update_date} to {today}...")
            new_data = yf.download(TICKERS, start=last_update_date, end=today)['Close']
            
            if os.path.exists(DATA_CSV_PATH):
                # Append new data to the existing CSV
                data = pd.read_csv(DATA_CSV_PATH, index_col=0, parse_dates=True)
                new_data.index = pd.to_datetime(new_data.index)
                updated_data = pd.concat([data, new_data])
                updated_data.to_csv(DATA_CSV_PATH)
            else:
                # If the CSV does not exist, save the new data directly
                new_data.to_csv(DATA_CSV_PATH)

            # Update the last update date to today
            set_last_update(now)
        else:
            print("Data is already up-to-date. No need to fetch new data.")

    # Maintain only the last year of data
    data = pd.read_csv(DATA_CSV_PATH, index_col=0, parse_dates=True)
    data = data[data.index >= pd.Timestamp(one_year_ago)]
    data.to_csv(DATA_CSV_PATH)