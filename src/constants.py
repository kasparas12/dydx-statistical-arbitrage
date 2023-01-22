from dydx3.constants import API_HOST_GOERLI, API_HOST_MAINNET
from decouple import config

# !!!! SELECT MODE !!!!
MODE = "DEVELOPMENT"

# Close all open positions and orders
ABORT_ALL_POSITIONS = True

# Find Cointegrated Pairs
FIND_COINTEGRATED = True

# Manage Exits
MANAGE_EXITS = True

# Place Trades
PLACE_TRADES = True

# Resolution
RESOLUTION = "1HOUR"

# Stats Window
WINDOW = 21

# Thresholds - Opening
MAX_HALF_LIFE = 24
ZSCORE_THRESH = 1.5
USD_PER_TRADE = 100
USD_MIN_COLLATERAL = 1880

# Thresholds - Closing
CLOSE_AT_ZSCORE_CROSS = True

# Ethereum Address
ETHEREUM_ADDRESS=config('ETHEREUM_ADDRESS')
ETHEREUM_PRIVATE_KEY=config('ETHEREUM_PRIVATE_KEY')

# HOST - Export
HOST = API_HOST_MAINNET if MODE == "PRODUCTION" else API_HOST_GOERLI

# HTTP PROVIDER
HTTPS_PROVIDER_MAINNET = config('HTTPS_PROVIDER_MAINNET')
HTTPS_PROVIDER_TESTNET = config('HTTPS_PROVIDER_TESTNET')
HTTPS_PROVIDER = HTTPS_PROVIDER_MAINNET if MODE == "PRODUCTION" else HTTPS_PROVIDER_TESTNET