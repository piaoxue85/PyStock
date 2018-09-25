from lib import download as dl
import csv
from lib import sharedfunctions as fn
from lib import knndata
import datetime as dt
import pandas
import numpy as np
import pandas as pd
import math
import os

import multiprocessing
import time
import sys

import random

ldt_timestamps = []
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

    dt_date = dt.datetime.now().date()
    
    idx = []

    idx.insert(0,fheader)

    completed = []

    urls = []

    df_urls = fn.readconfigfile('gethistorical.cfg')

    urls = df_urls.values.tolist()  #to be passed to download 

    global ls_symbols

    #dl.googleData()

    dl.historicalindex()
    
    directory = "data\\google\\"
    #filepath = directory + "gdata.csv"
    #df_googleData = pd.read_csv(filepath)

    # =len(df_googleData)

    #on hand stock
    #directory = "data\\google\\"
    #filepath = directory + "transactions.csv"
    #df_trans = pd.read_csv(filepath)
    #ls_symbols = fn.onhandsymbols(df_trans)
    #print ls_symbols

    filepath = directory + "symbolurl.csv"
    df_idxdata = pandas.read_csv(filepath, dtype={'SYMBOL': object})
    df_idxdata['DATE'] =  pandas.to_datetime(df_idxdata['DATE']).apply(lambda x: x.date())  

    #Download index
    directory = "data\\google\\"
    filepath = directory + "historical-data-index.csv"
    df_hindex = pd.read_csv(filepath)

    c = len(df_idxdata)

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

    directory1 = "data\\historical\\raw\\"
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
##              ##To write raw data downloaded, 26 AUG 2018
##                filepath1 = directory1 + filename2 + '.csv'
##                df_data1.to_csv(filepath1, index=False)                
                
                if headers == list(df_data1.columns.values):
                    df_data2 = knndata.formatGoogleData(df_data1)
                    filepath2 = directory2 + filename2 + ".csv"                 
                    df_data2.to_csv(filepath2, index=False)
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
    


