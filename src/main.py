from constants import ABORT_ALL_POSITIONS
from integrations.dydx import DyDxClient

if __name__ == "__main__":
    try:
        client = DyDxClient()
        client.connect_to_dydx()
    except Exception as e:
        print(f"Error while connecting to dydx: {e}")
        exit(1)
        
    # Abort all open positions
    if ABORT_ALL_POSITIONS:
        try:
            print("Closing all positions...")
            close_orders = client.abort_all_positions()
        except Exception as e:
            print("Error closing all positions: ", e)
            exit(1)