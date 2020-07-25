import pandas as pd
import numpy as np
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
import pandas_market_calendars as mcal
import datetime
import copy

#  Pull Data
def get_Rolling_Data(ticker, startdate, enddate, period):  
    
    # Pull Stock Data
    stock_data = pd.DataFrame()
    stock_data[ticker] = wb.DataReader(ticker, data_source="yahoo", start=startdate, end=enddate)['Adj Close']
    stock_data['mov_avg'] = stock_data.rolling(window=period, min_periods=0).mean()

    # Plot Stock Data
    plot_graph(ticker, stock_data, period)
    
    # Return Data
    #return stock_data 

#   Plot Data  
def plot_graph(ticker, price_list, period):
    
    plt.style.use('seaborn-ticks')    
    plt.figure(figsize=(10,6))
    
    plt.title("Stock Price Over Time")
    plt.ylabel("Price of Stock ($)")
    plt.xlabel("Time (Trading Days)")
    
    plt.plot(price_list[ticker])
    plt.plot(price_list['mov_avg'], 'r:')
    plt.legend([ticker, str(period) + " Day Rolling Average"], loc=4)
    plt.show()
    
     
get_Rolling_Data('SPY', '2020-02-01', '2020-07-17', 5)
