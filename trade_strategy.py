import numpy
import parameters
from scipy import stats
import time

def fitnessHelp(btc_arr, eth_arr, prams):
    parameters.STOP_LOSS = prams[0]
    parameters.TAKE_PROFIT = prams[1]
    parameters.TIME_OUT = prams[2]
    parameters.UPPER_THRESHOLD = prams[3]
    parameters.LOWER_THRESHOLD = prams[4]
    #print(type(btc_arr[0]))
    for i in range (len(btc_arr)):
        bot_trade(btc_arr[i:i+parameters.PERIOD],eth_arr[i:i+parameters.PERIOD])
    profit = parameters.BTC_AMOUNT*btc_arr[i] + parameters.ETH_AMOUNT*eth_arr[i] - parameters.USDT_START
    parameters.USDT_START = parameters.BTC_AMOUNT*btc_arr[i] + parameters.ETH_AMOUNT*eth_arr[i]
    return profit

def bot_trade(btc_closes,eth_closes):
    #print('bot trade is runing')
    #print(btc_closes)
    my_zscore = calculateZscore(btc_closes,eth_closes)
    trigger = getTrigger(my_zscore, btc_closes[-1:][0], eth_closes[-1:][0])

    if(trigger == 'Buy BTC and sell ETH'):
        create_order(btc_closes[-1:][0], eth_closes[-1:][0], 'Buy BTC and sell ETH')
    elif(trigger == 'Sell BTC and buy ETH'):
        create_order(btc_closes[-1:][0],eth_closes[-1:][0], 'Sell BTC and buy ETH')
    #else:
        #print('do nothing')
    #print("***********************************")

def create_order(btc_price,eth_price,order):
    #print("createing order: {}".format(order))
    parameters.LAST_ORDER['order'] = order
    parameters.BTC_AMOUNT_BEFOR_ORDER = parameters.BTC_AMOUNT
    parameters.ETH_AMOUNT_BEFOR_ORDER = parameters.ETH_AMOUNT
    parameters.LAST_ORDER['time'] = time.time()
    if(order == 'Buy BTC and sell ETH'):
        parameters.ETH_AMOUNT -= parameters.OREDR_AMOUNT/eth_price
        parameters.BTC_AMOUNT += parameters.OREDR_AMOUNT/btc_price
    elif(order == 'Sell BTC and buy ETH'):
        parameters.BTC_AMOUNT -= parameters.OREDR_AMOUNT/btc_price
        parameters.ETH_AMOUNT += parameters.OREDR_AMOUNT/eth_price
    #print('My current BTC is: {}'.format(parameters.BTC_AMOUNT))
    #print('My current ETH is: {}'.format(parameters.ETH_AMOUNT))
    parameters.PORTFOLIO_AFER_ORDER = parameters.BTC_AMOUNT*btc_price + parameters.ETH_AMOUNT*eth_price

def calculateZscore(btc_closes,eth_closes):
    np_closesBTC = numpy.array(btc_closes[-parameters.PERIOD:])
    np_closesETC = numpy.array(eth_closes[-parameters.PERIOD:])
    rtio = numpy.divide(np_closesBTC,np_closesETC)
    zscore = stats.zscore(rtio)
    #print("zscore {}".format(zscore[-1:]))
    return zscore[-1:]


def getTrigger(my_zscore, btc_price, eth_price):
    #print(parameters.LAST_ORDER['order'])
    if(parameters.LAST_ORDER['order'] == None):
        # open position
        parameters.LAST_ORDER['is_opened_position'] = True
        if(my_zscore>parameters.UPPER_THRESHOLD):
            parameters.LAST_ORDER['order'] = 'Buy BTC and sell ETH'
            return 'Buy BTC and sell ETH'
        elif(my_zscore<parameters.LOWER_THRESHOLD):            
            parameters.LAST_ORDER['order'] = 'Sell BTC and buy ETH'
            return 'Sell BTC and buy ETH'
        else:
            return 'do nothing'
    else:
        # open position
        if(parameters.LAST_ORDER['is_opened_position'] == False):
            if(my_zscore>parameters.UPPER_THRESHOLD and parameters.LAST_ORDER['order'] == 'Sell BTC and buy ETH'):
                parameters.LAST_ORDER['is_opened_position'] = True
                parameters.LAST_ORDER['order'] = 'Buy BTC and sell ETH'
                return 'Buy BTC and sell ETH'
            elif(my_zscore<parameters.LOWER_THRESHOLD and parameters.LAST_ORDER['order'] == 'Buy BTC and sell ETH'):  
                parameters.LAST_ORDER['is_opened_position'] = True
                parameters.LAST_ORDER['order'] = 'Sell BTC and buy ETH'
                return 'Sell BTC and buy ETH'
            else: 
                return 'do nothing'
        # close position
        elif(parameters.LAST_ORDER['is_opened_position'] == True):
            #print("Cheaking close position")
            profit = getProfit(btc_price, eth_price)
            passedTime = time.time() - parameters.LAST_ORDER['time']
            #print('passed time {}'.format(passedTime))
            if(profit < parameters.STOP_LOSS or profit > parameters.TAKE_PROFIT or passedTime > parameters.TIME_OUT):
                parameters.LAST_ORDER['is_opened_position'] = False
                if(parameters.LAST_ORDER['order'] == 'Buy BTC and sell ETH'):
                    return 'Sell BTC and buy ETH'
                else:
                    return 'Buy BTC and sell ETH'
            else:
                return 'do nothing'


def getProfit(btc_price,eth_price):
    profit_if_order = parameters.BTC_AMOUNT*btc_price + parameters.ETH_AMOUNT*eth_price
    #print('profit_if_order {}'.format(profit_if_order))
    profit_if_not_order = parameters.BTC_AMOUNT_BEFOR_ORDER*btc_price + parameters.ETH_AMOUNT_BEFOR_ORDER*eth_price
    #print('profit_if_not_order {}'.format(profit_if_not_order))
    profit = profit_if_order - profit_if_not_order
    usdt = parameters.BTC_AMOUNT*btc_price + parameters.ETH_AMOUNT*eth_price
    #print('profit is {}'.format(profit))
    #print('usdt is {}'.format(usdt))
    return profit