from flask import Flask, render_template,request
from threading import Lock
from flask_socketio import SocketIO, emit
import sys

sys.path.insert(0, '../final project/genetic_algorithm')
from genetictest import runGa
sys.path.insert(1, '../final project/strategy')
from ws import runWS
from initialize import initialize
import parameters

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        print(parameters.BTC_AMOUNT)
        socketio.sleep(30)
        count += 1
        socketio.emit('my_response',
                      {'data': parameters.BTC_AMOUNT, 'count': count})

@app.route('/')
def hello_world():
    print(parameters.BTC_AMOUNT)
    return render_template('index.html',Stoploss=parameters.STOP_LOSS,
                                        Takeprofit=parameters.TAKE_PROFIT,
                                        Timeout=parameters.TIME_OUT,
                                        Upper=parameters.UPPER_THRESHOLD,
                                        Lower=parameters.LOWER_THRESHOLD)

@app.route("/forward/", methods=['POST'])
def my_link():
    params = runGa()
    print(parameters.BTC_AMOUNT)
    return render_template('index.html', Stoploss=params[0],
                                        Takeprofit=params[1],
                                        Timeout=params[2],
                                        Upper=params[3],
                                        Lower=params[4])
@app.route("/start/", methods=['POST'])
def start():
    initialize()
    runWS()
    return render_template('index.html',Stoploss=parameters.STOP_LOSS,
                                        Takeprofit=parameters.TAKE_PROFIT,
                                        Timeout=parameters.TIME_OUT,
                                        Upper=parameters.UPPER_THRESHOLD,
                                        Lower=parameters.LOWER_THRESHOLD)

@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})

if __name__ == "__main__":
    print(parameters.BTC_AMOUNT)
    socketio.run(app)