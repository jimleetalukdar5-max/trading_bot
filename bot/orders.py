from bot.client import send_order
import logging

def place_order(symbol, side, order_type, quantity, price=None):
   
    # Here we place a MARKET or LIMIT order on Binance Testnet.#

    params = {               # params is parameters for the API request #
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity
    }

    if order_type == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"  

    logging.info(f"Placing order: {params}")
    order_response = send_order(params)
    logging.info(f"Order response: {order_response}")
    return order_response