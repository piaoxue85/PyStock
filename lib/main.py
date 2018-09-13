
import csv
import random
import math
import operator

import os
import sys, getopt

import itertools

import knndata
import knn
import sharedfunctions as fn
import download as dl

from timeit import default_timer as timer
import datetime as dt

import pandas as pd
import numpy as np

import copy

import time

import rule1 as r1
import rule2 as r2
import rule3 as r3
import rule4 as r4
import rule5 as r5
import rule6 as r6
import rule7 as r7
import rule8 as r8
import rule9 as r9
import rule10 as r10
import rule11 as r11
import rule12 as r12
import rule13 as r13
import rule14 as r14
import rule15 as r15
import rule16 as r16


import analyzer as an

global dt_end
global dt_start
global ls_symbols

global overhead #Broker, stampduty, trading overheads
global argv
global para

import glob

overhead = 0.0031
ls_rules = [1,2,3,4,5,6,6.1,7,8,8.1,8.2,8.3,8.4,9,10,11, 12, 13, 14.93070,14.143070,14.253070,16]

def prepareRefDf(market):

        ret = []

        directory = "data\\google\\"
        filepath = directory + "gdata.csv"
        df_googleData = pd.read_csv(filepath)
        ret.append(df_googleData)

        directory = "data\\google\\"
        filepath = directory + "transactions.csv"
        df_trans = pd.read_csv(filepath)
        ret.append(df_trans)

        directory = "analysis\\rsi9\\output\\"
        filepath = directory + "seasonalrsi.csv"
        df_rsi_an = pd.read_csv(filepath)
        ret.append(df_rsi_an)

        c = "results\\prediction\\*" + market + "*-1.csv"
        files = glob.glob(c)
        df_predict = fn.read_as_df(files)
        ret.append(df_predict)

        return ret

#dfs: dataframes 
def run(s, dfs):

        global dt_today

        dt_today = dt.datetime.now().date()

        global ls_symbols
        global df_close

        global dt_end
        global dt_start

        #dt_end = dt.datetime.now() - dt.timedelta(hours=24)
        dt_timeofday = dt.timedelta(hours=16)
        dt_today = dt.datetime.now().date()
        dt_end = dt.datetime(dt_today.year, dt_today.month, dt_today.day)
        dt_date = dt.datetime.now() - dt.timedelta(hours=24)
                
        global df_googleData
        global df_trans
        global df_rsi_an
        global df_predict
        
        df_googleData = dfs[0]
        df_trans = dfs[1]
        #df_rsi_an = dfs[2]
        #df_predict = dfs[3]
        
        info = GetGoogleData(df_googleData,s)

        n = ''
        t = ''
##        nrd = ''
##        rd = ''
        eps = ''
##        mkt = ''

        if len(info.index) == 1:
                n = str(info.iloc[0]['NAME'])
                eps = info.iloc[0]['EPS']
      
##        pheaders = []
##        pheaders = df_predict.columns.values.tolist()
##        lenph = len(pheaders)

        ls_file = []
        ls_file_headers = []
        ls_analysis = []
        ls_pricelevel = []
        ls_fbtext = []
        ls_line = []

        fn.dprint("Analysing " + s + "...")		

        #Select data for analysis, limit date range for reduce processing time, 
        beginDate = dt_end - dt.timedelta(days=960)
        
        beginDate = beginDate.date()
        endDate = dt_end.date()
        
        ls_data = knndata.getData(s, beginDate, endDate,False, False)
        headers = ls_data[0]

        df_data = knndata.getdfdata(ls_data)

        pe = 0

        try:
                eps = float(eps)
                pe = ls_data[-1][headers.index("CLOSE")] / eps
        except:
                eps = 'N/A'
                pe = 'N/A'
		
        ucost, qty, amt, accmulamt, btrans, strans = fn.readTrans(df_trans, s)

##        stoploss = 0
##        minsell = 0
##
##        try:
##
##                if qty > 0:
##                        stoploss = ucost - eps
##                        minsell = ucost * 1.0031
##                else:
##                        stoploss = ls_data[-1][headers.index("CLOSE")] - eps
##                        minsell = ls_data[-1][headers.index("CLOSE")] * 1.0031
##        except:
##                stoploss = 0
##                minsell = 0
        
        val = qty * ls_data[-1][headers.index("CLOSE")]
        pl = val - amt
        plpct = 0
        if amt > 0:
                plpct = fn.formatpct(pl / amt)

        plchg = (ls_data[-1][headers.index("CLOSE")] - ls_data[-2][headers.index("CLOSE")]) * qty
        
        ls_line = copy.copy(ls_data[-1])

        ls_line.insert(1, str("%.2f" %ucost))
