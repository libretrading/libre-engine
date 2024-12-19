import pytz
import time
from datetime import datetime
from historical_data.datamanager import update_database


def scheduler():
    while True:
        now = datetime.now(pytz.timezone('America/New_York'))

        # 2 AM Database Maintenance
        if now.hour == 2 and now.minute == 0:
            update_database()

        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    scheduler()