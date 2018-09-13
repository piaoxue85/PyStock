
import os
import sys, getopt

import itertools

from lib import sharedfunctions as fn
from lib import main as mn
from lib import consolidate as consol
from lib import knn as knn
from lib import knndata as knndata

from timeit import default_timer as timer
import datetime as dt

import pandas as pd
import numpy as np

import copy

import time

global ls_symbols
global argv
global ofilename

para  = ''

testSize = 252 #60
forecastSize = 10 #10

#KNN forecast
#Moved to WEKA
#All symbols for backtest and forecast
def run():
        
        for s in ls_symbols:

                df_rawdata = knndata.getRawData(s,False)
                dataset = knndata.prepareData(df_rawdata,s)
                keys = knn.getKeys(dataset)

                columns = [0,2,3,4,2,3,4]

                c = len(dataset)

                #1 exclude header row

                actualData = knn.selectRows(dataset,c-testSize,c,columns)
                
                keyNames = dataset[0]

                #Rolling forecast
                beginDate = dt.datetime.strptime(dataset[-testSize][0], '%Y-%m-%d').date()

                endDate = dt.datetime.strptime(dataset[-1][0], '%Y-%m-%d').date()
                endDate = endDate + dt.timedelta(days=forecastSize)

                dates = []

                for d in range(-testSize,0):
                        dates.append(dt.datetime.strptime(dataset[d][0], '%Y-%m-%d').date())

                for d in range(1,forecastSize+1):
                        idate = dates[-1]
                        idate = idate + dt.timedelta(days=1)
                        dates.append(idate)

                df_forecastData = df_rawdata[(df_rawdata['Date'] < str(beginDate))]
                forecastDataset = knndata.prepareData(df_forecastData,s)

                keys = [[7,8,9,10,13,14,18,19,21,22,24,25,27,28,30,31,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52]]

                for k in keys:
                        k.append(-1)
                        #fn.dprint(k)

                        #Backtest + Forecast
                        Closes = backtest(dataset, k, "CLOSE")
                        Highs = backtest(dataset, k, "HIGH")
                        Lows = backtest(dataset, k, "LOW")

                        forecastResult2 = forecast(df_rawdata, dataset, s, k, dates[-forecastSize:])

                        size = len(Closes)
                        backtestResult = []
                        forecastResult = []

                        for i in range(0,size):
                                backtestResult.append([dates[i], Highs[i],Lows[i],Closes[i]])

                        backtestResult = backtestResult + forecastResult2
                                
                        forecastResult = forecast(df_forecastData, forecastDataset, s, k, dates)

                        formatted = formatResult(dates, actualData,backtestResult,forecastResult)

                        dfile = "data\\knn\\result-" + s + "-" + keyNames[k[0]] + ".csv"
                        fn.writecsv(formatted, dfile)
             
        return


def formatResult(dates, actualData, backtestResult, forecastResult):

        #A - ACTUAL
        #T - TEST
        #F - FORECAST
        fheaders = ['Date','A-High','A-Low','A-Close','T-High','T-Low','T-Close','F-High','F-Low','F-Close','T-High-Ref','T-Low-Ref','T-Close-Ref']
        hl = len(fheaders)
        
        result = []
        result.append(fheaders)

        l = len(dates)
        for i in range(0, l):
                row = []
                for j in range(0,hl):
                        row.append(0)
                row[0] = dates[i]
                result.append(row)

        l = len(actualData)
        for i in range(0,l):
                for j in range(1,4):
                        result[i+1][j] = actualData[i][j]

        l = len(backtestResult)

        for i in range(0,l):
                for j in range(1,4):
                        try:
                                result[i+1][j+3] = backtestResult[i][j][0]
                        except:
                                result[i+1][j+3] = backtestResult[i][j]
                        result[i+1][j+9] = backtestResult[i][j]
                        

        l = len(forecastResult)
        for i in range(0,l):
                result[i+1][7] = forecastResult[i][1]
                result[i+1][8] = forecastResult[i][2]
                result[i+1][9] = forecastResult[i][3]

        return result        


#dataset knndata.getData
#columnName = Result Column Name CLOSE, HIGH, LOW
#def test(dataset, keys, columnName):

#df_rawdata knndata.getRawData(s)

