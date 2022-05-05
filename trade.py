from alice_blue import *
import datetime
import statistics
from time import sleep

with open('access_token', 'r') as file:
    access_token = file.read().rstrip("\n")

alice = AliceBlue(username='', password='', access_token=access_token, master_contracts_to_download=['NSE', 'NFO'])
scrip = alice.get_instrument_for_fno(symbol = 'NIFTY', expiry_date=datetime.date(2022, 5, 26), is_fut=True, strike=None, is_CE = False)

socket_opened = False

def event_handler_quote_update(message):
    global cmp
    cmp = message['ltp']

def open_callback():
    global socket_opened
    socket_opened = True

alice.start_websocket(subscribe_callback=event_handler_quote_update, socket_open_callback=open_callback, run_in_background=True)

while(socket_opened==False):
    pass

alice.subscribe(scrip, LiveFeedType.MARKET_DATA)

def buy_signal(in_scrip):
    alice.place_order(transaction_type = TransactionType.Buy, instrument = in_scrip, quantity = 1, order_type = OrderType.Market, product_type = ProductType.Delivery, price = 0.0, trigger_price = None, stop_loss = None, square_off = None, trailing_sl = None, is_amo = False)

def sell_signal(in_scrip):
    alice.place_order(transaction_type = TransactionType.Sell, instrument = in_scrip, quantity = 1, order_type = OrderType.Market, product_type = ProductType.Delivery, price = 0.0, trigger_price = None, stop_loss = None, square_off = None, trailing_sl = None, is_amo = False)

minute_close = []
current_signal = ''

while True:
    if(datetime.datetime.now().second == 0):
        minute_close.append(cmp)
        if(len(minute_close) > 20):
            sma_5 = statistics.mean(minute_close[-5:])
            sma_20 = statistics.mean(minute_close[-20:])
            print(f"sma_5: {sma_5}, sma_20: {sma_20}, Diff: {sma_5 - sma_20}")
            if(current_signal != 'buy'):
                if(sma_5 > sma_20):
                    #buy_signal(scrip)
                    current_signal = 'buy'
                    print(f"{current_signal} at {datetime.datetime.now()}")
            if(current_signal != 'sell'):
                if(sma_5 < sma_20):
                    #sell_signal(scrip)
                    current_signal = 'sell'
                    print(f"{current_signal} at {datetime.datetime.now()}")
        sleep(1)
    sleep(0.2)

