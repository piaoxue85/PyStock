
import os
import sys, getopt

import itertools

from lib import sharedfunctions as fn
from lib import download as dl
from lib import knndata
from lib import main as mn
from lib import consolidate as consol

from timeit import default_timer as timer
import datetime as dt
from lib import formatter as fileformatter

import pandas as pd
import numpy as np

import numpy
import talib

from lib import talibw

import talib

import trade

#from talib import MA_Type

import glob

import copy

import time

global argv
global ofilename

para  = ''
shiftdays = [1,2,3,4,5,10,20]
patterns = talibw.getcdlpatterns()

def run(sym):

        df_rawdata = knndata.getRawData(sym,True)
        df_quote = knndata.readQuote(knndata.getQuoteFilepath(sym))

        if df_rawdata.iloc[-1]['DATE'] == df_quote.iloc[-1]['DATE']:
                df_rawdata = df_rawdata.iloc[0:-1]

        fs = fn.filenameFormatter(sym)        
        df_result = pd.DataFrame()

        patterns = talibw.getcdlpatterns()
        df_basedata = df_rawdata.copy()

        rsi = talib.RSI(df_basedata['CLOSE'],9)
        df_rsi = pd.DataFrame(rsi, columns=['RSI9'])
        df_basedata = pd.concat([df_basedata, df_rsi], axis=1)
        df_basedata['RSI9CHG'] = df_basedata['RSI9']/df_basedata['RSI9'].shift(1)

        print df_basedata.iloc[-10:]

        df_result = pd.DataFrame()
        
        for day in shiftdays:
                df_basedata = dayshift(df_basedata,day)

        for pattern in patterns:
                pts = talibw.recg_pattern(df_rawdata,pattern)
                retval = pts.iloc[-1]
                if retval <> 0:
                        print sym, pattern, retval 
                        df_pts = pd.DataFrame(pts, columns=[pattern])
                        df_signaldata = pd.concat([df_basedata, df_pts], axis=1)
##                        df_signaldata.to_csv('data\\signal\\' + sym + '-' + pattern + '.csv', index=False)                  
                        df_stat = analyse(df_signaldata, pattern, retval)
                        df_stat.insert(0, 'SYMBOL', sym) 
                        df_stat.insert(1, 'DATADATE',df_rawdata.iloc[-1]['DATE'])
                        df_stat.insert(2, 'QUOTEDATE', df_quote.iloc[-1]['DATE'])
                        df_stat.insert(3, 'LASTCLOSE', df_rawdata.iloc[-1]['CLOSE'])                        
                        df_stat.insert(4, 'CLOSE', df_quote.iloc[-1]['CLOSE'])
                        closechg = round((df_quote.iloc[-1]['CLOSE'] / df_rawdata.iloc[-1]['CLOSE'])*100-100,2)
                        df_stat.insert(5, 'CLOSECHG', closechg)
                        
                        result = ''
                        if df_stat['ACTION']=='BUY' and closechg > 0:
                                result = 'HIT'
                                
                        if df_stat['ACTION']=='BUY' and closechg < 0:
                                result = 'MISS'

                        if df_stat['ACTION']=='SELL' and closechg < 0:
                                result = 'HIT'
                                
                        if df_stat['ACTION']=='SELL' and closechg > 0:
                                result = 'MISS'

                        df_stat.insert(6,'RESULT', result)                        
                        
                        df_result = fn.dfconcat(df_result,df_stat)

        return df_result

def dayshift(df_price,days=1):

        ls_data = df_price.iloc[days:]['CLOSE'].tolist()
        colname = str(days) + 'D'
        df_shift = pd.DataFrame(ls_data, columns=[colname])
        df_shift.index = range(len(df_shift.index))

        df_merged = df_price.copy() 
        df_merged = pd.concat([df_merged, df_shift], axis=1, join='outer')
        df_merged[colname + 'CHG'] = df_merged[colname] / df_merged['CLOSE']

        return df_merged

def analyse(df_data, pattern, retval):

        df_signal = df_data[(df_data[pattern] == retval)]

        ls_shd = []
        ls_stat = []

        ls_shd.append('PATTERN')
        ls_stat.append(pattern + str(retval))        

        tcount = len(df_data)
        scount = len(df_signal)        
        spct = round((float(scount) / float(tcount)) * 100,1)

        ls_shd.append('SIGNALPCT')
        ls_stat.append(spct)

        vals = []
        for day in shiftdays:
                colname = str(day) + 'DCHGAVG-PCT'
                ls_shd.append(colname)
                colname = str(day) + 'DCHG'           
                val = round((df_signal[colname].mean()*100)-100,2)
                vals.append(val)
                ls_stat.append(val)

                df_win = df_signal[(df_signal[colname] > 1)]
                colname = str(day) + 'DWIN-PCT'
                ls_shd.append(colname)
                colname = str(day) + 'DCHG' 
                val = round((float(df_win[colname].count())/float(scount))*100,2)
                ls_stat.append(val)                

        minval = min(vals)
        maxval = max(vals)

        signal = ''

        if minval > 0 and maxval > 0:
                signal = 'BUY'

        if minval < 0 and maxval < 0:
                signal = 'SELL'                
                
        ls_shd.insert(1,'ACTION')
        ls_stat.insert(1,signal)

        ls_shd.append('TRADEDAYS')       
        ls_stat.append(tcount)
        
        ls_shd.append('SIGNALCOUNT')        
        ls_stat.append(scount)        
                
        df_stat = pd.DataFrame([ls_stat], columns=ls_shd)

        return df_stat        

def main():

        directory = "data\\google\\"
        filepath = directory + "gdata.csv"
        global df_googleData
        df_googleData = pd.read_csv(filepath)

        directory = "\\python\\data\\google\\"
        filepath = directory + "transactions.csv"

        df_trans = pd.read_csv(filepath)
        ls1 = df_trans.SYMBOL.unique()

        markets = ['ASX','HSI','NYSE']

        odir = "results\\"        

        for market in markets[2:]:
                
                df_summary = pd.DataFrame()                
                dfs = mn.prepareRefDf(market)
                df_googleData = dfs[0]
                ls_symbols2 = fn.readsymbols(df_googleData,market)
                ls_symbols2 = ['ASX-CBA']
                
                for s in ls_symbols2:
                        try:
                                df_result = run(s)
                                df_summary = fn.dfconcat(df_summary,df_result)
                        except SystemExit as e:
                                print "System Exit Error " + s + " - " + + str(e)
                        except Exception, e:
                                print "Error " + s + " - " + str(e)

                ofilename = 'SignalScan-' + market
                sfile = odir + ofilename + '.csv'                
                df_summary.to_csv(sfile, index=False)  
                hfile = odir + ofilename + '.htm'        
                fileformatter.convertfile(sfile,hfile)                

        print 'Completed'
                                
                                        
main()