def backtest(dataSet, key, columnName, size = testSize):

        headers = dataSet[0]
        i = headers.index(columnName + 'CHG')
        j = headers.index(columnName)

        #12 FEB 2017
        #Set date as result in training set for referencing training set from result                
        for x in range(1, len(dataSet)-1):
                dataSet[x][-1] = dataSet[x+1][i]
                dt_date = dt.datetime.strptime(dataSet[x][0], '%Y-%m-%d').date() 
                dataSet[x][-1] =  str(dataSet[x+1][i]) + "," + dt_date.strftime("%Y-%m-%d")
                        
        r = len(dataSet) #size of trainingSize + testSize
        r = r - 1 #Exclude columns header
        #r = r - 1 #Exclude last day quote

        trainingSize = r - size

        headerSet = knn.selectRows(dataSet,0,1,key)
        trainingSet = knn.selectRows(dataSet,1,trainingSize,key)
        testSet = knn.selectRows(dataSet,trainingSize, r ,key)
        #Value
        dataSet2 = knn.selectRows(dataSet,trainingSize,r,[0,j])

        
        resultSet = knn.analyse(trainingSet, testSet)
        resultSet2 = []
        
        for x in range(0,size):
                try:
                        result = resultSet[x].split(",")
                        value = float(result[0]) * dataSet2[x][1]
                        result.append(value)
                except:
                        fn.dprint("Error:" + str(resultSet[x]))
                        result = resultSet[x]
                resultSet2.append(result)
                
        return resultSet2


def rolling(dataSet, key, columnName):

        r = len(dataSet) #size of trainingSize
        r = r - 1 #Exclude columns header
        headers = dataSet[0]

        trainingSize = r -1

        i = headers.index(columnName + 'CHG')
        j = headers.index(columnName)
        
        for x in range(1, r):
                dataSet[x][-1] = dataSet[x+1][i]   

        #fn.dprint(dataSet[-2])
        #fn.dprint(dataSet[-1])

        #datSet,1, Exclude heaeder columns
        trainingSet = knn.selectRows(dataSet,1,trainingSize,key)
        testSet = knn.selectRows(dataSet,trainingSize, r ,key)
        dataSet2 = knn.selectRows(dataSet,trainingSize,r,[0,j])

        
        resultSet = knn.analyse(trainingSet, testSet)
        resultSet2 = []
        
        #for x in range(0,size):
        resultSet2.append(dataSet2[-1][1]*resultSet[-1])

        #fn.dprint(resultSet2[-1])

        return resultSet2


def forecast(df_forecastData, forecastDataset, symbol, key, dates):

        results = []
        
        for d in dates:
                        sdate = str(d.month) + '/' + str(d.day) + '/' +  str(d.year)

                        fn.dprint("Forecast " + sdate)
                
                        #GET RESULT CLOSE, HIGH, LOW
                        Closes = rolling(forecastDataset, key, "CLOSE")
                        Highs = rolling(forecastDataset, key, "HIGH")
                        Lows = rolling(forecastDataset, key, "LOW")

                        Open = df_forecastData.iloc[-1]['Close']
                        High = Highs[0]
                        Low = Lows[0]
                        Close = Closes[0]
                        Volume = df_forecastData.iloc[-1]['Volume']

                        results.append([d,High, Low, Close])

                        #APPEND RESULT TO RAWDATA
                        df_data2 = knndata.formatQuote(sdate,Open,High,Low,Close,Volume,Close)
                        df_forecastData = knndata.appendQuote(df_forecastData,df_data2)
                        #PREPARE DATA (RSI, SMA....)
                        forecastDataset = knndata.prepareData(df_forecastData,symbol)

                        #fn.dprint(df_data2.iloc[-1])
                        #fn.dprint(forecastDataset[0])
                        #fn.dprint(forecastDataset[-1])


        return results


def main():
        main_datajoin()
        return

def main_datajoin():


        s = '0002'

        file1 = "data\\knndata\\" + s + ".csv"
        file2 = "data\\knndata\\HSI.csv"
        file3 = "data\\knndata\\DJI.csv"
        file4 = "data\\knndata\\VIX.csv"
        df1 = pd.read_csv(file1)

        e = ['DATE','OPEN','HIGH','LOW','CLOSE','VOLUME','ADJ CLOSE','HIGH52','LOW52','SMA5','SMA10','SMA20','SMA50','SMA100','SMA200']

        del df1['ACTION']
        #df3 = datajoin(df1,file2, 'HSI')
        df3 = df1
        df3['ACTION'] = ""
        tfile = "data\\knn\\" + s + "HSI-Data.csv"
        df3.to_csv(tfile, index=False)
        fields = list(df3.columns.values)


        for f in fields:
                #['RSI','ROC','SMA','B-BAND','MACD','TREND','VOLUME','CHG']
                for i in ['SMA5','SMA20','SMA50','SMA100','RSI14','RSI25']:
                        if f.find(i) > -1:
                                e.append(f)

        
        key = knndata.getFieldIndexExclude(fields,e)
        dfile = "data\\knn\\"  + s + "HSI-Result.csv"
        run_file(tfile, key, dfile)

        print "PROGRAM ENDED"

        return

