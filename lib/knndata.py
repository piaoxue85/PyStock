
#implement MACD http://www.investopedia.com/ask/answers/122414/what-moving-average-convergence-divergence-macd-formula-and-how-it-calculated.asp

import csv
import sharedfunctions as fn

import os
import sys, getopt
import time
import shutil
import pandas
import math

import datetime as dt

import technical_indicators as ti

import pandas
import copy

import numpy as np
from numpy import array

import globalfd
import globaldf

global writeFile

hdir = "data\\historical\\"
qdir = "data\\dayquote\\"
kdir = "data\\knndata\\"

hheaders = ['DATE','OPEN','HIGH','LOW','CLOSE','VOLUME','ADJ CLOSE','SOURCE']
qheaders = ['SYMBOL','CLOSE','DATE','TIME','CHANGE','OPEN','HIGH','LOW','VOLUME','SOURCE']

def openFile(fnn):

    global outputfile1
    global text_file1
    global writeFile

    if writeFile == True:

        fnn = fn.filenameFormatter(fnn)

        outputfile1 = kdir + fnn + '.csv'
    
        try:
            text_file1 = open(outputfile1, "w")
        except:
            print "Error when opening " + outputfile1
            
    return

def printout(str):

    global writeFile

    if writeFile == True:
        try:
            text_file1.write(str + '\n')
        except:
            print "Error when writing " + outputfile1

    return

def closeFile():

    global writeFile

    if writeFile == True:    
        try:
            text_file1.close()
        except:
            print "Error when closing " + outputfile1

    return


def getbb(prices, interval=20):

    means = pandas.rolling_mean(prices,interval,min_periods=interval)
    std = pandas.rolling_std(prices, interval, min_periods=interval)
    bb = (prices - means) / std
    c = len(bb)
    #Fixing inf value in bollinger band
    for x in range(0,c-1):
        if math.isinf(bb[x]):
            bb[x] = bb[x-1]
        
    return bb

def getData(symbol, beginDate, endDate, wfile=True, cache=False):

    if cache==True:
        ls_data = readCache(symbol,beginDate, endDate)
        if len(ls_data) > 0:
            return ls_data
    
    #if len(beginDate) > 0 and len(endDate) > 0:
    #    df = df_rawdata[(df_rawdata['DATE'] >= beginDate) & (df_rawdata['DATE'] <= endDate)]
    #else:
    #    df = df_rawdata

    df_rawdata = getRawData(symbol)

    df = df_rawdata[(df_rawdata['DATE'] >= beginDate) & (df_rawdata['DATE'] <= endDate)]

    df_tdata = prepareData(df, symbol,wfile)
    
    return df_tdata

def run():

    global ls_symbols

    ls_symbols = fn.readsymbols('HSI')
    for s in ls_symbols:

        df_rawdata = getRawData(s)

        for d in range(0,1):
            prepareData(df_rawdata, s, d)

def formatQuote(fdate,Open=0,High=0,Low=0,Close=0,Volume=0,AdjClose=0,Source=''):
    qd = pandas.DataFrame([[fdate,float(Open),float(High),float(Low),float(Close),float(Volume),float(AdjClose),str(Source)]], columns=hheaders)
    return qd

def readQuote(filepath):
    #LATEST QUOTE
    df_data = pandas.read_csv(filepath,names=qheaders)

    globaldf.update([filepath,df_data])
    df_data = changedftouppercase(df_data)

    df_data['DATE'] =  pandas.to_datetime(df_data['DATE']).apply(lambda x: x.strftime('%m/%d/%Y'))
    df_data['DATE'] =  pandas.to_datetime(df_data['DATE']).apply(lambda x: x.strftime('%Y-%m-%d'))
    df_data['DATE'] =  pandas.to_datetime(df_data['DATE']).apply(lambda x: x.date())

    df_data = df_data.iloc[-1]
    
    return df_data

