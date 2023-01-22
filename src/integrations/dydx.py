from dydx3 import Client, DydxApiError
from web3 import Web3
from constants import (
  HOST,
  ETHEREUM_ADDRESS,
  ETHEREUM_PRIVATE_KEY,
  HTTPS_PROVIDER,
)

def connect_to_dydx() -> Client:
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

    first_api_key = get_api_keys_result.data['apiKeys'][0]
    
    account = client.private.get_account()
    account_id = account.data["account"]["id"]
    quote_balance = account.data["account"]["quoteBalance"]
    
    print("Connection Successful 1")
    print("Account ID: ", account_id)
    print("Quote Balance: ", quote_balance)
    
    return client