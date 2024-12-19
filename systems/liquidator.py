from postgresql.postgremanager import *
from alpaca_api.functions import liquidate_all_positions

def inactive_liquidator():
    """Process daily liquidation for inactive accounts marked to be stopped."""
    # Iterate through the inactive accounts
    for account in get_inactive_accounts():
        if account['to_be_stopped']:  # No need for `== True`, just check the truthy value
            success = liquidate_all_positions(account)  # Liquidate positions
            
            if success:
                update_liquidation_status(account)