def getQuoteFilepath(s):
    fnn = fn.filenameFormatter(s)
    filepath2 = qdir + fnn + ".csv"
    return filepath2

def appendQuote(df_data1, df_data2):

    df_data = pandas.DataFrame()

    try:
        if len(df_data2) > 0:
            
            dt_date2 = df_data2['DATE']
            fdate = dt_date2            
            data = [fdate,float(df_data2['OPEN']),float(df_data2['HIGH']),float(df_data2['LOW']),float(df_data2['CLOSE']),float(df_data2['VOLUME']),float(df_data2['CLOSE']),df_data2['SOURCE']]
            qd = pandas.DataFrame([data],columns=hheaders)
 
        if len(df_data1) > 0 and len(df_data2) > 0:

            df_hdata = df_data1[df_data1.DATE == dt_date2]
            df_hdata = df_hdata[df_hdata.SOURCE <> 'GOOG-Q']

            #If price quote cannot be found in historical data
            if len(df_hdata) == 0 :
                df_data1 = df_data1[df_data1.DATE != dt_date2]        
                df_data = fn.dfconcat(df_data1, qd)
                df_data['DATE'] =  pandas.to_datetime(df_data['DATE']).apply(lambda x: x.date())

        if len(df_data) == 0:
            df_data = df_data1

        if len(df_data) == 0:
            df_data = qd

    except Exception as e:
        
        df_data = df_data1        
        print "append quote error " + str(e)

    return df_data

def formatGoogleData(df_data2):

        #Change all column labels to upper case, all columns label are in upper case in the entire program
        llabels = df_data2.columns.values.tolist()
        ulabels = map(str.upper,llabels)
        df_data2.columns = [ulabels]
        del df_data2['SYMBOL']
        df_data2 = df_data2.replace('#N/A',np.NaN)
        df_data2['OPEN'].astype('float')
        df_data2['HIGH'].astype('float')
        df_data2['LOW'].astype('float')
        df_data2['CLOSE'].astype('float')
        df_data2['VOLUME'].astype('float')        
        df_data2= df_data2.fillna(method='ffill')
        df_data2['ADJ CLOSE'] = df_data2['CLOSE']
        df_data2['SOURCE'] = 'GOOG-H'
        
        return df_data2

def formatYahooData(df_data2):

        #Change all column labels to upper case, all columns label are in upper case in the entire program
        llabels = df_data2.columns.values.tolist()
        ulabels = map(str.upper,llabels)
        df_data2.columns = [ulabels]
        df_data2['DATE'] =  pandas.to_datetime(df_data2['DATE']).apply(lambda x: x.date())        
        df_data2 = df_data2.replace('null',np.NaN)        
        df_data2 = df_data2[['DATE','OPEN','HIGH','LOW','CLOSE','VOLUME','ADJ CLOSE']]
        numcols = ['OPEN','HIGH','LOW','CLOSE','ADJ CLOSE']
        df_data2 = globaldf.rounddf(df_data2, numcols, 4)
        df_data2= df_data2.fillna(method='ffill')        
        df_data2['SOURCE'] = 'YA-H'      
        
        return df_data2

##Merging raw data files from different sources
##28 Sep 2018
def mergeRawData(df1, df2):

    colname = 'DATE'

    df4 = pandas.DataFrame()

    #REMOVING DAY QUOTE
    df1 = df1[df1['SOURCE']!='GOOG-Q']

    if len(df1) > 0 and len(df2) > 0:
        
        val = df1[colname]

        df3 = df2[~df2[colname].isin(val)]

        df4 = fn.dfconcat(df1,df3)

    if len(df2) == 0:

        df4 = df1

    if len(df4) == 0:

        df4 = df2

    if len(df4) > 0:

        df4 = df4.sort(colname)
        df4.index = range(len(df4.index))
        numcols = ['OPEN','HIGH','LOW','CLOSE','ADJ CLOSE']
        df4 = globaldf.rounddf(df4, numcols, 4)    

    return df4


