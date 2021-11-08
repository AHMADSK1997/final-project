import websocket, json
import threading

def on_message(ws, message):
    json_message = json.loads(message)
    symbol = json_message['s']
    close = json_message['p']
    print(symbol,":",close)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def runWebSocketThread(socket):
    ws = websocket.WebSocketApp(socket, on_message=on_message, on_close=on_close)
    wst = threading.Thread(target=ws.run_forever)
    wst.start()

socket_btc = f'wss://stream.binance.com:9443/ws/btcusdt@aggTrade'
socket_eth = f'wss://stream.binance.com:9443/ws/ethusdt@aggTrade'
runWebSocketThread(socket_btc)
runWebSocketThread(socket_eth)