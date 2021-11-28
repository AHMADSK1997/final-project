import websocket, json, pprint, numpy
from trade_strategy import bot_trade  
from binance.client import Client
import config

btc_price = None
etc_price = None
closesBtc = []
closesEth = []

client = Client(config.API_KEY, config.API_SECRET, tld='us')

def historical_last_in_minutes(stock,time,arayyToSave):
    klines = client.get_historical_klines(stock, Client.KLINE_INTERVAL_1MINUTE, time+" minute ago UTC")
    for i in range(len(klines)):
        arayyToSave.append(float(klines[i][4]))
    
def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    global btc_price,etc_price, closesBtc, closesEth
    json_message = json.loads(message)
    data = json_message['data']
    candle = data['k']
    symbol = candle['s']
    is_candle_closed = candle['x']
    close = candle['c']
    if is_candle_closed:
        print("candle closed at {}".format(close))
        if(symbol=='BTCUSDT'):
            btc_price = float(close)
            closesBtc.append(btc_price)
        elif(symbol=='ETHUSDT'):
            etc_price = float(close)
            closesEth.append(etc_price)
        if(btc_price != None and etc_price != None):
            print("***********************************")
            print("call to the trade strategy") # create the trade strategy
            bot_trade(closesBtc,closesEth)
            btc_price = None
            etc_price = None

def runWS():
    historical_last_in_minutes("BTCUSDT","10",closesBtc)
    historical_last_in_minutes("ETHUSDT","10",closesEth)
    socket = f'wss://stream.binance.com:9443/stream?streams=ethusdt@kline_1m/btcusdt@kline_1m'
    ws = websocket.WebSocketApp(socket, on_open=on_open ,on_message=on_message, on_close=on_close)
    ws.run_forever()