def getRawData(s, readquote = True):
    #HISTORICAL
    fnn = fn.filenameFormatter(s)
    filepath = hdir + fnn + ".csv"

    #df_data1 = pandas.read_csv(filepath)
    df_data1 = globaldf.read(filepath)
    if len(df_data1) > 0:
        df_data1 = changedftouppercase(df_data1)
        df_data1['DATE'] =  pandas.to_datetime(df_data1['DATE']).apply(lambda x: x.date())    

    #LATEST QUOTE, APPEND ONLY IF TRUE
    if(readquote==True):
        filepath2 = qdir + fnn + ".csv"
        df_data2 = readQuote(filepath2)
        df_data = appendQuote(df_data1,df_data2)        
    else:        
        df_data = df_data1

    df_data = df_data.sort('DATE')

    #22 AUG 2018
    #For applying index starting from 0
    df_data.index = range(len(df_data.index))

    return df_data

def calcChg(v1, v2):

    try:
        if v2 == 0:
            v = 0
        else:
            v = float(v1) / float(v2)
    except:
        v = 0
        
    return v

def calcMACD(values, days):

#1. Calculate a 12-period EMA of price for the chosen time period.
#2. Calculate a 26-period EMA of price for the chosen time period.
#3. Subtract the 26-period EMA from the 12-period EMA.
#4. Calculate a nine-period EMA of the result obtained from step 3.

#   This nine-period EMA line is overlaid on a histogram that is created by subtracting the nine-period EMA from the result in step 3, which is called the MACD line, but it is not always visibly plotted on the MACD representation on a chart.
#   The MACD also has a zero line to indicate positive and negative values. The MACD has a positive value whenever the 12-period EMA is above the 26-period EMA and a negative value when the 12-period EMA is below the 26-period EMA.

    emaslow = []
    emafast = []
    emadiff = []
    emasignal = []
    emaos = []
    macd = []
    for i in range(0, len(days)):
        emafast = ti.ema(values, days[i][0])
        emaslow = ti.ema(values, days[i][1])
        emadiff = emaslow - emafast[(days[i][1]-days[i][0]):]
        signal = ti.ema(emadiff, days[i][2])
        macd.insert(0,signal)   
    return macd

#10 Feb 2017
#To get field index of selected fields
#allfields: list of all fields
#selection: list of selected fields
def getFieldIndex(allfields, selection):

    c = 0
    index = []
    for f in allfields:
        if f in selection:
            index.append(c)
        c= c + 1

    return index

#10 Feb 2017
#To get field index of fields with exclusion
#allfields: list of all fields
#excluded: list of excluded fields
def getFieldIndexExclude(allfields, excluded):
    c = 0
    index = []
    for f in allfields:
        if not f in excluded:
            index.append(c)
        c= c + 1
    return index

def removeCache(s):

    fnn = fn.filenameFormatter(s)
    filepath = kdir + fnn + '.csv'

    try:            
        os.remove(filepath)

    except:
        print "Error - removing " + filepath

    return 

def readCache(s, beginDate, endDate):

    fnn = fn.filenameFormatter(s)
    filepath = kdir + fnn + '.csv'
    ls_data = []

    try:            
        #df_data = pandas.read_csv(filepath)
        df_data = globaldf.read(filepath)
        df_data = changedftouppercase(df_data)
        df_data['DATE'] =  pandas.to_datetime(df_data['DATE']).apply(lambda x: x.date())
        df_data = df_data[(df_data['DATE'] >= beginDate) & (df_data['DATE'] <= endDate)]
        df_data = df_data.sort(['DATE'])
        df_data['DATE'] =  pandas.to_datetime(df_data['DATE']).apply(lambda x: x.strftime('%Y-%m-%d'))
        ls_data = df_data.values.tolist()
        ls_data.insert(0,df_data.columns.values.tolist())

    except:
        print "Error in opening " + filepath


    return ls_data
    

