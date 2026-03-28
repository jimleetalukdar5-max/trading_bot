#trading bot
## Project structure

trading_bot/
│
├─ bot/
│   ├─ __init__.py
│   ├─ client.py          # API interaction & order sending
│   ├─ orders.py          # Build and send orders
│   ├─ validators.py      # Input validation
│   └─ logging_config.py  # Logger setup
│
├─ cli.py                 # Command-line interface
├─ requirements.txt       # Required Python packages
├─ README.md              # Instructions & examples            
└─ sample_logs/
    ├─ market_order.log   # Example MARKET order
    └─ limit_order.log    # Example LIMIT order


## Setup Steps 

1.** Install Python** 
2.** Install dependencies from requirements.txt: 
     " pip install -r requirements.txt "
3.Configure API keys
  (i) Create your Binance Future Testnet accound.
  (ii) Set your API key and secret in the environment variables.
     " set BINANCE_API_KEY=<your_testnet_api_key>
       set BINANCE_API_SECRET=<your_testnet_api_secret>"

## How to run 
1. Run the CLI bot:
   "python cli.py"

## Assumptions 

1. All trading is done on ( Binance Futures Testnet ), so no real funds are used.
2. The minimum order notional is 100 USDT, meaning any order must be worth at least 100 USDT.
3. Quantity and price rounding rules are based on Binance specifications:

   * BTCUSDT quantity:rounded to 3 decimals
   * Other symbols quantity:rounded to 6 decimals
   * Price:rounded to 2 decimals
4. MARKET orders execute immediately at the best available price; LIMIT orders execute at the specified price or better.
5. Users must provide ( valid symbols ), sides (`BUY`/`SELL`), and order types (`MARKET`/`LIMIT`).
6. API keys are not included as users must set their own Testnet API key and secret.
7. The bot automatically calculates minimum order quantity based on the current price to ensure compliance with Binance rules.
8. Logs (`tradings.log`) record all order activity for review.


