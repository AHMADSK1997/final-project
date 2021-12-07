from flask import Flask, render_template

import sys
sys.path.insert(0, '../final project/genetic_algorithm')
from genetictest import runGa

app = Flask(__name__)

@app.route('/')
def hello_world():
    title = 'CoinView'
    return render_template('index.html', title=title)

@app.route("/forward/", methods=['POST'])
def my_link():
    params = runGa()
    return render_template('index.html', Stoploss=params[0],Takeprofit=params[1],Timeout=params[2],Upper=params[3],Lower=params[4])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)