##        ls_line.insert(2, str("%.2f" %stoploss))
##        ls_line.insert(3, str("%.2f" %minsell))

        #obp, osp = reversersi(s)
##        df_p =  predict(s)
##        plow = 0
##        phigh = 0
##        oprice = 0
##
##        if len(df_p) > 0:
##                plow = df_p.iloc[0]['PLOW']
##                phigh = df_p.iloc[0]['PHIGH']
##                oprice = (plow + phigh) / 2

        #ls_line.insert(4, str("%.2f" %obp))     #OVERBOUGHT PRICE
##        ls_line.insert(4, str("%.2f" %phigh))      #PREDICTION HIGH  
        #ls_line.insert(6, str("%.2f" %osp))     #OVERSOLD PRICE
##        ls_line.insert(5, str("%.2f" %plow))     #PREDICTION LOW
##        ls_line.insert(6, str("%.2f" %oprice))     #ORDER PRICE
        
        ls_line.insert(2, qty)
        ls_line.insert(3, amt)
        ls_line.insert(4, val)
        ls_line.insert(5, plchg)
        ls_line.insert(6, pl)
        ls_line.insert(7, plpct)
        ls_line.insert(8, accmulamt)

        lbprice = 0 #LAST BUY PRICE
        lsprice = 0 #LAST SELL PRICE
        lbpricepct = 0 #CLOSE PRICE / LAST BUY PRICE
        lspricepct = 0 #CLOSE PRICE / LAST SELL PRICE

        close = ls_data[-1][headers.index("CLOSE")]
        
        if len(btrans) > 0:
                lbprice = str(btrans['PRICE']).replace(",","")
                lbpricepct = float(lbprice) / close

        if len(strans) > 0:
                lsprice = str(strans['PRICE']).replace(",","")
                lspricepct = float(lsprice) / close

        ls_line.insert(9, lbprice)
        ls_line.insert(10, str("%.4f" % round(lbpricepct,4)))        
        ls_line.insert(11, lsprice)
        ls_line.insert(12, str("%.4f" % round(lspricepct,4)))
        

##        ls_line.insert(0, mkt)
						
        ls_line.insert(0, fn.symbolFormatter(s))
##        ls_line.insert(1, n)
##        ls_line.insert(2, t)
      
        ls_line.insert(-1, eps)
        ls_line.insert(-1, pe)
        #ls_line.insert(-1, result[-1])
##        ls_line.insert(-1, nrd)
##        ls_line.insert(-1, rd)

        #RSI SWING, 20 JUL 2017
        os, ob = rsiswing(df_data)

        v1 = 0
        v2 = 0

        osd = ""
        obd = ""

        if len(os) > 0:
                v1 = os.iloc[-1]['LOW']
                osd = os.iloc[-1][0]                

        if len(ob) > 0:
                v2 = ob.iloc[-1]['HIGH']
                obd = ob.iloc[-1][0]                

        if len(os) > 0 and len(ob) > 0:
                #osd = dt.datetime.strptime(os.iloc[-1][0], '%Y-%m-%d').date()
                #obd = dt.datetime.strptime(ob.iloc[-1][0], '%Y-%m-%d').date()

                #osd = os.iloc[-1][0]
                #obd = ob.iloc[-1][0]
                
                delta = obd - osd
                rsidelta = delta.days
                
                v = 1-((v2-ls_data[-1][headers.index("CLOSE")])/(v2-v1))
        else:
                rsidelta = 0
                v = 1

        ls_line.insert(-1,v2)
        ls_line.insert(-1,str(obd))

        ls_line.insert(-1,v1)
        ls_line.insert(-1,str(osd))
        
        ls_line.insert(-1,str(rsidelta))
        #Price level
        ls_line.insert(-1,str("%.4f" % round(v,2)))

