import sys
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException  # <--- FIXED IMPORT

# --- CONFIGURATION ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_activity.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class BasicBot:
    """
    A simplified trading bot for Binance Futures Testnet.
    """
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret, testnet=testnet)
        logger.info("Bot initialized and connected to Binance Testnet.")

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        try:
            params = {
                'symbol': symbol.upper(),
                'side': side.upper(),
                'type': order_type.upper(),
                'quantity': quantity,
            }

            # Add specific parameters based on order type
            if order_type.upper() == 'LIMIT':
                if not price:
                    raise ValueError("Price is required for LIMIT orders.")
                params['price'] = price
                params['timeInForce'] = 'GTC'
            
            elif order_type.upper() == 'STOP': 
                 if not price or not stop_price:
                    raise ValueError("Price and Stop Price are required for STOP-LIMIT orders.")
                 params['type'] = 'STOP'
                 params['price'] = price
                 params['stopPrice'] = stop_price
                 params['timeInForce'] = 'GTC'

            logger.info(f"Sending order: {params}")
            
            # Execute the order using the Binance Client
            response = self.client.futures_create_order(**params)
            
            logger.info(f"Order Success! ID: {response.get('orderId')} | Status: {response.get('status')}")
            print(f"\n[SUCCESS] Order placed successfully!")
            print(f"Order ID: {response.get('orderId')}")
            print(f"Status: {response.get('status')}")
            return response

        except BinanceAPIException as e:  # <--- FIXED EXCEPTION
            logger.error(f"Binance API Error: {e.message} | Code: {e.code}")
            print(f"\n[ERROR] Binance API failed: {e.message}")
        except ValueError as e:
            logger.error(f"Validation Error: {str(e)}")
            print(f"\n[ERROR] Input invalid: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected Error: {str(e)}")
            print(f"\n[ERROR] An unexpected error occurred: {str(e)}")

# --- CLI INTERFACE ---

def get_user_input():
    print("\n--- BINANCE TESTNET TRADING BOT ---")
    print("1. Place Market Order")
    print("2. Place Limit Order")
    print("3. Place Stop-Limit Order")
    print("4. Exit")
    
    choice = input("Select an option (1-4): ").strip()
    return choice

def main():
    print("Please enter your Binance Testnet Credentials:")
    api_key = input("API Key: ").strip()
    api_secret = input("Secret Key: ").strip()

    if not api_key or not api_secret:
        print("Error: Credentials cannot be empty.")
        return

    bot = BasicBot(api_key, api_secret)

    while True:
        choice = get_user_input()

        if choice == '4':
            print("Exiting bot. Goodbye!")
            break

        if choice not in ['1', '2', '3']:
            print("Invalid selection. Please try again.")
            continue

        symbol = input("Enter Symbol (e.g., BTCUSDT): ").strip().upper()
        side = input("Enter Side (BUY/SELL): ").strip().upper()
        
        try:
            quantity = float(input("Enter Quantity: ").strip())
        except ValueError:
            print("Invalid quantity. Must be a number.")
            continue

        if choice == '1': # Market
            bot.place_order(symbol, side, 'MARKET', quantity)

        elif choice == '2': # Limit
            try:
                price = float(input("Enter Limit Price: ").strip())
                bot.place_order(symbol, side, 'LIMIT', quantity, price=price)
            except ValueError:
                print("Invalid price. Must be a number.")

        elif choice == '3': # Stop-Limit
            try:
                price = float(input("Enter Limit Price: ").strip())
                stop_price = float(input("Enter Stop Price: ").strip())
                bot.place_order(symbol, side, 'STOP', quantity, price=price, stop_price=stop_price)
            except ValueError:
                print("Invalid price inputs.")

if __name__ == "__main__":
    main()