from alpaca_api import functions as api
from datetime import datetime
import pandas as pd
from historical_data.datamanager import DATA_CSV_PATH
from postgresql.postgremanager import *

"""
accelerating dual momentum system 100% of equity
1 3 6 month selecting highest between us and smallcap-em-exus
every last trading day of month
if none is positive select highest roc21 between
tlt and uup
requirements "TRADER SUBSCRIPTION"
"""

### UTILS ###

TICKERS = ['QQQE', 'EFA', 'TLT', 'UUP', 'IEI']

### INDICATORS ###

# Calculate the momentum scores based on ROC (Rate of Change) TEST PASSED
def calculate_momentum(data):
    roc_21 = data.pct_change(21, fill_method=None)
    roc_63 = data.pct_change(63, fill_method=None)
    roc_126 = data.pct_change(126, fill_method=None)
    
    momentum_scores = (roc_21 + roc_63 + roc_126) / 3
    return momentum_scores.iloc[-1]  # Return latest momentum scores for the last day in the data

### EXECUTION ###

# 10:30 AM Check: Execute strategy for accounts without positions TEST PASSED
def daily_1030_check_and_execute():
    print(f"[{datetime.now()}] Performing daily 10:30 AM check...")

    # Load the historical data
    data = pd.read_csv(DATA_CSV_PATH, index_col=0, parse_dates=True)

    # Fetch the latest Alpaca prices and update the last data point
    for ticker in TICKERS:
        latest_price = api.fetch_alpaca_latest_price(ticker)
        if latest_price:
            data.loc[datetime.now().replace(hour=0, minute=0, second=0, microsecond=0), ticker] = latest_price  # Add the latest price as today's data point

    # Calculate the momentum scores using the updated data
    momentum_scores = calculate_momentum(data)

    # Apply system rules to determine which asset to buy
    QQQE_momentum = momentum_scores['QQQE']
    EFA_momentum = momentum_scores['EFA']
    IEI_momentum = momentum_scores['IEI']

    if QQQE_momentum > EFA_momentum and QQQE_momentum > IEI_momentum and QQQE_momentum > 0:
        target_ticker = 'QQQE'
    elif EFA_momentum > QQQE_momentum and EFA_momentum > IEI_momentum and  EFA_momentum > 0:
        target_ticker = 'EFA'
    else:
        TLT_momentum = data['TLT'].pct_change(21, fill_method=None)
        UUP_momentum = data['UUP'].pct_change(21, fill_method=None)
        target_ticker = 'TLT' if TLT_momentum.iloc[-1] > UUP_momentum.iloc[-1] else 'UUP'

    print(f"Target ticker based on momentum: {target_ticker}")

    # Fetch active accounts
    active_accounts = get_active_accounts()

    # Check if there are any active accounts
    if not active_accounts:
        print(f"No active accounts found in the database. Skipping execution.")
        return  # Return early to avoid stopping the script

    # Execute strategy only for accounts without any open positions in the 4 tickers
    for account in active_accounts:
        current_position = api.has_open_position(account, TICKERS)
        if not current_position:
            execute_strategy(account, target_ticker)
        else:
            print(f"Account {account['email']} already holds {current_position}. Skipping execution.")

# weekly execute TEST PASSED
def weekly_execute():
    print(f"[{datetime.now()}] Performing monthly executions")

    # Load the historical data
    data = pd.read_csv(DATA_CSV_PATH, index_col=0, parse_dates=True)

    # Fetch the latest Alpaca prices and update the last data point
    for ticker in TICKERS:
        latest_price = api.fetch_alpaca_latest_price(ticker)
        if latest_price:
            data.loc[datetime.now().replace(hour=0, minute=0, second=0, microsecond=0), ticker] = latest_price  # Add the latest price as today's data point

    # Calculate the momentum scores using the updated data
    momentum_scores = calculate_momentum(data)

    # Apply system rules to determine which asset to buy
    QQQE_momentum = momentum_scores['QQQE']
    EFA_momentum = momentum_scores['EFA']
    IEI_momentum = momentum_scores['IEI']

    if QQQE_momentum > EFA_momentum and QQQE_momentum > IEI_momentum and QQQE_momentum > 0:
        target_ticker = 'QQQE'
    elif EFA_momentum > QQQE_momentum and EFA_momentum > IEI_momentum and  EFA_momentum > 0:
        target_ticker = 'EFA'
    else:
        TLT_momentum = data['TLT'].pct_change(21, fill_method=None)
        UUP_momentum = data['UUP'].pct_change(21, fill_method=None)
        target_ticker = 'TLT' if TLT_momentum.iloc[-1] > UUP_momentum.iloc[-1] else 'UUP'

    print(f"Target ticker based on momentum: {target_ticker}")

    # Execute strategy for all accounts
    for account in get_active_accounts():
        execute_strategy(account, target_ticker)

# Execute the strategy based on momentum scores TEST PASSED
def execute_strategy(account, ticker):
    # Checking if and wich of the tickers is open
    # the system is structured to have only one position in one of the 4 tickers at a time
    # so the has_open_position will be fine
    current_position = api.has_open_position(account, TICKERS)
    
    # If there's no open position or the current position is not the target ticker, proceed
    if not current_position:
        print(f"No position open for account {account['email']}.")
    elif current_position == ticker:
        print(f"{ticker} is already open. No action needed.")
        return
    else:
        print(f"Liquidating {current_position} to open a new position in {ticker}.")
        api.liquidate_position(account, current_position)

    # Get account equity to place the new order
    equity = api.get_account_equity(account)
    if equity:
        print(f"Account {account['email']} has equity: {equity}")
        api.place_order(account, ticker, equity)