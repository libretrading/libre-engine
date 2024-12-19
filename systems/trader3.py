from alpaca_api import functions as api
from datetime import datetime
import pandas as pd
from historical_data.datamanager import DATA_CSV_PATH
from postgresql.postgremanager import *

"""
Long mean reverting rsi system on VSS daily
2007 TO 2024 OPTIMIZED RSI 4 LONG 25 FLAT 70
EMA20 > EMA50 FILTER
requirements "TRADER SUBSCRIPTION"
"""

### UTILS ###

TICKER = 'VSS'

### INDICATORS ###

# Function to calculate RSI
def calculate_rsi(data, ticker, window=4):
    delta = data[ticker].diff()  # Calculate the difference in price
    gain = delta.where(delta > 0, 0)  # Positive gains
    loss = -delta.where(delta < 0, 0)  # Negative losses (absolute value)
    
    # Calculate rolling mean of gains and losses
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    
    # Handle division by zero
    rs = avg_gain / avg_loss.replace(0, 1)  # Replace loss=0 with 1 to avoid division by zero
    
    rsi = 100 - (100 / (1 + rs))
    
    return rsi.iloc[-1]

# Function to calculate MA
def calculate_ema(data, ticker, window):
    """
    Calculate the Exponential Moving Average (EMA) of a given ticker's price data.
    
    Parameters:
    - data: pandas DataFrame containing the price data.
    - ticker: The column name (string) of the specific ticker in the DataFrame.
    - window: The lookback period for the EMA (default is 10).
    
    Returns:
    - A pandas Series representing the EMA of the specified ticker.
    """
    ema = data[ticker].ewm(span=window, adjust=False).mean()
    return ema.iloc[-1]



### EXECUTION ###

# 15:00 AM Check: Execute strategy for accounts without positions TEST PASSED
def daily_1500_check_and_execute():
    print(f"[{datetime.now()}] Performing daily 10:30 AM check...")

    # Load the historical data
    data = pd.read_csv(DATA_CSV_PATH, index_col=0, parse_dates=True)

    # Fetch the latest Alpaca prices and update the last data point
    
    latest_price = api.fetch_alpaca_latest_price(TICKER)

    if latest_price:
        data.loc[datetime.now().replace(hour=0, minute=0, second=0, microsecond=0), TICKER] = latest_price  # Add the latest price as today's data point

    # Calculate the momentum scores using the updated data
    rsi = calculate_rsi(data, TICKER)
    ema20 = calculate_ema(data, TICKER, 20)
    ema50 = calculate_ema(data, TICKER, 50)
    size = 0.25  # % of equity

    # Fetch active accounts
    active_accounts = get_active_accounts()

    # check conditions and execute
    # buy condition check
    if rsi < 25 and ema20 > ema50:
        print(f"rsi={rsi}, ema20={ema20}, ema50={ema50}, buy condition met")
        # buy loop
        for account in active_accounts:
            current_position = api.has_open_position(account, TICKER)
            if not current_position:
                equity = api.get_account_equity(account)
                if equity:
                    print(f"Account {account['email']} has equity: {equity}")
                    positionsize = round(equity*size, 2)
                    api.place_order(account, TICKER, positionsize)              
            else:
                print(f"Account {account['email']} already holds {current_position}. Skipping execution.")
    # sell condition check
    elif rsi > 70:
        print(f"rsi={rsi}, sell condition met")
        # sell loop
        for account in active_accounts:
            current_position = api.has_open_position(account, TICKER)
            if current_position:
                api.liquidate_position(account, TICKER)              
            else:
                print(f"Account {account['email']} is not holding {current_position}. No liquidation needed.")
    else:
        print('rsi={rsi}, ema20={ema20}, ema50={ema50}, buy/sell conditions not met, no action needed')
