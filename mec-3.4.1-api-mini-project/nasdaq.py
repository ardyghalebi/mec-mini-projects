'''
Assignment 3.4.1

Ardavan Ghalebi
'''

from dotenv import load_dotenv
import collections
import os
import json
import math
import requests

load_dotenv()
API_KEY = os.getenv('NASDAQ_API_KEY')

def analyze_data(exchange = 'FSE', ticker = ''):
    
    # Date range is all of 2017
    start_date = '2017-01-01'    
    end_date = '2017-12-31'

    # request data for 2017   
    base_url = f'https://data.nasdaq.com/api/v3/datasets/{exchange}/{ticker}/data.json?start_date={start_date}&end_date={end_date}&api_key={API_KEY}'
                
    response = requests.get(url=base_url, params={})
        
    if (response.ok):       
        # decode json response data to dictionary        
        data = response.json()   
        stock_values = data['dataset_data']['data']            
        day_count = 0  
        open_prices = []
        close_prices = []              
        daily_changes_high_low = {}
        daily_changes_closing = {}        
        trading_volume_dict = {}
        trading_volume_for_duration = 0
        entries = len(stock_values)

        for stock_value in stock_values:            
            open_price = 0
            
            # Indexing is easier with these
            stock_date = stock_value[0]
            open_price = stock_value[1]
            high_price = stock_value[2]
            low_price = stock_value[3]
            close_price = stock_value[4]     
            trading_volume = stock_value[6]

            if stock_value[1] != None:
                open_price = stock_value[1]
                
            else:                
                # To remediate data, we'll arbitrarily choose the previous day's closing price for cases where there is None opening price.
                print(f"[WARNING] No value found for Open price on {stock_date}. Choosing the previous day's Closing Price as an approximation.")                
                open_price = stock_values[day_count - 1][4]
            
            open_prices.append(open_price)                                                
            close_prices.append(close_price)
            daily_changes_high_low[stock_date] = abs(high_price - low_price)
            

            # Determine the total trading volume for the given date range 
            if (trading_volume != None):
                trading_volume_for_duration = trading_volume_for_duration + trading_volume
                trading_volume_dict[stock_date] = trading_volume
            
            day_count = day_count + 1       
        

        # Largest day change based on High and Low price
        largest_change_high_low_date = max(daily_changes_high_low, key=daily_changes_high_low.get)
        largest_change_high_low_value = daily_changes_high_low[largest_change_high_low_date]

        # The largest change between any two days is by definition the max(close_price) - min(close_price)
        largest_difference_closing_price = max(close_prices) - min(close_prices)
          
        # Answers        
        
        print(f"The highest opening price for date range {start_date} through {end_date} was: {max(open_prices)}.")
        print(f"The lowest opening price for the date range {start_date} through {end_date} was: {min(open_prices)}.")        
        print(f"The largest change in any one day (based on High and Low price) was: {largest_change_high_low_value} which occurred on {largest_change_high_low_date}.")
        print(f"The largest change between any two days (based on Closing price) was: {largest_difference_closing_price}.")
        print(f"Average trading volume was: {trading_volume_for_duration/entries}.")                
        find_median_trading_volume(trading_volume_dict)
                
    else:
        print(f'Error retrieving data: {response.status_code}')

    

"""
Find the median trading volume given a sorted dictionary of trading volumes. 
The median will be defined as:
    The middle number in a sorted list (assuming the len(dict) is odd)
    If the len(dict) is even, then the median is defined as the middle two numbers from the sorted dictionary.

"""
def find_median_trading_volume(trading_volumes):
    
    # Find sorted dates
    sorted_dates = sorted(trading_volumes.keys())

    size = len(sorted_dates)
    median_indices = []

    # After sorting, median index is the middle index (if odd)
    if size % 2 != 0:    
        median_date = sorted_dates[int(size / 2)] 
        print(f"Median trading volumen is {trading_volumes[median_date]} on {median_date}.")

    # After sorting, median index is the middle pair of indices (if even)    
    elif size % 2 == 0:        
        median_dates = [sorted_dates[int(size / 2)], sorted_dates[(int(size / 2)) + 1]]
        print(f"Median trading volumes are {trading_volumes[median_dates[0]]} on {median_dates[0]} and {trading_volumes[median_dates[1]]} on {median_dates[1]}.")
             


if __name__ == '__main__':
    print("Assignment 3.4.1")
    exchange = 'FSE'
    ticker = 'AFX_X'    
    analyze_data(exchange, ticker)
