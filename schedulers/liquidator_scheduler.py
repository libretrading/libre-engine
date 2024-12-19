import pytz
import time
from datetime import datetime
from systems.liquidator import inactive_liquidator
from alpaca_api.functions import is_market_open

def scheduler():
    while True:
        now = datetime.now(pytz.timezone('America/New_York'))

        # 12:00 Inactive Accounts Liquidation
        if now.hour == 12 and now.minute == 00 and is_market_open():
            inactive_liquidator()

        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    scheduler()