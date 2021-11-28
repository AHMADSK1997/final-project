import parameters
import config
from binance.client import Client
from ws import runWS

client = Client(config.API_KEY, config.API_SECRET, tld='us')



def initialize():
    btc_klines = client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_1MINUTE, "1 minute ago UTC")
    eth_klines = client.get_historical_klines('ETHUSDT', Client.KLINE_INTERVAL_1MINUTE, "1 minute ago UTC")
    parameters.BTC_AMOUNT = (parameters.USDT_START/2)/float(btc_klines[0][4])
    parameters.ETH_AMOUNT = (parameters.USDT_START/2)/float(eth_klines[0][4])
    parameters.BTC_AMOUNT_BEFOR_ORDER = parameters.BTC_AMOUNT
    parameters.ETH_AMOUNT_BEFOR_ORDER = parameters.ETH_AMOUNT

def main():
    initialize()
    runWS()


if __name__ == "__main__":
    main()