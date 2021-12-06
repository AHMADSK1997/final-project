import numpy as np
from geneticalgorithm import geneticalgorithm as ga
from trade_strategy import fitnessHelp
import pandas as pd

i=0
btc_arr = None
eth_arr = None
def f(X):
    global btc_arr,eth_arr,i
    if(i == 0):
        btc_arr = getDatafromExel(100 ,'BTC-1-minute.csv', 0)
        eth_arr = getDatafromExel(100 ,'ETH-1-minute.csv', 0)
        profit = fitnessHelp(btc_arr, eth_arr, X)
        i+=100
    else:
        btc_row = getDatafromExel(1, 'BTC-1-minute.csv', i)
        eth_row = getDatafromExel(1, 'ETH-1-minute.csv', i)
        btc_arr = np.delete(btc_arr,0)
        btc_arr = np.append(btc_arr,btc_row)
        eth_arr = np.delete(eth_arr,0)
        eth_arr = np.append(eth_arr,eth_row)
        profit = fitnessHelp(btc_arr, eth_arr, X)
        i+=1
    return -profit

def getDatafromExel(num_of_points ,file_name, start):
    df = pd.read_csv(file_name, usecols= [1], skiprows=start, nrows=num_of_points)
    arr =df.values.flatten()
    return arr
# arr[stoploss,takeprofit,timeout,UPPER_THRESHOLD,LOWER_THRESHOLD]
varbound=np.array([[-1000,0],[0,1000],[0,5*60],[0,5],[-5,0]])
vartype=np.array([['int'],['int'],['int'],['real'],['real']])

algorithm_param = {'max_num_iteration': 1000,\
                   'population_size':100,\
                   'mutation_probability':0.1,\
                   'elit_ratio': 0.01,\
                   'crossover_probability': 0.5,\
                   'parents_portion': 0.3,\
                   'crossover_type':'uniform',\
                   'max_iteration_without_improv':None}

model=ga(function=f,\
            dimension=5,\
            variable_type='real',\
            variable_boundaries=varbound,\
            variable_type_mixed=vartype,\
            algorithm_parameters=algorithm_param)

def runGa():
    model.run()
    return model.best_variable