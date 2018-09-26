
import os
import sys, getopt

import itertools

from lib import sharedfunctions as fn
from lib import main as mn
from lib import knndata

from timeit import default_timer as timer
import datetime as dt

from datetime import datetime

from lib import technical_indicators as ti

import pandas as pd
import numpy as np
from numpy import array

import copy

import time

global ofile
global linecount

para  = ''

def main(market):

        global ofile
        global linecount

        directory = "data\\google\\"
        filepath = directory + "gdata.csv"
        global df_googleData
        df_googleData = pd.read_csv(filepath)

        fnn = "autotrade-" + market
        outputfile1 = 'data\\google\\' + fnn + ".csv"
        ofile = open(outputfile1, "w")
        linecount = 0
            
        ls_symbols = fn.readsymbols(df_googleData,market)

        for symbol in ls_symbols:
                print symbol
                ret = select(symbol)

        ofile.close()


def formatter(df_date,symbol, quantity):
        global ofile
        global linecount

        colheader = "SYMBOL"
        data = symbol

        colheader = colheader + ",DATE" 
        #dt_date1 = dt.datetime.strptime(df_date['DATE'], '%Y-%m-%d').date()
        fdate = df_date['DATE'].strftime("%#m/%#d/%Y")        
        data = data + "," + str(fdate)

        colheader = colheader + ",SHARES"
        data = data + "," + str(quantity)
        
        colheader = colheader + ",PRICE"
        price = round(df_date['CLOSE'],2)
        data = data + "," + str(price)
        
        colheader = colheader + ",COMMISSION"
        commission = abs(price * quantity) * 0.0031
        data = data + "," + str(commission)
                      
        colheader = colheader + ",CASHONHAND"
        amount = (-quantity * price) - commission
        data = data + "," + str(amount)

        colheader = colheader + ",DIVIDEND"
        data = data + ",0"

        colheader = colheader + ",TURNOVER"
        data = data + "," + str(abs(amount))
                      
        colheader = colheader + ",PERIOD"
        period = df_date['DATE'].strftime("%Y%m")        
        data = data + "," + str(period)
                      
                      
        colheader = colheader + ",TYPE"
        data = data + ",AUTO TRADE"

        colheader = colheader + ",BROKER"
        data = data + ","
                      
        colheader = colheader + ",IB-ASX"
        data = data + ","
                      
        colheader = colheader + ",IB-HSI"
        data = data + ","
                      
        colheader = colheader + ",SCB"
        data = data + ","                

        if linecount == 0:
                ofile.write(colheader + "\n")
        
        ofile.write(data + "\n")

        linecount = linecount + 1
        
        
def select(symbol):


        df_rawdata = knndata.getRawData(symbol,False)
        dataset = knndata.prepareData(df_rawdata,symbol)

        print "Preparing data"

        directory = "data\\knndata\\"
        filename = fn.filenameFormatter(symbol)
        filepath = directory + filename + '.csv'
        df = pd.read_csv(filepath)

        df['DATE'] =  pd.to_datetime(df['DATE']).apply(lambda x: x.date())

        l = len(df)

        for i in range(0,l):
                df_date = df.iloc[i]
                if (df_date['HIGHCHG'] < 1) & (df_date['LOWCHG'] < 1):
                        formatter(df_date,symbol,-100)

                if ((df_date['LOWCHG'] > 1) & (df_date['HIGHCHG'] > 1)) or ((df_date['RSI9']/df_date['RSI9CHG'] < 30) &(df_date['RSI9CHG'] > 1)):
                        formatter(df_date,symbol,100)

        return df


if __name__ == '__main__':

    argv = sys.argv

    
    if len(argv)>1:
        para = ",".join(argv)
        main(argv[1])
        print "[" + para + "]"
    else:
        main('ASX')
        #main('HSI')
