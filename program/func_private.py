import datetime
import time
from pprint import pprint
from func_connections import connect_dydx
from func_utils import format_number


#Place Market Order
def place_market_order(client, market, side, size, price, reduce_only):
    #get position ID
    account_response = client.private.get_account()
    position_id = account_response.data["account"]["positionId"]
    #Get Expiration Time
    server_time = client.public.get_time()
    # expiration = datetime.fromisoformat(server_time.data["iso"].replace["Z",""]) + timedelta(seconds=70)
    #Place Order
    placed_order = client.private.create_order(
        position_id=position_id,
        market=market,
        side=side,
        order_type="MARKET",
        post_only=False,
        size=size,
        price=price,
        limit_fee='0.015',
        expiration_epoch_seconds=time.time() + 70,
        time_in_force="FOK",
        reduce_only=reduce_only
    )
    #Return Result
    return placed_order.data 


def abort_all_positions(client):
    #cancel all orders
    # print("TEST")
    client.private.cancel_all_orders()
    # print("orders_canceled")
    #protect API
    time.sleep(0.5)
    #get markets for reference of tick size
    markets = client.public.get_markets().data
    # pprint(markets)
    #Protect API
    time.sleep(0.5)
    #Get all open positions
    positions = client.private.get_positions(status="OPEN")
    # print(positions)
    all_positions = positions.data["positions"]
    # print(all_positions)
    #Handle open positions
    close_orders = []
    if len(all_positions) > 0:
        for position in all_positions:
            market = position["market"]
            #determine side
            side = "Buy"
            if position["side"] == "LONG":
                side = "SELL"
            price = float(position["entryPrice"])
            accept_price = price * 1.7 if side == "BUY" else price * 0.3
            tick_size = markets["markets"][market]["tickSize"]
            accept_price = format_number(accept_price, tick_size)
            print(market, price, accept_price, position["sumOpen"])
            order = place_market_order(
                client,
                market,
                side,
                position["sumOpen"],
                accept_price,
                True
            )
            #Append Result
            close_orders.append(order)
            #protect API
            time.sleep(0.2)
        #Return Closed Orders
        return close_orders