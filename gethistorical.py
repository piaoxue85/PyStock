from lib import download as dl
from lib import sharedfunctions as fn
from lib import knndata
from lib import globaldf

import datetime as dt
import pandas
import numpy as np
import pandas as pd
import os
import csv

import multiprocessing
import time
import sys

global idx
global dt_date
global df_idxdata

global market
global fheader

fheader = "SYMBOL,URL,DATE,MARKET"

def run():

    urls = []
    global idx
    global dt_date
    global fheader
    global df_idxdata
    global market
    global ls_symbols

    dt_date = dt.datetime.now().date()
    
    idx = []

    idx.insert(0,fheader)

    completed = []

    urls = []

    df_urls = fn.readconfigfile('gethistorical.cfg')

    urls = df_urls.values.tolist()  #to be passed to download 

    dl.historicalindex()
    
    directory = "data\\google\\"

    filepath = directory + "symbolurl.csv"
    df_idxdata = pandas.read_csv(filepath, dtype={'SYMBOL': object})
    df_idxdata['DATE'] =  pandas.to_datetime(df_idxdata['DATE']).apply(lambda x: x.date())  

    #Download index
    directory = "data\\google\\"
    filepath = directory + "historical-data-index.csv"
    #df_hindex = pd.read_csv(filepath)
    df_hindex = globaldf.read(filepath)

    ls_hindex = df_hindex.SYMBOL.unique()
    market = df_hindex.MARKET.unique()[0]

    print "Market: " + market

    c = len(ls_hindex) + 5

    pool = multiprocessing.Pool(processes=5)
    print str(len(urls[0:c])) + " symbols"

    #Multithreading
    #False - Debug and test
    #True - Production
    mtflag = True

    if mtflag == True:
        output = pool.map(download,urls[0:c])
    else:
        for i in range(0,c):
            download(urls[i])

    print "Completed"

def download(parms):

    directory2 = "data\\historical\\"

    dt_date = dt.datetime.now().date()

    fname = parms[0]
    url = parms[1]
    
    flag = True

    if flag == True:

        symbol = ""
        ret = 0

        try:
            df_data1 = dl.downloadfromgoogle(url)
            headers = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Symbol']

            line = symbol + "," + url + ","
            
            if len(df_data1) > 0:
                symbol = df_data1.iloc[0]["Symbol"]
                filename2 = fn.filenameFormatter(symbol)            
                
                if headers == list(df_data1.columns.values):
                    df_data2 = knndata.formatGoogleData(df_data1)
                    #Read raw data file without reading price quote
                    df_data0 = knndata.getRawData(symbol,False)
                    df_result = knndata.mergeRawData(df_data0, df_data2)                    
                    filepath2 = directory2 + filename2 + ".csv"                    
                    df_result.to_csv(filepath2, index=False)
                    ret = len(df_data2)
                    print symbol + ", " + fname + " - Completed"
                else:                    
                    print symbol + ", " + fname + " - No price data"
            else:
                line = symbol + "," + fname + "," + str(dt_date)
                print "No symbol"

        except Exception as e :
            print fname + "- Error - " + str(e)

    return symbol, ret


def writeidxfile(filepath):

    global fheader
    
    idxfile = open(filepath, "w")
    c = len(idx)
    idxfile.write(fheader + "\n")
    for i in range(0,c-1):
        idxfile.write(idx[i] + "\n")
    idxfile.close()
            
    return

            
if __name__ == '__main__':
    run()
    


