import numpy as np
from geneticalgorithm import geneticalgorithm as ga
from trade_strategy import fitnessHelp
import pandas as pd

index = 0

def f(X):
    global index
    btc_arr = getDatafromExel(100 ,'BTC-1-minute.csv')
    eth_arr = getDatafromExel(100 ,'ETH-1-minute.csv')
    index = index + 100
    profit = fitnessHelp(btc_arr, eth_arr, X)
    return -profit

def getDatafromExel(num_of_points ,file_name):
    df = pd.read_csv(file_name, usecols= [1], skiprows=index, nrows=num_of_points)
    arr =df.values.flatten()
    return arr
# arr[stoploss,takeprofit,timeout,UPPER_THRESHOLD,LOWER_THRESHOLD]
varbound=np.array([[-1000,0],[0,1000],[0,5*60],[0,5],[-5,0]])

algorithm_param = {'max_num_iteration': 100,\
                   'population_size':50,\
                   'mutation_probability':0.1,\
                   'elit_ratio': 0.01,\
                   'crossover_probability': 0.5,\
                   'parents_portion': 0.3,\
                   'crossover_type':'uniform',\
                   'max_iteration_without_improv':None}

model=ga(function=f,\
            dimension=5,\
            variable_type='int',\
            variable_boundaries=varbound,\
            algorithm_parameters=algorithm_param)

model.run()
print(model.best_variable[0])
print(-1*model.best_function)
