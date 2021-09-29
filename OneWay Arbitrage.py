# -*- coding: utf-8 -*-
"""
Created on Sat May  8 09:13:31 2021

@author: lordd
"""

import numpy as np
import pandas as pd


def OnewayArbitrage (buy_currency,sell_currency,crosscurrency,initial_amount,bid):
    """
    

    Parameters
    ----------
    buy_currency : str
        Inserted by the user.
    sell_currency : str
        Inserted by the user.
    crosscurrency : str
        Crosscurrency.
    initial_amount : float
        amount of selling currency.
    bid : DataFrame
        Bid DataFrame.

    Returns
    -------
    result: float
        result of arbitrage execution.

    """
    result = initial_amount * bid.loc[crosscurrency,sell] * bid.loc[buy,crosscurrency]
    return result


FXMatrix = pd.read_excel("Quotation Matrix.xlsx",header=0,index_col=0)
k = len(FXMatrix)

currencies = np.array(FXMatrix.columns,dtype=str)

pd.options.display.float_format = "{:,.7f}".format

ask = np.zeros([k,k],dtype=float)
bid = np.zeros([k,k],dtype=float)

crosscurrency = " "
flipped_cur = np.flip(currencies)
strategy = pd.DataFrame(np.zeros([k-2,4],dtype=float), columns=["Sell","Buy","Via","Results"],
                        index = np.arange(1,k-1))

for i in range(k):
    for j in range(k):
        if FXMatrix.iloc[i,j] == np.nan:
            ask[i,j] = np.nan
            bid[i,j] = np.nan
        else:
            fx1 = FXMatrix.iloc[j,i]
            fx2 = 1/FXMatrix.iloc[k-1-i,k-1-j]
            if fx1 > fx2:
                ask[i,j] = fx1
                bid[i,j] = fx2
            else:
                ask[i,j] = fx2
                bid[i,j] = fx1

ask_frame = pd.DataFrame(np.transpose(ask), columns = currencies
                         ,index=np.flip(currencies,0))
bid_frame  = pd.DataFrame(np.transpose(bid), columns = currencies
                         ,index=np.flip(currencies,0))

flagbuy =0
while flagbuy == 0:
    print("Valid Currencies: ",np.transpose(currencies))
    buy = input("Please indicate the currency that you want to buy: ")
    buy = buy.upper()
    for i in range(k):
        if buy == currencies[i]:
            flagbuy =1
            break
        else:
            continue

flagsell =0
while flagsell == 0:
    print("Valid Currencies: ",np.transpose(currencies))
    sell = input("Please indicate the currency that you want to sell: ")
    sell = sell.upper()
    for i in range(k):
        if sell == currencies[i]:
            flagsell =1
            break
        else:
            continue



initial_amount = ask_frame.loc[sell,buy]

sum0 = 0
for i in range(k):
    crosscurrency = currencies[i]
    if buy != crosscurrency and sell !=crosscurrency:
        result=OnewayArbitrage(buy,sell,crosscurrency,initial_amount,bid_frame)
        strategy.iloc[sum0,0] = sell
        strategy.iloc[sum0,1] = buy
        strategy.iloc[sum0,2] = crosscurrency
        strategy.iloc[sum0,3] = result
        sum0 = sum0 + 1

print(strategy)
    

    
    
    
    
    