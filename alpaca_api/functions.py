import requests
from datetime import datetime, timedelta
import pytz
import pandas as pd
# Load the API keys from the .env file
import os
from dotenv import load_dotenv
load_dotenv()

API_PUBLIC = os.getenv("API_PUBLIC")
API_SECRET = os.getenv("API_SECRET")

### ACCOUNT MANAGEMENT FUNCTIONS ###
# Check if the account has any open positions in the tickers TEST PASSED
def has_open_position(account, tickers):
    # URLs for live and paper trading
    live_url = "https://api.alpaca.markets/v2/positions"
    paper_url = "https://paper-api.alpaca.markets/v2/positions"
    
    headers = {
        'accept': 'application/json',
        'APCA-API-KEY-ID': account['api_public'],
        'APCA-API-SECRET-KEY': account['api_secret']
    }
    
    try:
        # Try the live trading API first
        response = requests.get(live_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        print("Successfully retrieved positions from live trading.")
    except requests.exceptions.RequestException as live_error:
        # If the live API fails, fall back to paper trading
        print(f"Live trading positions retrieval failed: {live_error}, trying paper trading...")
        try:
            response = requests.get(paper_url, headers=headers)
            response.raise_for_status()
            print("Successfully retrieved positions from paper trading.")
        except requests.exceptions.RequestException as paper_error:
            print(f"Paper trading positions retrieval also failed: {paper_error}")
            return None
    
    # If successful, check for open positions
    open_positions = response.json()
    for position in open_positions:
        if position['symbol'] in tickers:
            return position['symbol']  # Return the ticker that is open
    return None

# Get the account equity (for placing orders) TEST PASSED
def get_account_equity(account):
    # URLs for live and paper trading
    live_url = "https://api.alpaca.markets/v2/account"
    paper_url = "https://paper-api.alpaca.markets/v2/account"
    
    headers = {
        'accept': 'application/json',
        'APCA-API-KEY-ID': account['api_public'],
        'APCA-API-SECRET-KEY': account['api_secret']
    }

    try:
        # Try the live trading API first
        response = requests.get(live_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        print("Successfully retrieved account equity from live trading.")
    except requests.exceptions.RequestException as live_error:
        # If the live API fails, fall back to paper trading
        print(f"Live trading account equity retrieval failed: {live_error}, trying paper trading...")
        try:
            response = requests.get(paper_url, headers=headers)
            response.raise_for_status()
            print("Successfully retrieved account equity from paper trading.")
        except requests.exceptions.RequestException as paper_error:
            print(f"Paper trading account equity retrieval also failed: {paper_error}")
            return None
    
    # If successful, return the account equity
    return float(response.json().get('equity', 0))

# Place an order to buy the selected ticker TEST PASSED
def place_order(account, ticker, usdamount):
    # URLs for live and paper trading
    live_url = "https://api.alpaca.markets/v2/orders"
    paper_url = "https://paper-api.alpaca.markets/v2/orders"
    
    headers = {
        'accept': 'application/json',
        'APCA-API-KEY-ID': account['api_public'],
        'APCA-API-SECRET-KEY': account['api_secret']
    }
    
    order_data = {
        "symbol": ticker,
        "notional": usdamount,
        "side": "buy",
        "type": "market",
        "time_in_force": "day"
    }

    try:
        # Try to place the order on the live API first
        response = requests.post(live_url, json=order_data, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        print(f"Successfully placed order for {ticker} on live trading.")
    except requests.exceptions.RequestException as live_error:
        # If live API fails, fall back to paper trading
        print(f"Live trading order failed: {live_error}, trying paper trading...")
        try:
            response = requests.post(paper_url, json=order_data, headers=headers)
            response.raise_for_status()
            print(f"Successfully placed order for {ticker} on paper trading.")
        except requests.exceptions.RequestException as paper_error:
            print(f"Paper trading order also failed: {paper_error}")

# Liquidate any current position if it's not the target TEST PASSED
def liquidate_position(account, ticker):
    print(f"Liquidating {ticker} for account {account['email']}")
    
    # URLs for live and paper trading
    live_url = f"https://api.alpaca.markets/v2/positions/{ticker}"
    paper_url = f"https://paper-api.alpaca.markets/v2/positions/{ticker}"
    
    headers = {
        'accept': 'application/json',
        'APCA-API-KEY-ID': account['api_public'],
        'APCA-API-SECRET-KEY': account['api_secret']
    }

    try:
        # Try to liquidate the position on the live API first
        response = requests.delete(live_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        print(f"Successfully liquidated position in {ticker} on live trading.")
    except requests.exceptions.RequestException as live_error:
        # If live API fails, fall back to paper trading
        print(f"Live trading liquidation failed: {live_error}, trying paper trading...")
        try:
            response = requests.delete(paper_url, headers=headers)
            response.raise_for_status()
            print(f"Successfully liquidated position in {ticker} on paper trading.")
        except requests.exceptions.RequestException as paper_error:
            print(f"Paper trading liquidation also failed: {paper_error}")


def liquidate_all_positions(account):
    # URLs for live and paper trading
    live_url = "https://api.alpaca.markets/v2/positions?cancel_orders=true"
    paper_url = "https://paper-api.alpaca.markets/v2/positions?cancel_orders=true"
    
    headers = {
        'accept': 'application/json',
        'APCA-API-KEY-ID': account['api_public'],
        'APCA-API-SECRET-KEY': account['api_secret']
    }
    
    try:
        # Try to liquidate all positions on the live API first
        response = requests.delete(live_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        print(f"Successfully liquidated all positions for {account['email']} on live trading.")
        return True
    except requests.exceptions.RequestException as live_error:
        # If live API fails, fall back to paper trading
        print(f"Live trading liquidation failed: {live_error}, trying paper trading...")
        try:
            response = requests.delete(paper_url, headers=headers)
            response.raise_for_status()
            print(f"Successfully liquidated all positions for {account['email']} on paper trading.")
            return True
        except requests.exceptions.RequestException as paper_error:
            print(f"Paper trading liquidation also failed: {paper_error}")
            return False

### DATA FUNCTIONS ###
# Fetch latest Alpaca price TEST PASSED
def fetch_alpaca_latest_price(ticker):
    url = f"https://data.alpaca.markets/v2/stocks/quotes/latest?symbols={ticker}"
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": API_PUBLIC,
        "APCA-API-SECRET-KEY": API_SECRET
    }
    response = requests.get(url, headers=headers)
    # print(response.text)
    if response.status_code == 200:
        # Accessing the ask price ('ap') under the ticker symbol ('***')
        return response.json()['quotes'][ticker]['ap']  # Last ask price
    return None

### TIME AND CALENDAR FUNCTIONS ###
# Fetch Alpaca trading calendar TEST PASSED
def get_trading_calendar(start_date, end_date):
    url = f"https://paper-api.alpaca.markets/v2/calendar?start={start_date}&end={end_date}&date_type=TRADING"
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": API_PUBLIC,
        "APCA-API-SECRET-KEY": API_SECRET
    }
    response = requests.get(url, headers=headers)
    # print(response.text)
    return response.json()

# Check if today is the last trading day of the month (using Alpaca's calendar) TEST PASSED
def is_last_trading_day_of_month():
    now = datetime.now(pytz.timezone('America/New_York'))
    today = now.date()
    next_day = today + timedelta(days=1)
    calendar = get_trading_calendar(today, next_day)

    trading_dates = [pd.Timestamp(day['date']).date() for day in calendar]
    
    if next_day.month != today.month and today in trading_dates:
        print(f"[{now}] It's the last trading day of the month!")
    else:
        print(f"[{now}] It's NOT the last trading day of the month")
    
    return next_day.month != today.month and today in trading_dates

# Check if today the market is open TEST PASSED
def is_market_open():
    now = datetime.now(pytz.timezone('America/New_York'))
    today = now.date()
    next_day = today + timedelta(days=1)
    calendar = get_trading_calendar(today, next_day)

    trading_dates = [pd.Timestamp(day['date']).date() for day in calendar]

    if today in trading_dates:
        print(f"[{now}] market is OPEN today")
    else:
        print(f"[{now}] market is CLOSED today")
    
    return today in trading_dates