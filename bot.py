import websocket, json, pprint, numpy
import config
from binance.client import Client
from binance.enums import *
from scipy import stats
import threading

SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
UPPER_THRESHOLD = 1.5
LOWER_THRESHOLD = -1.5
PERIOD = 3
closesBtc = []
closesEth = []

client = Client(config.API_KEY, config.API_SECRET, tld='us')

def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    global closesBtc,closesEth, in_position
    
    #print('received message')
    json_message = json.loads(message)
    #pprint.pprint(json_message)

    candle = json_message['k']
    symbol = candle['s']
    is_candle_closed = candle['x']
    close = candle['c']
    print(close)
    if is_candle_closed:
        print("candle closed at {}".format(close))
        if(symbol=='BTCUSDT'):
            closesBtc.append(float(close))
            print("closes BTC")
            print(closesBtc)
        if(symbol=='ETHUSDT'):
            closesEth.append(float(close))
            print("closes ETH")
            print(closesEth)
        if len(closesBtc)>=PERIOD:
            np_closesBTC = numpy.array(closesBtc[-PERIOD:])
            np_closesETC = numpy.array(closesEth[-PERIOD:])

            rtio = numpy.divide(np_closesBTC,np_closesETC)
            zscore = stats.zscore(rtio)
            print("zscore")
            print(zscore)
            if(zscore[-1:]>UPPER_THRESHOLD):
                print("Buy! ........")
            if(zscore[-1:]<LOWER_THRESHOLD):
                print("SELL! .........")

def runWebSocketThread(socket):
    ws = websocket.WebSocketApp(socket, on_message=on_message, on_close=on_close)
    wst = threading.Thread(target=ws.run_forever)
    wst.start()

socket_btc = f'wss://stream.binance.com:9443/ws/btcusdt@kline_1m'
socket_eth = f'wss://stream.binance.com:9443/ws/ethusdt@kline_1m'
runWebSocketThread(socket_btc)
runWebSocketThread(socket_eth)
#ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
#ws.run_forever()