def main_join2():
        
        del df3['ACTION']
        df3 = datajoin(df3,file3, 'DJI')
        df3['ACTION'] = ""
        tfile = "data\\knn\\"  + s + "HSIDJI-Data.csv"
        df3.to_csv(tfile, index=False)
        fields = list(df3.columns.values)
        key = knndata.getFieldIndexExclude(fields,e)
        dfile = "data\\knn\\"  + s + "HSIDJI-Result.csv"
        run_file(tfile, key, dfile)

        del df3['ACTION']
        df3 = datajoin(df3,file4, 'VIX')
        df3['ACTION'] = ""
        tfile = "data\\knn\\"  + s + "HSIDJIVIX-Data.csv"    
        df3.to_csv(tfile, index=False)
        fields = list(df3.columns.values)
        key = knndata.getFieldIndexExclude(fields,e)
        dfile = "data\\knn\\"  + s + "HSIDJIVIX-Result.csv"
        run_file(tfile, key, dfile)

        key = [7,8,9,10,13,14,18,19,21,22,24,25,27,28,30,31,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52]
        tfile = "data\\knndata\\"  + s + ".csv"        
        dfile = "data\\knn\\"  + s + "-Result.csv"
        run_file(tfile, key, dfile)

        fn.dprint("completed")

        return

def main_file():

        tfile = "data\\knndata\\0002HSI.csv"        
        key = [7,8,9,10,13,14,18,19,21,22,24,25,27,28,30,31,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91]
        dfile = "data\\knn\\0002HSI.csv"
        run_file(tfile, key, dfile)


        key = [7,8,9,10,13,14,18,19,21,22,24,25,27,28,30,31,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52]
        tfile = "data\\knndata\\0002.csv"        
        dfile = "data\\knn\\0002.csv"
        run_file(tfile, key, dfile)

        fn.dprint("Completed")

def run_file(tfile, key, dfile):
#run with datafile provided of backtest only
       
        df_data = pd.read_csv(tfile)
        
        #columns = [0,2,3,4,2,3,4]      #Absolute value
        columns = [0,7,8,9,7,8,9]     #Change value, normalised

        rc = len(df_data.index)

        dataset = []

        dataset.append(list(df_data.columns.values))

        for r in range(0, rc):
                dataset.append(df_data.iloc[r].values.tolist())               

        c = len(dataset)
        #1 exclude header row
        actualData = knn.selectRows(dataset,c-testSize,c,columns)

        keyNames = dataset[0]

        dates = []

        for d in range(-testSize,0):
                dates.append(dt.datetime.strptime(dataset[d][0], '%Y-%m-%d').date())

        Closes = backtest(dataset, key, "CLOSE")
        Highs = backtest(dataset, key, "HIGH")
        Lows = backtest(dataset, key, "LOW")

        size = len(Closes)
        backtestResult = []
        forecastResult = []

        for i in range(0,size):
                backtestResult.append([dates[i], Highs[i],Lows[i],Closes[i]])

        formatted = formatResult(dates, actualData,backtestResult,forecastResult)
        fn.writecsv(formatted, dfile)
        
        return
        

def _main():

        global ls_symbols
        global dt_today
        global para

        global ofilename

        dt_today = dt.datetime.now().date()

        argv = sys.argv
        if len(argv)>1:
                para = ",".join(argv)

        market = 'HSI'

        directory = "data\\google\\"
        filepath = directory + "gdata.csv"
        global df_googleData
        df_googleData = pd.read_csv(filepath)

        ls_symbols = fn.readsymbols(df_googleData,market)

        ls_symbols = ['HSI']

        #fn.dprint("KNN ANALYSER - TEST RUN")
        #knn.testrun()

        run()

        fn.dprint("PROGRAM ENDED")


def datajoin(df1, f, suffix):

        df2 = pd.read_csv(f)

        #eliminate absolute values
        e = ['OPEN','HIGH','LOW','CLOSE','VOLUME','ADJ CLOSE','HIGH52','LOW52','SMA5','SMA10','SMA20','SMA50','SMA100','SMA200']

        for n in e:
                del df2[n]

        df3 = pd.merge(df1, df2,on=['DATE'], how='left',suffixes=('', suffix))

        return df3
        

main()
