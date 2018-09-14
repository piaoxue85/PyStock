import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import math
import copy

import csv

import globaldf

from collections import OrderedDict

print "Pandas Version", pd.__version__

def dprint(text):
    print text
    return

def readDate(value):
        try:
                rtn = dt.datetime.strptime(value, '%m/%d/%Y').date()
        except:
                rtn = ""
        return rtn

def findDateIndex(ldt_timestamps, d):
    i = 0
    while ldt_timestamps[i].date() < d.date():
        i = i + 1  
    return i

def getTradeDates(market,df_index):

    ldt_timestamps = df_index.index
    timestamps = []
    timestampsIdx = 0
    dt_today = dt.datetime.now()
    for i in range(timestampsIdx, len(ldt_timestamps)):
        if math.isnan(df_index[market][i]) == False or ldt_timestamps[i].date() >= dt_today.date():
            timestamps.append(ldt_timestamps[i])

    return timestamps

def getRawData(ldt_timestamps, ls_symbols, field):

    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    df_rets = d_data[field].copy()
    
    return d_data, df_rets
        
def getData(ldt_timestamps, ls_symbols, field):

    d_data, df_rets = getRawData(ldt_timestamps, ls_symbols, field)
    
    # Filling the data.
    df_rets = df_rets.fillna(method='ffill')
    df_rets = df_rets.fillna(method='bfill')
    df_rets = df_rets.fillna(1.0)

    return d_data, df_rets

def GenTimestamps(dt_start, dt_end, dt_timeofday):
    
    timestamps = []
    
    total_days = (dt_end - dt_start).days + 1 #inclusive

    for day_number in range(total_days):
        current_date = (dt_start + dt.timedelta(days = day_number)).date()
        if int(current_date.strftime("%w")) > 0 and int(current_date.strftime("%w")) < 6:
            quoteDate = dt.datetime(current_date.year, current_date.month, current_date.day, dt_timeofday)
            timestamps.append(quoteDate)

    return timestamps