def prepareData(df_data, s, wfile=True):

        global writeFile

        writeFile = wfile

        data = []

        openFile(s)

        rc = len(df_data.index)# - delta #row count
        lr = [] #Last row
        nr = []

        tc = 0 #trend counter
        lt = 0 #trend
        t = 0 #current trend

        tchg = 0 #trend change
        tchgpct = 0

        priceCol = 'CLOSE'

        ls_rsi = []
        ls_rsios = []

        ls_fd = []  #Field description

        rp = [9,11,14,25]
        #17 Feb 2018
        #Getting max rsi and min rsi, last record only
        rsiCols = ['CLOSE','LOW','HIGH']
        for rsiCol in rsiCols:
            rsi = []
            rsios = []
            for i in range(0, len(rp)):
                vals = df_data[priceCol].values.copy()                         
                vals[-1] = df_data.iloc[-1][rsiCol]
                rsi.append(ti.rsi(vals, rp[i]))
                rsios.append(rc - len(rsi[i]))
            ls_rsi.append(rsi)
            ls_rsios.append(rsios)

        sp = [5,10,20,50,100,200]
        sma = []
        smaos = []
        for i in range(0, len(sp)):
            sma.append(ti.sma(df_data[priceCol].values, sp[i]))
            smaos.append(rc - len(sma[i]))

        macddays = [[12,26,9]]
        macd = calcMACD(df_data[priceCol].values,macddays)
        macdos = []
        for i in range(0, len(macddays)):
            macdos.append(rc - len(macd[i]))
                        
        bb = getbb(df_data[priceCol].values,20)
        roc = ti.roc(df_data[priceCol].values,period=20)

        #D1015
        lvp = [5,10,20,50,100,200,252]  #Price level periods
        ls_highs = [] #Price high
        ls_lows = [] #Price low
        for i in range(0, len(lvp)):
            highs = pandas.rolling_max(df_data['HIGH'].values,lvp[i],lvp[i])
            lows = pandas.rolling_min(df_data['LOW'].values,lvp[i],lvp[i])
            ls_highs.append(highs)
            ls_lows.append(lows)

        minperiod = 252
        offset = minperiod + 1

        rh = [0] * len(lvp)
        rl = [0] * len(lvp)
        
        for r in range(offset, rc):

            ls_fd = []            

            cr = df_data.iloc[r]
            lr = df_data.iloc[r - 1]
            if(rc > r+1):
                nr = df_data.iloc[r + 1]
            else:
                nr = []
           
            #if cr['Volume'] > 0 and len(lr) > 0:
            #Some older HSI data volume = 0
            if len(lr) > 0:
            
                l = ""
                h = ""
                
                #dt_date = dt.datetime.strptime(cr['DATE'], '%Y-%m-%d').date()

                dt_date = cr['DATE']

                h = h + hheaders[0].upper() + ","
                l = l + str(cr['DATE']) + ","

                for c in range(1, 6):
                    v = float(cr[c]) 
                    h = h + hheaders[c].upper() + ","
                    l = l + str("%.4f" % round(v,4)) + ","

                #HIGH,LOW,CLOSE,VOLUME,ADJ CLOSE
                for c in [2,3,4,5,6]:
                    p = 0
                    if lr[c] > 0:
                        v = float(cr[c]) / float(lr[c])
                        s = v
                    h = h + hheaders[c].upper() + "CHG,"
                    l = l + str("%.4f" % round(v,4)) + ","

                v1 = cr[2]
                v2 = lr[6]
                v = calcChg(v1,v2)
                h = h + "CLOSEOPENCHG,"
                l = l + str("%.4f" % round(v,2)) + ","
                
                if cr['HIGH'] > cr['LOW']:
                    v = 1-((cr['HIGH']-cr['OPEN'])/(cr['HIGH']-cr['LOW']))
                else:
                    v = 1                    
                h = h + "OPENLV,"
                l = l + str("%.4f" % round(v,2)) + ","

                if cr['HIGH'] > cr['LOW']:
                    v = 1-((cr['HIGH']-cr[priceCol])/(cr['HIGH']-cr['LOW']))
                else:
                    v = 1                    
                h = h + "CLOSELV,"
                l = l + str("%.4f" % round(v,2)) + ","

                for i in range(0, len(lvp)):
                    highs = ls_highs[i]
                    lows = ls_lows[i]

                    v1 = 1-((highs[r]-cr[priceCol])/(highs[r]-lows[r]))
                    v2 = 1-((highs[r-1]-lr[priceCol])/(highs[r-1]-lows[r-1]))
                    v = calcChg(v1,v2)
                    h = h + "LV" + str(lvp[i]) + ","
                    l = l + str("%.4f" % round(v1,2)) + ","
                    h = h + "LV" + str(lvp[i]) + "CHG,"
                    l = l + str("%.4f" % round(v,4)) + ","

                    #DAY HIGH
                    v = highs[r]
                    h = h + "HIGH" + str(lvp[i]) + ","
                    l = l + str("%.4f" % round(v,2)) + ","

                    v = (highs[r] / highs[r-1]) 
                    h = h + "HIGH" + str(lvp[i]) + "CHG,"
                    l = l + str("%.4f" % round(v,2)) + ","

                    #PIVOT HIGH
                    if r == offset or highs[r] <> highs[r-1]:
                        rh[i] = highs[r-1]
                    
                    v = rh[i]                        
                    h = h + "PIHIGH" + str(lvp[i]) + ","
                    l = l + str("%.4f" % round(v,2)) + ","

                    v = calcChg(highs[r],rh[i])
                    h = h + "PIHIGH" + str(lvp[i]) + "CHG,"
                    l = l + str("%.4f" % round(v,4)) + ","                    

                    #DAY LOW
                    v = lows[r]
                    h = h + "LOW" + str(lvp[i]) + ","
                    l = l + str("%.4f" % round(v,2)) + ","

                    v = calcChg(lows[r],lows[r-1])
                    h = h + "LOW" + str(lvp[i]) + "CHG,"
                    l = l + str("%.4f" % round(v,4)) + ","

                    #PIVOT LOW
                    if r == offset or lows[r] <> lows[r-1]:
                        rl[i] = lows[r-1]
                            
                    v = rl[i]                        
                    h = h + "PILOW" + str(lvp[i]) + ","
                    l = l + str("%.4f" % round(v,2)) + ","

                    v = calcChg(lows[r], rl[i]) 
                    h = h + "PILOW" + str(lvp[i]) + "CHG,"
                    l = l + str("%.4f" % round(v,4)) + ","

                    #VOLATILITY
                    #12 SEP 2018
                    v =  highs[r] / lows[r]
                    fn = "V" + str(lvp[i]) + "D"
                    h = h + fn + ","
                    fd = str(lvp[i]) + ' days volatility, higher value means higher volatility'
                    ls_fd.append([fn,fd])
                    l = l + str("%.4f" % round(v,4)) + ","

                    #VOLATILITY CHG
                    v1 = highs[r] / lows[r]
                    v2 = highs[r-1] / lows[r-1]         
                    v = calcChg(v1,v2)
                    fn = "V" + str(lvp[i]) + "DCHG"                    
                    h = h + fn + ","
                    fd = 'Change of ' + str(lvp[i]) + ' days volatility, 1 means no change, lower value means higher change'
                    ls_fd.append([fn,fd])                  
                    l = l + str("%.4f" % round(v,4)) + ","                       

                for i in range(0, len(sp)):
                    v1 = sma[i][r - smaos[i]]
                    v2 = sma[i][r - smaos[i]-1]

                    v = calcChg(v1,v2)
                    h = h + "SMA" + str(sp[i]) + ","
                    l = l + str("%.4f" % round(v1,4)) + ","
                    h = h + "SMA" + str(sp[i]) + "CHG,"
                    l = l + str("%.4f" % round(v,4)) + ","

                    v1 = v1 / cr[priceCol]
                    v2 = v2 / lr[priceCol]
                    v = calcChg(v1,v2)
                    h = h + "CLOSESMA" + str(sp[i]) + "CHG,"
                    l = l + str("%.4f" % round(v,4)) + ","

                for i2 in range(0, len(rsiCols)):
                    rsios = ls_rsios[i2]
                    rsi = ls_rsi[i2]                      
                    for i in range(0, len(rp)):
                        v1 = rsi[i][r - rsios[i]]
                        v2 = rsi[i][r - rsios[i]-1]
                        v = calcChg(v1,v2)
                        hprefix = rsiCols[i2][0]
                        if rsiCols[i2] == 'CLOSE':
                            hprefix = ""
                        h = h + hprefix + "RSI" + str(rp[i]) + ","
                        l = l + str("%.4f" % round(v1,4)) + ","
                        h = h + hprefix + "RSI" + str(rp[i]) + "CHG,"
                        l = l + str("%.4f" % round(v,4)) + ","
            
                    #GET OVERBOUGHT / OVERSOLD PRICE
                    #REMARKED FOR PERFORMANCE ISSUE, TIME CONSUMING
                    #20 SECS FOR EACH SYMBOL
                    #31 JAN 2018
                    #closes = list(df_data.iloc[r - rp[i]-1:r-1]['Close'].values)

                    #ret1, ret2 = reversersi(closes,rp[i])

                    #ob = ret2[0]
                    #os = ret2[1]

                    #h = h + "RSI" + str(rp[i]) + "-OBPRICE,"
                    #l = l + str("%.4f" % round(ob,4)) + ","                    
            
                    #h = h + "RSI" + str(rp[i]) + "-OSPRICE,"
                    #l = l + str("%.4f" % round(os,4)) + ","                    
                    
                for i in range(0, len(macddays)):
                    v = macd[i][r - macdos[i]]
                    mh = "MACD" + str(macddays[i]) + ","
                    mh = mh.replace(",","+")
                    h = h + mh + ","
                    l = l + str("%.4f" % round(v,4)) + ","

                v1 = bb[r - 20]
                v2 = bb[r - 21]
                v = calcChg(v1,v2)
                h = h + "B-BAND20,"
                l = l + str("%.4f" % round(v1,4)) + ","
                h = h + "B-BAND20CHG,"
                l = l + str("%.4f" % round(v,4)) + ","

                v1 = roc[r - 20]
                v2 = roc[r - 21]
                v = calcChg(v1,v2)
                h = h + "ROC20,"
                l = l + str("%.4f" % round(v1,4)) + ","
                h = h + "ROC20CHG,"
                l = l + str("%.4f" % round(v,4)) + ","

                try:
                    v1 = float(cr['LOW']) / float(cr['HIGH'])
                    v2 = float(lr['LOW']) / float(lr['HIGH'])
                    v = calcChg(v1,v2)#              
                except:
                    v = 0
                    
                h = h + "HIGHLOWCHG,"
                l = l + str("%.4f" % round(v,4)) + ","

                h = h + "LTREND,"
                l = l + str(tc) + ","

                tr = df_data.iloc[r - abs(tc) -1]
                v = calcChg(lr[priceCol], tr[priceCol])
                h = h + "LTRENDCHG,"
                l = l + str("%.4f" % round(v,4)) + ","

                if lr[priceCol] > cr[priceCol]:
                    t = -1
                else:
                    t = 1
            
                if t <> lt:
                    tc = 0
                
                tc = tc + 1 * t
                lt = t

                h = h + "TREND,"
                l = l + str(tc) + ","
                
                tr = df_data.iloc[r - abs(tc)]
                v = calcChg(cr[priceCol], tr[priceCol])
                h = h + "TRENDCHG,"
                l = l + str("%.4f" % round(v,4)) + ","
                
                #SEASONAL ANALYSIS
                #h = h + "Month,"
                #l = l + str(dt_date.month) + ","

                #h = h + "Year,"
                #l = l + str(dt_date.year) + ","
                
                s = ""
                        
                h = h + "ACTION"
                l = l + str(s)

                if r - offset == 0:
                    printout(h)

                printout(l)
                
                data.append(l.split(','))

        data.insert(0,h.split(','))

        for fd in ls_fd:
            globalfd.add(fd)
                
        closeFile()

        r = len(data)
        c = len(data[0])

        for x in range(1, r):
                for y in range(c):
                        try:
                            data[x][y] = float(data[x][y])
                        except:
                            data[x][y] = data[x][y]
                #for y in range(-7, -1):
                #        data[x][y] = float(data[x][y])
        return data

        #:
         #   print "Error - " + s


