import requests
import time
import hmac
import hashlib
import logging

BASE_URL = "https://testnet.binancefuture.com"
API_KEY = "YOUR_API_KEY"     # place your api_key here #
API_SECRET = "YOUR_SECRET_KEY"  # place your api_secret_key here #

def sign_params(params):
    # Sign the request parameters for Binance. #
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    return signature

def get_price(symbol="BTCUSDT"):
    # To get the current market price for a symbol. #
    response = requests.get(BASE_URL + "/fapi/v1/ticker/price", params={"symbol": symbol.upper()})
    data = response.json()
    if "price" in data:
        return float(data["price"])
    else:
        logging.error(f"Invalid symbol '{symbol}' | Response: {data}")
        raise ValueError(f"Invalid symbol '{symbol}'")

def send_order(params):
    # It sends order to Binance Futures Testnet. #
    params["timestamp"] = int(time.time() * 1000)
    params["signature"] = sign_params(params)
    headers = {"X-MBX-APIKEY": API_KEY}
    response = requests.post(BASE_URL + "/fapi/v1/order", headers=headers, params=params)
    logging.info(f"Request → {params}")
    logging.info(f"Response ← {response.text}")
    return response.json()

def min_quantity(symbol="BTCUSDT"):
    # For Calculating the minimum quantity to meet 100 USDT notional requirement.#
    price = get_price(symbol)
    qty = 100 / price
    return round(qty, 6)