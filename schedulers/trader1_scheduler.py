import time
import pytz
from datetime import datetime
from alpaca_api.functions import is_market_open
from systems.trader1 import daily_1030_check_and_execute, weekly_execute

def scheduler():
    while True:
        now = datetime.now(pytz.timezone('America/New_York'))

        # 10:30 AM Execute Accounts with no positions (new subs)
        if now.hour == 10 and now.minute == 30 and is_market_open():
            daily_1030_check_and_execute()

        # 3:00 PM Last Trading Day Check (actual strategy)
        if now.hour == 15 and now.minute == 0 and is_market_open() and now.weekday() == 4:
            weekly_execute()

        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    scheduler()
    