def validateData(ls_symbols):

    column_names = ['SYMBOL','CLOSE','DATE','TIME','CHANGE','OPEN','HIGH','LOW','VOL','VOLCHG']

    for s in ls_symbols:

        try:

            fnn = fn.filenameFormatter(s)
        
            filepath = hdir + fnn + ".csv"
            filepath2 = qdir + fnn + ".csv"
            
            #df_data = pandas.read_csv(filepath)
            df_data = globaldf.read(filepath)
            df_data2 = pandas.read_csv(filepath2,names = column_names)
            df_data2 = changedftouppercase(df_data2)

            dt_date = dt.datetime.strptime(df_data.iloc[0]['DATE'], '%Y-%m-%d').date()        
            dt_date2 = dt.datetime.strptime(df_data2.iloc[0]['DATE'], '%m/%d/%Y').date()

            maxDate = dt_date

            if dt_date2 > maxDate:
                maxDate = dt_date2

            #if dt_end.date() > maxDate:
            #    ls_symbols = [x for x in ls_symbols if x != s]
            #    print s + " REMOVED - INSUFFICIENT DATA"

        except:
            ls_symbols = [x for x in ls_symbols if x != s]
            print s + " REMOVED - NO DATA FILE"


    return ls_symbols


def reversersi(ls_val, period):

        vals = ls_val

        tval = vals[-1]
        price = tval
        
        spread = tval / 1000
        if tval < 0.01:
                spread = 0.01

        if spread > 20:
                spread = 20

        while True:
                tvals = copy.copy(vals)
                tval = tval + spread
                tvals.append(tval)
                a = array(tvals)
                rvals = ti.rsi(a,period)
                if len(rvals) > 1:
                    if rvals[-2] > 70:
                            obp = price
                            break
                
                if rvals[-1] > 70:
                        obp = tval
                        break
                
        while True:
                tvals = copy.copy(vals)
                tval = tval - spread
                tvals.append(tval)
                a = array(tvals)
                rvals = ti.rsi(a,period)
                if len(rvals) > 1:
                    if rvals[-2] < 30:
                            osp = price
                            break
                
                if rvals[-1] < 30:
                        osp = tval
                        break
        ret1 = "OVERBOUGHT,OVERSOLD,OBCHG%,OSCHG%".split()
        ret2 = [round(obp,4), round(osp,4), round(obp/price,2), round(osp/price,2)]        
        
        return ret1, ret2

def getdfdata(ls_data):
    headers = ls_data[0]
    df_data = pandas.DataFrame.from_records(ls_data[1:], columns=headers)
    df_data['DATE'] =  pandas.to_datetime(df_data['DATE']).apply(lambda x: x.date())
    return df_data


def changedftouppercase(df):
    llabels = df.columns.values.tolist()
    ulabels = map(str.upper,llabels)
    df.columns = [ulabels]
    return df



    


    

