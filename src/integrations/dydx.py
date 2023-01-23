import time
from dydx3 import Client, DydxApiError
from web3 import Web3
from constants import (
  HOST,
  ETHEREUM_ADDRESS,
  ETHEREUM_PRIVATE_KEY,
  HTTPS_PROVIDER,
)
from datetime import datetime, timedelta

from utils import format_number

class DyDxClient():
    client: Client

    def connect_to_dydx(self) -> Client:
        
        print("Connecting to dydx...")
        
        client = Client(
            host=HOST,
            default_ethereum_address=ETHEREUM_ADDRESS,
            web3=Web3(Web3.HTTPProvider(HTTPS_PROVIDER)),
            eth_private_key=ETHEREUM_PRIVATE_KEY)
            
        # Set STARK key.
        stark_key_pair_with_y_coordinate = client.onboarding.derive_stark_key()
        client.stark_private_key = stark_key_pair_with_y_coordinate['private_key']
        (public_x, public_y) = (
            stark_key_pair_with_y_coordinate['public_key'],
            stark_key_pair_with_y_coordinate['public_key_y_coordinate'],
        )
        
        # Onboard the user.
        try:
            client.onboarding.create_user(
                ethereum_address=ETHEREUM_ADDRESS,
                stark_public_key=public_x,
                stark_public_key_y_coordinate=public_y,
            )

        # If the Ethereum address was already onboarded, ignore the error.
        except DydxApiError:
            pass
        
        get_api_keys_result = client.private.get_api_keys()
        
        if len(get_api_keys_result.data['apiKeys']) == 0:         
            # Register API key.
            client.eth_private.create_api_key()
            get_api_keys_result = client.private.get_api_keys()
        
        account = client.private.get_account()
        account_id = account.data["account"]["id"]
        quote_balance = account.data["account"]["quoteBalance"]
        
        print("Connection Successful")
        print("Account ID: ", account_id)
        print("Quote Balance: ", quote_balance)
        
        self.client = client
        return self.client
    
    def place_market_order(self, market:str, side: str, size: str, price: str, reduce_only: bool):
        
        # Get Position Id
        account_response = self.client.private.get_account()
        position_id = account_response.data["account"]["positionId"]
        
        # Get expiration time
        server_time = self.client.public.get_time()
        expiration = datetime.fromtimestamp(server_time.data["epoch"]) + timedelta(seconds=70)
        
        # Place an order
        placed_order = self.client.private.create_order(
            position_id=position_id, # required for creating the order signature
            market=market,
            side=side,
            order_type="MARKET",
            post_only=False,
            size=size,
            price=price,
            limit_fee='0.015',
            expiration_epoch_seconds=expiration.timestamp(),
            time_in_force="FOK", 
            reduce_only=reduce_only
        )
        
         # Return result
        return placed_order.data
    
    def abort_all_positions(self):
        
        # Cancel all orders
        self.client.private.cancel_all_orders()        
        
        # Protect API
        time.sleep(0.5)
        
        # Get markets for reference of tick size
        markets = self.client.public.get_markets().data
        
        # Protect API
        time.sleep(0.5)
        
        # Get all open positions
        positions = self.client.private.get_positions(status="OPEN")
        all_positions = positions.data["positions"]
        
        # Handle open positions
        close_orders = []
        if len(all_positions) > 0:
            # Loop through each position
            for position in all_positions:
                
                # Determine Market
                market = position["market"]
                # Determine Side
                side = "BUY"   
                       
                if position["side"] == "LONG":
                    side = "SELL"    
                    
                # Get Price
                price = float(position["entryPrice"])
                accept_price = price * 1.7 if side == "BUY" else price * 0.3
                tick_size = markets["markets"][market]["tickSize"]
                accept_price = format_number(accept_price, tick_size)
        
                # Place order to close
                order = self.place_market_order(
                    market,
                    side,
                    position["sumOpen"],
                    accept_price,
                    True
                )
        
                # Append the result
                close_orders.append(order)

                # Protect API
                time.sleep(0.2)
                
        # Return closed orders
        return close_orders