##        lenph = len(pheaders)
##        len_dfp = len(df_p)
##        for x in range(1, lenph):
##                val = 0
##                if len_dfp > 0:
##                        val = df_p.iloc[0][x]
##                                
##                ls_line.insert(-1,str(val))
                
        rowText = ""

        rowText = rowText + fn.symbolFormatter(s) + " " + n + " "
        rowText = rowText + str(ls_data[-1][headers.index("CLOSE")])
        cp = fn.formatpct(ls_data[-1][headers.index("CLOSECHG")] - 1)
        rowText = rowText + " (" + str(cp) + ") "
        rowText = rowText + str(ls_data[-1][headers.index("DATE")])

        rowText = rowText + "\n\n"

        try:
                intervals = [10,20,50,200,abs(rsidelta)]
                ppa = PricePositionAnalysis(s,ls_data,intervals)
                ls_pricelevel.append(ppa)
        except:
                fn.dprint("ERROR PRICE POSITION: " + s)

        for r in ls_rules:                    
                try:
                        action, comment = applyrule(r,ls_data, info, -1)
                        if action <> 'BUY' and action <> 'SELL' and action <> 'HOLD':
                                ls_line.insert(-1,"---")
                        else:
                                ls_line.insert(-1,action)
                except:
                        ls_line.insert(-1,"ERR")
                        action = ""
                        comment = ""

                if len(action) > 0 or len(comment) > 0:
                        rowText = rowText + coltext(str(r))
                        rowText = rowText + coltext(action)
                        rowText = rowText + coltext(comment)
                        rowText = rowText + "\n\n"                

        ls_file.append(ls_line)

        emptyCols = coltext("") + coltext("")
                
        rowText = rowText + emptyCols + "LAST "

        #LAST HIGH
        LHigh = ls_data[-2][headers.index("HIGH")]
        rowText = rowText +  "HIGH " + str("%.2f" %LHigh)

        #LAST LOW
        LLow = ls_data[-2][headers.index("LOW")]
        rowText = rowText + " LOW " + str("%.2f" %LLow)

        rowText = rowText + "\n\n"

        rowText = rowText + emptyCols + "52 WEEKS"

        #52 WEEKS (252 DAYS) HIGH D1015
        High52 = ls_data[-2][headers.index("HIGH252")]
        rowText = rowText+ " HIGH " + str("%.2f" %High52)

        #52 WEEKS (252 DAYS) LOW D1015
        Low52 = ls_data[-2][headers.index("LOW252")]
        rowText = rowText + " LOW " + str("%.2f" %Low52)

        #52 WEEKS PRICE LEVEL
        try:
                PriceLv = ls_data[-2][headers.index("LV252")]
                PriceLv = str("%.0f" % int(PriceLv * 100)) + '%'
        except:
                PriceLv = 0        

        #52 WEEKS PRICE LEVEL
        rowText = rowText + " LV " + str(PriceLv) 

        rowText = rowText + "\n\n"

        rowText = rowText + emptyCols        

        try:
                rowText = rowText  + "PE " + str("%.2f" %pe) + "\n\n"
        except:
                rowText = rowText  + "PE " + str(pe) + "\n\n"

        #if result[-1] <> 'N/A':
        #        rowText = rowText + "KNN PREDICTION: " + result[-1] + " (" + fn.formatpct(result[-2]) + ")"
        #        rowText = rowText + result[3] + "\n\n"

        rowText = rowText.replace("\n\n", "\n" + coltext(fn.symbolFormatter(s)))
        rowText = rowText[:-len(coltext(fn.symbolFormatter(s)))]
        
        ls_analysis.append(rowText)

        ls_file_headers = copy.copy(headers)

        ls_file_headers.insert(1,'AVGCOST')
##        ls_file_headers.insert(2,'STOP LOSS')
##        ls_file_headers.insert(3,'MIN SELL')

        #ls_file_headers.insert(4,'OVERBOUGHT')
##        ls_file_headers.insert(4,'PHIGH')
        #ls_file_headers.insert(6,'OVERSOLD')
##        ls_file_headers.insert(5,'PLOW')
##        ls_file_headers.insert(6,'ORDER PRICE')        
        
        ls_file_headers.insert(2,'ONHAND')
        ls_file_headers.insert(3,'INVESTED')
        ls_file_headers.insert(4,'CURRENT')
        ls_file_headers.insert(5,'PLCHG')
        ls_file_headers.insert(6,'PL')
        ls_file_headers.insert(7,'PL%')
        ls_file_headers.insert(8,'TOTAL INVESTED')

        ls_file_headers.insert(9,'LBUY')
        ls_file_headers.insert(10,'LBUYPCT')
        ls_file_headers.insert(11,'LSELL')        
        ls_file_headers.insert(12,'LSELLPCT')

