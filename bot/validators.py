def validate_input(symbol, side, order_type, quantity, price):
    if not symbol:

        raise ValueError("Symbol is required")
    
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")
    
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValueError("Order type must be MARKET or LIMIT")
    
    try:
        quantity = float(quantity)
        if quantity <= 0:
            raise ValueError
    except:
        raise ValueError("Quantity must be a positive number")
    
    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price required for LIMIT orders")
        try:
            float(price)
        except:
            raise ValueError("Price must be a number")