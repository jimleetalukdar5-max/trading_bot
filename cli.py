# cli.py
from bot.orders import place_order
from bot.validators import validate_input
from bot.client import get_price, min_quantity
from bot.logging_config import setup_logger
import logging

# To call log #
setup_logger()


# Rounding functions for quantity and price # 
def round_quantity(symbol, qty):
    
    #Round quantity based on Binance rules , for  BTCUSDT: 3 decimals and others: 6 decimal #
    if symbol.upper() == "BTCUSDT":
        return round(qty, 3)
    return round(qty, 6)

def round_price(symbol, price):
    
    #Round price based on Binance rules , for BTCUSDT: 2 decimals and others: 2 decimals #
    
    return round(price, 2)


# Here is the CLI Loop #
print("  Binance Futures Testnet Bot\n")

while True:
    try:
        # GTo get the user inputs #
        symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
        side = input("Enter side (BUY/SELL): ").upper()
        order_type = input("Enter order type (MARKET/LIMIT): ").upper()

        # CTo check symbol validity #
        try:
            current_price = get_price(symbol)
        except Exception as e:
            print(f" Invalid symbol '{symbol}'. Please try again.")
            logging.error(f"Invalid symbol input: {symbol} | {e}")
            continue

        # To show minimum quantity (for MARKET orders) #
        min_qty = min_quantity(symbol)
        print(f" Minimum order quantity for {symbol} is {min_qty}")

        # To get quantity input#
        quantity = float(input(f"Enter quantity (≥ {min_qty}): "))
        if quantity < min_qty:
            print(f" Quantity too small. Setting to minimum: {min_qty}")
            quantity = min_qty
        quantity = round_quantity(symbol, quantity)

        # Here handles LIMIT orders #
        price = None
        if order_type.upper() == "LIMIT":
            price = float(input("Enter price: "))
            price = round_price(symbol, price)

            # To calculate minimum quantity for the entered price #
            min_qty_at_price = 100 / price  # 100 USDT min notional #
            quantity = max(quantity, min_qty_at_price)
            quantity = round_quantity(symbol, quantity)  # For correct rounding #

            print(f" Minimum order quantity for {symbol} at {price} USDT is {quantity}")

        # MARKET orders here shows current price #
        elif order_type.upper() == "MARKET":
            print(f" Current {symbol} price: {current_price}")

        # To validate all inputs #
        validate_input(symbol, side, order_type, quantity, price)

        # To place the order #
        print("\n Placing order...")
        logging.info(f"User placing order: {symbol}, {side}, {order_type}, {quantity}, {price}")
        order = place_order(symbol, side, order_type, quantity, price)

        # To show order response #
        print("\n Order Response:")
        print(f"Order ID: {order.get('orderId')}")
        print(f"Status: {order.get('status')}")
        print(f"Executed Qty: {order.get('executedQty')}")
        print(f"Avg Price: {order.get('avgFillPrice', 'N/A')}")
        if "code" in order and "msg" in order:
            print(f"Error Code: {order['code']}, Message: {order['msg']}")
            logging.error(f"Order Error: {order}")

    except Exception as e:
        print(f"\n Error: {e}")
        logging.error(f"CLI Error: {e}")

    # We ask user if they want to place another order #
    again = input("\nDo you want to place another order? (y/n): ").lower()
    if again != "y":
        print(" Exiting bot. Happy trading!")
        break