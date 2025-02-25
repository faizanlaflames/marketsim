""""""  		  	   		 	 	 			  		 			     			  	 
"""MC2-P1: Market simulator.  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		 	 	 			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		 	 	 			  		 			     			  	 
All Rights Reserved  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
Template code for CS 4646/7646  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		 	 	 			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		 	 	 			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		 	 	 			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		 	 	 			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		 	 	 			  		 			     			  	 
or edited.  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		 	 	 			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		 	 	 			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		 	 	 			  		 			     			  	 
GT honor code violation.  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
-----do not edit anything above this line---  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
Student Name: Faizan Hussain 		  	   		 	 	 			  		 			     			  	 
GT User ID: fhussain45  		  	   		 	 	 			  		 			     			  	 
GT ID: 904082279		  	   		 	 	 			  		 			     			  	 
"""  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
import datetime as dt  		  	   		 	 	 			  		 			     			  	 
import os  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
import numpy as np  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
import pandas as pd  		  	   		 	 	 			  		 			     			  	 
from util import get_data, plot_data  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
def compute_portvals(  		  	   		 	 	 			  		 			     			  	 
    orders_file="./orders/orders.csv",  		  	   		 	 	 			  		 			     			  	 
    start_val=1000000,  		  	   		 	 	 			  		 			     			  	 
    commission=9.95,  		  	   		 	 	 			  		 			     			  	 
    impact=0.005,  		  	   		 	 	 			  		 			     			  	 
):  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
    Computes the portfolio values.  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
    :param orders_file: Path of the order file or the file object  		  	   		 	 	 			  		 			     			  	 
    :type orders_file: str or file object  		  	   		 	 	 			  		 			     			  	 
    :param start_val: The starting value of the portfolio  		  	   		 	 	 			  		 			     			  	 
    :type start_val: int  		  	   		 	 	 			  		 			     			  	 
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		 	 	 			  		 			     			  	 
    :type commission: float  		  	   		 	 	 			  		 			     			  	 
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		 	 	 			  		 			     			  	 
    :type impact: float  		  	   		 	 	 			  		 			     			  	 
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		 	 	 			  		 			     			  	 
    :rtype: pandas.DataFrame  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
    # this is the function the autograder will call to test your code  		  	   		 	 	 			  		 			     			  	 
    # NOTE: orders_file may be a string, or it may be a file object. Your  		  	   		 	 	 			  		 			     			  	 
    # code should work correctly with either input  		  	   		 	 	 			  		 			     			  	 
    # TODO: Your code here  	

    orders_df = pd.read_csv(orders_file, parse_dates=True, index_col='Date')

    # get unique symbols from orders
    symbols = orders_df['Symbol'].unique().tolist()

    # start and end dates
    start_date = orders_df.index.min()
    end_date = orders_df.index.max()

    # adjusted close prices
    prices = get_data(symbols, pd.date_range(start_date, end_date))
    prices = prices[symbols]  # remove spy if present

    # init trades datafram
    trades = pd.DataFrame(0.0, index=prices.index, columns=symbols + ['Cash'])
    trades['Cash'] = 0.0

    # process orders
    for date, order in orders_df.iterrows():
        symbol = order['Symbol']
        order_type = order['Order']
        shares = order['Shares']

        # get price for symbol
        price = prices.loc[date, symbol]

        # calculate transaction cost
        if order_type == 'BUY':
            cost = shares * price * (1 + impact)
            trades.loc[date, symbol] += shares
            trades.loc[date, 'Cash'] -= cost
        elif order_type == 'SELL':
            cost = shares * price * (1 - impact)
            trades.loc[date, symbol] -= shares
            trades.loc[date, 'Cash'] += cost  # fix: add sale proceeds

        # deduct commission
        trades.loc[date, 'Cash'] -= commission

    # init holdings df
    holdings = pd.DataFrame(0.0, index=prices.index, columns=symbols + ['Cash'])
    holdings.iloc[0] = trades.iloc[0]
    holdings.loc[start_date, 'Cash'] += start_val  # add starting cash

    # calculate cumulative holdings
    for i in range(1, len(holdings)):
        holdings.iloc[i] = holdings.iloc[i - 1] + trades.iloc[i]

    # calculate portfolio value
    portvals = (prices * holdings[symbols]).sum(axis=1) + holdings['Cash']
    portvals = pd.DataFrame(portvals, columns=['Portfolio Value'])

    return portvals		     			  	 
  		  	   		 	 	 			  		 			     			  	 

def test_code():
    """
    Helper function to test code
    """
    # define input parameters
    of = "./orders/orders2.csv"  
    sv = 1000000  # portfolio starting value

    # Process orders
    portvals = compute_portvals(orders_file=of, start_val=sv)

    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # Just get the first column
    else:
        print("warning, code did not return a DataFrame")

    # start_date = portvals.index.min()
    # end_date = portvals.index.max()

    
    # cum_ret = (portvals[-1] / portvals[0]) - 1

   
    # daily_rets = (portvals / portvals.shift(1)) - 1
    # daily_rets = daily_rets[1:]  # Remove the first row (NaN)

   
    # avg_daily_ret = daily_rets.mean()
    # std_daily_ret = daily_rets.std()

    
    # sharpe_ratio = np.sqrt(252) * (avg_daily_ret / std_daily_ret)

    # spy_prices = get_data(['SPY'], pd.date_range(start_date, end_date))
    # spy_prices = spy_prices[['SPY']]  # Remove other columns if present

    
    # spy_cum_ret = (spy_prices.iloc[-1] / spy_prices.iloc[0]) - 1
    # spy_daily_rets = (spy_prices / spy_prices.shift(1)) - 1
    # spy_daily_rets = spy_daily_rets[1:]  # Remove the first row (NaN)
    # spy_avg_daily_ret = spy_daily_rets.mean()
    # spy_std_daily_ret = spy_daily_rets.std()
    # spy_sharpe_ratio = np.sqrt(252) * (spy_avg_daily_ret / spy_std_daily_ret)

    # print(f"Date Range: {start_date} to {end_date}")
    # print()
    # print(f"Sharpe Ratio of Fund: {sharpe_ratio}")
    # print(f"Sharpe Ratio of SPY : {spy_sharpe_ratio}")
    # print()
    # print(f"Cumulative Return of Fund: {cum_ret}")
    # print(f"Cumulative Return of SPY : {spy_cum_ret}")
    # print()
    # print(f"Standard Deviation of Fund: {std_daily_ret}")
    # print(f"Standard Deviation of SPY : {spy_std_daily_ret}")
    # print()
    # print(f"Average Daily Return of Fund: {avg_daily_ret}")
    # print(f"Average Daily Return of SPY : {spy_avg_daily_ret}")
    # print()
    # print(f"Final Portfolio Value: {portvals[-1]}")	 

def author():
    return "fhussain45"

def study_group():
    return "fhussain45"
  		  	   		 	 	 			  		 			     			  	 
if __name__ == "__main__":  		  	   		 	 	 			  		 			     			  	 
    test_code()  		  	   		 	 	 			  		 			     			  	 