##        ls_file_headers.insert(0,'MARKET')
        ls_file_headers.insert(0,'SYMBOL')
##        ls_file_headers.insert(1,'NAME')
##        ls_file_headers.insert(2,'TAG')

        ls_file_headers.insert(-1,'EPS')
        ls_file_headers.insert(-1,'PE')
##        ls_file_headers.insert(-1,'PREDICTION')
##        ls_file_headers.insert(-1,'RESULTDATE')
##        ls_file_headers.insert(-1,'RECORDDATE')
     
        ls_file_headers.insert(-1,'RSI9HIGH')
        ls_file_headers.insert(-1,'RSI9HIGHDATE')        

        ls_file_headers.insert(-1,'RSI9LOW')
        ls_file_headers.insert(-1,'RSI9LOWDATE')   

        ls_file_headers.insert(-1,'RSI9HIGH-LOW')
        ls_file_headers.insert(-1,'RSI9SWINGLV')

##        for x in range(1, lenph):
##                ls_file_headers.insert(-1,pheaders[x]) 

        #SIGNAL RULES
        for r in ls_rules:
                ls_file_headers.insert(-1,'R' + str(r))
        
        ls_file.insert(0,ls_file_headers)

        odir = "results\\listdata\\"
        fnn = fn.filenameFormatter(s)
        ofile = odir + fnn + '.csv'

        openFile(ofile)
        for r in ls_file:
                list = ""
                for c in r:
                        list = list + coltext(c)
                printout (list)
        closeFile()

        odir = "results\\comment\\"
        ofile = odir + fnn + '.csv'
        openFile(ofile)
        printout('SYMBOL,RULE,ACTION,COMMENT')
        for r in ls_analysis:
                printout(r)
        closeFile()

        odir = "results\\pricelevel\\"
        ofile = odir + fnn + '.csv'
        openFile(ofile)
        for r in ls_pricelevel:
                printout(r)
        closeFile()
                
        return ls_file, ls_analysis, ls_pricelevel

def leadingspace(text,length):

    #space = ''
    
    #for i in range(len(text),length):
    #    space = space + ' '

    #strReturn = space + text

        strReturn = text + ','

        return strReturn

def findpara(p):
        return para.find(p) + 1

def coltext(text, width=7):

        strReturn = str(text) + ','

        return strReturn

def PricePositionAnalysis(symbol, ls_data, intervals):

        rowText = coltext("SYMBOL")
        #HEADER
        for j in range(0, len(intervals)):
                rowText = rowText + coltext("") + coltext(intervals[j])  + coltext("")

        rowText = rowText + "\n"
        rowText = rowText + PricePositionLine(symbol,ls_data, intervals)

        return rowText

     
def PricePositionLine(symbol, ls_data, intervals):
     
    spreads = 10

    headers = ls_data[0]

    spread=  [None] * len(intervals)
    high =  [None] * len(intervals)
    low =  [None] * len(intervals)
    ls_price =  [None] * len(intervals)
    ls_dist =  [None] * len(intervals)
    ls_count =  [None] * len(intervals)
    position = [None] * len(intervals)

    for i in range(0, len(intervals)):
        spread[i], high[i], low[i], ls_price[i], ls_count[i], ls_dist[i], position[i] = an.pricedist(ls_data, spreads , intervals[i])

    rowText = ""
    for i in range(0, spreads):
        rowText = rowText + coltext(fn.symbolFormatter(symbol))
        for j in range(0, len(intervals)):
            if position[j] == i:
                rowText = rowText + coltext(">")
            else:
                rowText = rowText + coltext("")
            rowText = rowText + coltext(str("%.2f" % round(ls_price[j][i],2)))
            rowText = rowText + coltext(str("%.2f" % round(ls_dist[j][i],2)))
        rowText = rowText + "\n"

    return rowText


