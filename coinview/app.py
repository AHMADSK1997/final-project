from flask import Flask, render_template
from genetictest import runGa
app = Flask(__name__)

@app.route('/')
def hello_world():
    title = 'CoinView'
    return render_template('index.html', title=title)

@app.route('/my-link/')
def my_link():
  array = runGa()
  return array

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)