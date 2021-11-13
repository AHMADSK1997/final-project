import websocket, json, pprint, numpy
import config
from binance.client import Client
from scipy import stats
import threading
import time

SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
UPPER_THRESHOLD = 0.5
LOWER_THRESHOLD = -0.5
PERIOD = 3
STOP_LOSS = -5
TAKE_PROFIT = 10
TIME_OUT = 60
BTC = 10
ETH = 50
oldtime = time.time()
profit = 0
position_BTC_ETH = False
in_position = False
closesBtc = []
closesEth = []

client = Client(config.API_KEY, config.API_SECRET, tld='us')

def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    global closesBtc,closesEth, in_position, position_BTC_ETH, oldtime, profit
    json_message = json.loads(message)
    #pprint.pprint(json_message)
    data = json_message['data']
    candle = data['k']
    symbol = candle['s']
    is_candle_closed = candle['x']
    close = candle['c']
    #print(close)
    if is_candle_closed:
        print("candle closed at {}".format(close))
        if(symbol=='BTCUSDT'):
            closesBtc.append(float(close))
        elif(symbol=='ETHUSDT'):
            closesEth.append(float(close))
        
        # need Barrier
        if len(closesBtc)>=PERIOD:
            
            # open position
            if(in_position == False):
                print("Cheaking open position")
                np_closesBTC = numpy.array(closesBtc[-PERIOD:])
                np_closesETC = numpy.array(closesEth[-PERIOD:])
                rtio = numpy.divide(np_closesBTC,np_closesETC)
                zscore = stats.zscore(rtio)
                print("zscore {}".format(zscore[-1:]))
                if(zscore[-1:]>UPPER_THRESHOLD):
                    print("Buy BTC and sell ETH")
                    profit = 0 
                    oldtime = time.time()
                    position_BTC_ETH = True
                    in_position = True
                elif(zscore[-1:]<LOWER_THRESHOLD):
                    print("Sell BTC and buy ETH")
                    oldtime = time.time()
                    profit = 0
                    position_BTC_ETH = False
                    in_position = True
            # close position
            elif(in_position == True):
                print("Cheaking close position")
                passedTime = time.time() - oldtime
                if(profit < STOP_LOSS  or profit > TAKE_PROFIT or passedTime > TIME_OUT):
                    in_position = False
                    if(position_BTC_ETH == True):
                        print("Sell BTC and buy ETH")
                    else:
                        print("Buy BTC and sell ETH")

def runWebSocketThread(socket):
    ws = websocket.WebSocketApp(socket, on_message=on_message, on_close=on_close)
    ws.run_forever()
    #wst = threading.Thread(target=ws.run_forever)
    #wst.start()

socket = f'wss://stream.binance.com:9443/stream?streams=ethusdt@kline_1m/btcusdt@kline_1m'
#socket_eth = f'wss://stream.binance.com:9443/ws/ethusdt@kline_1m'
runWebSocketThread(socket)
