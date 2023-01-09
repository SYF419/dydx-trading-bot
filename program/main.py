from func_connections import connect_dydx
from constants import ABORT_ALL_POSITIONS
from constants import FIND_COINTEGRATED
from func_private import abort_all_positions
from func_public import construct_market_prices

if __name__ == "__main__":
    #Connect to client
    try:
        client = connect_dydx()
        print("Connecting to Client")
    except Exception as e:
        print(e)
        print("Error Connecting to Client: ", e)
        exit(1)
        
    #Abort all positions
    if ABORT_ALL_POSITIONS:
        try:
            print("Closing all positions")
            close_orders = abort_all_positions(client)
        except Exception as e:
            print("Error aborting orders")
        exit(1)
    #FIND COINTEGRATED PAIRS
    if FIND_COINTEGRATED:
        try:
            print("Fetching market prices, please allow 3 minutes")
            df_market_prices = construct_market_prices(client)
        except Exception as e:
            print("Error finding coint: ", e)
            exit(1)