def applyrule(rule,data, info, ln):

    headers = data[0]
    action = ''
    comment = ''
        
    if rule==1:
        action, comment = r1.apply(data, ln)
    elif rule==2:
        r, ob, os = rsi_stat(fn.symbolFormatter(info.iloc[0]['SYMBOL']), dt_end.month)
        action, comment = r2.apply(data, ln, 9 ,r, ob, os)
    elif rule==3:
        action, comment = r3.apply(data, ln)
    elif rule==4:
        action, comment = r4.apply(data, ln)
    elif rule==5:
        action, comment = r5.apply(data, ln)
    elif rule==6:
        action, comment = r6.apply(data, 5, 10, ln)
    elif rule==6.1:
        action, comment = r6.apply(data, 50, 200, ln)
    elif rule==7:
        action, comment = r7.apply(data, ln)
    elif rule==8:
        action, comment = r8.apply(data, 5, ln)
    elif rule==8.1:
        action, comment = r8.apply(data, 10, ln)
    elif rule==8.2:
        action, comment = r8.apply(data,  20, ln)
    elif rule==8.3:
        action, comment = r8.apply(data, 50, ln)
    elif rule==8.4:
        action, comment = r8.apply(data,  200, ln)
    elif rule==9:
        action, comment = r9.apply(data, ln)
    elif rule==10:
        action, comment = r10.apply(data, ln)
    elif rule==11:
        action, comment = r11.apply(data, ln)
    elif rule==12:
        dt_date = dt.datetime.strptime(data[ln][0], '%Y-%m-%d').date()
        action, comment = r12.apply(info,dt_date)
    elif rule==13:
        action, comment = r13.apply(data, info)
    elif rule==14.93070:
        action, comment = r14.apply(data, ln,9,30,70)
    elif rule==14.92080:
        action, comment = r14.apply(data, ln,9,20,80)
    elif rule==14.143070:
        action, comment = r14.apply(data, ln,14,30,70)
    elif rule==14.142080:
        action, comment = r14.apply(data, ln,14,20,80)
    elif rule==14.253070:
        action, comment = r14.apply(data, ln,25,30,70)
    elif rule==16:
        action, comment = r16.apply(data, ln)       
    return action, comment

def rsi_stat(s,mth):
    s = fn.symbolFormatter(s)
    r = df_rsi_an[(df_rsi_an.SYMBOL == s) & (df_rsi_an.MONTH==mth)]
    b=0;
    s=0;
    if len(r.index) == 1:
        b = r.iloc[0]['OVERBOUGHT']
        s = r.iloc[0]['OVERSOLD']
        if math.isnan(b):
            b = 0
        if math.isnan(s):
            s = 0
        if b > 0 and s > 0:
            b = b/s
            s = 1
    return r, b, s

        
def rsiswing(df_data):

        os = df_data[(df_data.RSI9 < 30) & (df_data.RSI9CHG < 1)]
        ob = df_data[(df_data.RSI9 > 70) & (df_data.RSI9CHG > 1)]

        return os, ob

def reversersi(sym):

    sym = fn.symbolFormatter(sym)
    r = df_reversersi[(df_reversersi.SYMBOL == sym)]
    b=0;
    s=0;
    if len(r.index) == 1:
        b = r.iloc[0]['OVERBOUGHT']
        s = r.iloc[0]['OVERSOLD']
        if math.isnan(b):
            b = 0
        if math.isnan(s):
            s = 0
    return b, s

def predict(sym):

        sym = fn.symbolFormatter(sym)
        r = df_predict[(df_predict.SYMBOL == sym)]
        pl=0;
        ph=0;

        l = len(r.index)
        if l == 1:
                pl = r.iloc[0]['PLOW']
                ph = r.iloc[0]['PHIGH']
                if math.isnan(pl):
                    pl = 0
                if math.isnan(ph):
                    ph = 0
        elif l> 1:
                print "Multiple prediction found"
        elif 1 ==0:
                print "No prediction found"
        return r

def GetStockInfo(s):
    r = df_stock_info[(df_stock_info.SYMBOL == s)]
    n = ""
    t = ""
    if len(r.index) == 1:
        n = str(r.iloc[0]['NAME'])
        t = str(r.iloc[0]['TAG'])
    return r, n, t

def GetGoogleData(df_googleData, s):
    r = df_googleData[(df_googleData.SYMBOL == s) | (df_googleData.SYMBOL2 == s)]
    return r

def openFile(filepath):

        global text_file1

        try:
            text_file1 = open(filepath, "w")
        except:
            print "Error in opening " + filepath
            
        return

def printout(str):

        str = str + '\n'

        try:
                text_file1.write(str)
        except:
                print str

        return

def closeFile():

    try:
        text_file1.close()
    except:
        print "Error in closing file"
 
    return

