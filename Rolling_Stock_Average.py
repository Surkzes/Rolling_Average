import pandas as pd
import numpy as np
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
import pandas_market_calendars as mcal
import datetime
import copy


def ymd_to_dt(ymd_date):
    year, month, day = (int(x) for x in ymd_date.split('-'))    
    return datetime.date(year, month, day)


def get_business_days_list(startdate, enddate):   
    nyse = mcal.get_calendar('NYSE')
    business_days = nyse.valid_days(start_date=startdate, end_date=enddate).strftime('%Y-%m-%d')
    date_list = []
    for date in range(0, len(business_days) - 1):
        date_list.append(business_days[date])  
    return date_list


def market_closed(date, nyse):
    try:
        nyse.index(date)
        return False
    except: 
        return True
 
    
def get_rolled_back_start(start_date, period):
    
    delta = datetime.timedelta(days=(period * 2 + 5))
    nyse = get_business_days_list((ymd_to_dt(start_date) - delta).strftime('%Y-%m-%d'), start_date)
    new_start = nyse[len(nyse) - period:]
    
    return new_start[0]


def get_rolling_average(ticker, period, start_date, end_date):

    new_start_date = get_rolled_back_start(start_date, period)
    
    # Pull Stock Data
    stock_data = pd.DataFrame()
    stock_data = wb.DataReader(ticker, data_source="yahoo", start=new_start_date, end=end_date)['Adj Close']

    rolling_average = []
    for date in range(0, len(stock_data) - period):
        rolling_average.append(average(stock_data, period, date))
        
    return rolling_average

def average(stock_data, period, date):
    
    sum_ = 0
    
    for iterate in range(0, period):
        sum_ += stock_data[date + iterate]
        
    average = sum_ / period
    
    return average

def convert_data(twentyday_avg, stock_data):
    copy1 = copy.copy(stock_data)
    
    for date in range(0, len(stock_data)):
        copy1[date] = twentyday_avg[date]
    
    return copy1


def get_Stock_Data(ticker, startdate, enddate, period):  
    
    # Pull Stock Data
    stock_data = pd.DataFrame()
    stock_data = wb.DataReader(ticker, data_source="yahoo", start=startdate, end=enddate)['Adj Close']
    
    twentyday_avg = get_rolling_average(ticker, period, startdate, enddate)
    twentyday_avg = convert_data(twentyday_avg, stock_data)
    plot_graph(ticker, stock_data, twentyday_avg, period)


def plot_graph(ticker, price_list, rolling_average, period):
    
    plt.style.use('seaborn-ticks')    
    plt.figure(figsize=(10,6))
    
    plt.title("Stock Price Over Time")
    plt.ylabel("Price of Stock ($)")
    plt.xlabel("Time (Trading Days)")
    
    
    plt.plot(price_list)
    plt.plot(rolling_average, 'r:')
    plt.legend([ticker, str(period) + " Day Rolling Average"], loc=4)
    plt.show()
    
     
get_Stock_Data('SPY', '2019-02-01', '2020-07-17', 5)
