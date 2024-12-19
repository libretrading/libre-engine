import time
import pytz
from datetime import datetime
from alpaca_api.functions import is_market_open
from systems.trader2 import daily_1500_check_and_execute

def scheduler():
    while True:
        now = datetime.now(pytz.timezone('America/New_York'))

        # 15:00 execute voo mean rev system
        if now.hour == 15 and now.minute == 00 and is_market_open():
            daily_1500_check_and_execute()

        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    scheduler()