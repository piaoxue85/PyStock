
import os
import sys, getopt

import itertools

from lib import sharedfunctions as fn
from lib import download as dl
from lib import knndata
from lib import main as mn
from lib import consolidate as consol
from lib import globaldf

from timeit import default_timer as timer
import datetime as dt

from lib import formatter as fileformatter

import pandas as pd
import numpy as np

import glob

import copy

import time

import csv

global argv
global ofilename

global df_googleData

gdir = "data\\google\\"

para  = ''

def run(ls_symbols, dfs):

        for s in ls_symbols:
                try:
                        mn.run(s, dfs)                     
                except Exception as e:
                        print s + ' ' + str(e)
                except SystemExit as e:
                        print s + ' ' +  str(e)

        return

def main_bstrans():

        directory = "\\python\\data\\google\\"
        filepath = directory + "transactions.csv"

        df_trans = pd.read_csv(filepath)   

        df_trans = fn.format_df_trans(df_trans)

        print df_trans

        sym = 'GOOG'

        avgprice, qty, amt, accmulamt, btrans, strans = fn.readTrans(df_trans, sym)

        print str(btrans['PRICE']).replace(",","")
        print str(strans['PRICE']).replace(",","")

def main():
        
        directory = "data\\historical\\raw\\"
        filepath = directory + "ASX-CBA.csv"
        df_rawdata = pd.read_csv(filepath)
        df_rawdata['Date'] =  pd.to_datetime(df_rawdata['Date']).apply(lambda x: x.date())        
        print df_rawdata.iloc[-5:-1]
        df_data = knndata.formatGoogleData(df_rawdata)
        print df_data.iloc[-5:-1]
        df_data = knndata.formatGoogleDataOld(df_rawdata)
        print df_data.iloc[-5:-1]        

def main_getdata():

#Test main for knn.getdata

        s = 'VIX'   
        df_rawdata = knndata.getRawData(s,True)
        fs = fn.filenameFormatter(s)
        try:
                dataset = knndata.prepareData(df_rawdata,fs)
        except SystemExit as e:
                print e

        print "See " + fs
        
def main_download():
        #dl.transactions()



        url1 = 'https://query1.finance.yahoo.com/v7/finance/download/symbol?period1=1284559200&period2=1537020000&interval=1d&events=history&crumb=5m0v4UmYimf'
##        df = dl.downloadfromgoogle(url)
##        print df


        market = 'NYSE'
        dfs = mn.prepareRefDf(market)
        df_googleData = dfs[0]
        ls_symbols = fn.readsymbols(df_googleData,market)
        for symbol in ls_symbols:
                print '"' + symbol + '",'
                

        return

def main_backtest():

        market = 'HSI'
        odir = "results\\listdata\\"
        ofilename = 'list-' + market + '.csv'
        filepath = odir + ofilename

        print filepath
        df_output = pd.read_csv(filepath)

##        with open(filepath, 'rb') as csvfile:
##                lines = csv.reader(csvfile)
##                dataset = list(lines)
##

   
        return
   
        
def main_analyse():

#Test main for main.run
        
        #dl.googleData()
        #dl.transactions()
        
        fnn = "results\\Onhand.csv"
        sfile = fnn
        hfile = fnn.replace(".csv",".htm")
        fileformatter.convertfile(sfile,hfile) 

##        files = glob.glob("results\\transanalysis\\*.csv")
##
##        for fnn in files:
##                sfile = fnn
##                hfile = fnn.replace(".csv",".htm")
##                fileformatter.convertfile(sfile,hfile)        

        directory = "data\\google\\"
        filepath = directory + "gdata.csv"
        global df_googleData
        #df_googleData = pd.read_csv(filepath)
        
        markets = []
        for market in markets:
                dfs = mn.prepareRefDf(market)
                df_googleData = dfs[0]
                ls_symbols2 = fn.readsymbols(df_googleData,market)
                run(ls_symbols2, dfs)

        markets = ['ASX','NYSE','HSI']
        for market in markets:
                consol.run(market)
        
        #consol.run(market)        
        
        #for s in ls_symbols1:
        #        try:
        #                ls_symbols2.remove(s)
        #        except:
        #                fn.dprint(s + " is not in ls_symbols2")
        
        #print ls_symbols2

        #consol.run()

        #url = "http://www.asx.com.au/prices/asx-benchmark-rates.htm"

        #dl.quotefromgoogle(url,"download.htm")

def getSymbols():
        
        global df_googleData
            
        ls_symbols1 = fn.readsymbols(df_googleData,'HSI')
        ls_symbols2 = fn.readsymbols(df_googleData,'ASX')
        ls_symbols3 = fn.readsymbols(df_googleData,'NYSE')

        ls_symbols = ls_symbols1 + ls_symbols2 + ls_symbols3

        return ls_symbols

def main_data():
        
        ls_symbols = getSymbols()

        ls_symbols = ['VIX']
        
        for symbol in ls_symbols:
            fnn = fn.filenameFormatter(symbol)
            ydir = "data\\historical\\data1\\"
            filepath = ydir + fnn + ".csv"
            df_data1 = globaldf.read(filepath)

            fnn = fn.filenameFormatter(symbol)
            gdir = "data\\historical\\data2\\"            
            filepath = gdir + fnn + ".csv"
            df_data2 = globaldf.read(filepath)

##            ydates = df_data1['DATE']
##            gdates = df_data2['DATE']
##
##            g = df_data2.DATE.isin(ydates)
##
##            y = df_data1[~df_data1['DATE'].isin(gdates)]
##
##            r = fn.dfconcat(df_data2,y)

            df_result = knndata.mergeRawData(df_data1, df_data2)
            directory2 = "data\\historical\\result\\"
            filepath2 = directory2 + symbol + ".csv"
            df_result.to_csv(filepath2, index=False)

        return
             
status = "test"
filepath = gdir + "gdata.csv"
df_googleData = globaldf.read(filepath)  
main_analyse()
