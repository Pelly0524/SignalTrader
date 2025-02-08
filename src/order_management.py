from decimal import Decimal, ROUND_DOWN
from binance_service import get_balance, get_current_price


# Dynamically calculate the order quantity based on the available USDT balance and the current price
def calculate_order_quantity(symbol, percentage):
    # Retrieve the available USDT balance and convert it to Decimal to avoid precision issues
    usdt_balance = Decimal(get_balance("USDT"))

    # Retrieve the current price of the trading pair and convert it to Decimal
    current_price = Decimal(get_current_price(symbol))

    # Calculate the raw order quantity
    raw_quantity = (usdt_balance * Decimal(percentage)) / current_price

    # Set the stepSize from the filter (using LOT_SIZE filter as an example)
    # The original stepSize is '0.00001000'. After normalization, it becomes 1E-5 (which is 0.00001)
    step_size = Decimal("0.00001000").normalize()

    # Use floor division to ensure the raw_quantity is an integer multiple of step_size
    # For example: Decimal('0.01444339') // Decimal('0.00001') yields 1444,
    # and 1444 * Decimal('0.00001') results in Decimal('0.01444')
    order_quantity = (raw_quantity // step_size) * step_size

    order_quantity = order_quantity.quantize(step_size, rounding=ROUND_DOWN)

    return order_quantity