def writecsv(rows, filename):

    with open(filename, 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerows(rows)

    #reader = csv.reader(open(filename,'rU'),delimiter=',')
    #for row in reader:
    #    print row

def PlotGraph(ldt_timestamps, df_values, filename):

    # Plotting the plot of daily returns

    dprint(filename)
    na_values = df_values.values

    #To be completed
    #na_normalized_values= na_values / na_values[0,:]
    na_normalized_values= na_values 

    dprint(na_values)

    plt.clf()    
    plt.plot(ldt_timestamps, na_normalized_values)  # Value
    plt.axhline(y=0, color='r')
    plt.legend(['Value'])
    plt.ylabel('Value')
    plt.xlabel('Date')
    plt.savefig(filename, format='pdf')

    return


def readsymbols(df_googleData, m):

    #directory = "data\\google\\"
    #filepath = directory + "gdata.csv"
    #df_googleData = pd.read_csv(filepath)

    r = df_googleData

    if m <> '':
        r = df_googleData[(df_googleData.MARKET == m)]
    
    l = len(r.index)

    ls_symbols = []
    
    for i in range(0, l):
        #ls_symbols.append(r.iloc[i]['SYMBOL'])
	ls_symbols.append(filenameFormatter(r.iloc[i]['SYMBOL']))

    return ls_symbols

def appendunique(l1,l2):
    for i in l1:
        try:
            l2.remove(i)
        except:
            pass
    l = l1 + l2    

    return l

def uniquelist(list1):
  
    list2 = list(set(list1))    
    list2.sort(key=list1.index)

    return list2
        
    

def symbolFormatter(s):
    sym = s
    sym = sym.replace("HKG:", "")    
    if s.isdigit():
		s = str(s).zfill(4)
		sym = s + ".HK"
		
    return sym

def filenameFormatter(sym):

    r = sym

    try:
        r = r.replace(".HK", "")
        r = r.replace("HKG:", "")
        
        if sym.isdigit():
            r = str(sym).zfill(4)
           
        r = r.replace(":", "-")

    except:
        print "error formatting filename for " + str(sym)
        r = sym

    return str(r)


def leadingspace(text,length):

    space = ''
    
    for i in range(len(text),length):
        space = space + ' '

    return space + text


def formatpct(val):
    val = float(val) * 100;
    val = round(val,2)
    return str(val) + "%"

def trend(df_val, idx, col):

    val3 = df_val[idx-2][col]
    val2 = df_val[idx-1][col]
    val1 = df_val[idx][col]

    val = 0

    #PI.DOWN
    if max(val1, val2, val3) == val2:
        val = 1
    #PI.UP
    elif min(val1, val2, val3) == val2:
        val = 2
    #UP
    elif min(val1, val2, val3) == val3 and max(val1, val2, val3) == val1:
        val = 3
    #DOWN
    elif min(val1, val2, val3) == val1 and max(val1, val2, val3) == val3:
        val = 4
    #NO CHANGE
    if val1 == val2:
        val = 5

    return val


#Read multiple files with same data structure into one dataframe
#19 Feb 2018
def read_as_df(files):

        #df1 = pd.read_csv(files[0])
        df1 = globaldf.read(files[0])
        
        for i in range(1,len(files)):
                #df2 = pd.read_csv(files[i])
                df2 = globaldf.read(files[i])
                df1 = pd.concat([df1,df2])

        return df1

#Read config file in csv format
#11 Aug 2018
def readconfigfile(filepath):

    #df_data = pd.read_csv(filepath)
    df_data = globaldf.read(filepath)

    return df_data    



def formatsymbols(ls_symbols):

    ls2 = []

    for s in ls_symbols:
        ls2.append(str(s).zfill(4))

    return ls2


def onhandsymbols(df_trans):

        ls1 = df_trans.SYMBOL.unique()
        ls2 = []
        
        for s in ls1:
                ucost, qty, amt, accmulamt,btrans, strans = readTrans(df_trans, s)
                if qty > 0:
					ls2.append(filenameFormatter(s))
					
	return ls2

    
def findpara(para, p):
        return para.find(p)


def format_df_trans(df_trans):

        r = df_trans

        l = len(r)

        for i in range(0, l):

                shares = r.iloc[i]['SHARES']
                amount = r.iloc[i]['CASHONHAND']

                try:
                    shares = float(shares.replace(",", ""))                    
                except:
                    shares = 0

                try:
                    amount = float(amount.replace(",",""))
                except:
                    amount = 0

                r.iloc[i]['SHARES'] = shares
                r.iloc[i]['CASHONHAND'] = amount

        return r

def readTrans(df_trans, sym):
        avgprice = 0
        qty = 0
        amt = 0
        accmulamt = 0
        lastTrade = ""

        bTrans = ""
        sTrans = ""
		
	#removing leading zero in symbol
        sym2 = sym		
        try:
            sym2 = str(int(sym))
        except:
            sym2 = sym

        try:
            r = df_trans[(df_trans.SYMBOL == sym) | (df_trans.SYMBOL == sym2)]
            l = len(r)
        except:
            l = 0  			
            
        for i in range(0, l):

                shares = r.iloc[i]['SHARES']
                amount = r.iloc[i]['CASHONHAND']
                lastTrade = r.iloc[i]['DATE']
                
                try:
                    shares = float(shares.replace(",", ""))                    
                except:
                    shares = 0

                try:
                    amount = -float(amount.replace(",",""))
                except:
                    amount = 0

                qty = qty + shares    
                amt = amt + amount
                accmulamt  = accmulamt + amount

                #last buy transaction
                if shares > 0:
                        bTrans = r.iloc[i]

                #last sell transaction
                if shares < 0:
                        sTrans = r.iloc[i]


                if qty == 0:
                    amt = 0
                        
        if qty > 0:
                avgprice = amt / qty

                
        return avgprice, qty, amt, accmulamt, bTrans, sTrans

def dfconcat(df1, df2):

        if len(df1) == 0:
                if len(df2) > 0:
                    df1 = df2
        else:
                if len(df2) > 0:
                    df1 = pd.concat([df1,df2])
                
        return df1

#9 SEP 2018
#CONVERT ALL COLUMNS TO SPECIFY DATATYPE
def dfastype(df1, astype='float'):

    headers = df1.columns.values.tolist()

    for header in headers:
        try:
            df1[header] = df1[header].astype(astype)
        except:
            continue

    return df1

def updateStatus(fnn, status):
        file = open(fnn,"w")
        file.write(status)
        file.close()
        return 

def readStatus(fnn):
        try:
                file = open(fnn,"r")
                status = file.read()
                file.close()
        except:
                status = ""
                
        return status
