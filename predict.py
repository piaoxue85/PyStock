
import os
import sys, getopt

import itertools

from lib import sharedfunctions as fn
from lib import formatter

from timeit import default_timer as timer
from subprocess import check_output
from shutil import copyfile

from lib import knn as knn
from lib import knndata as knndata

import datetime as dt

import pandas as pd
import numpy as np

import copy

import time
import csv

import os

global ls_symbols3
global argv

global results
global para

global outputfile
global flag1
global forecastDays
global forecastDay

forecastDays = [1] #[1,5,10,20]
results = []
ls_symbols3 = [] #Processed symbols
para  = ''


def addSymbols(filepath, ls_symbols):

        try:
                df1 = pd.read_csv(filepath)
                ls_symbols2 = df1.loc[(df1['RSI9'] > 0)]['SYMBOL'].tolist()

                for s in ls_symbols:
                        try:
                                ls_symbols2.remove(s)
                        except:
                                pass
                ls_symbols = ls_symbols + ls_symbols2

        except:
                print "Error - " + filepath
                
        return ls_symbols

def selectOnhandSymbols(market):

        ls_symbols = []

        directory = "results\\"
        ofilename = "onhand"
        filepath = directory + ofilename + ".csv"
        df1 = pd.read_csv(filepath)
        df1 = df1[(df1['MARKET']==market)]
   
        ls_symbols = df1['SYMBOL'].tolist()

        return ls_symbols

def selectSymbols(market):

        ls_symbols = []
        directory = "results\\"        
        #ret = []        

        #For symbol traded in the past
        #ls_symbols2 = df_trans.SYMBOL.unique()
        #ls_symbols2 = fn.formatsymbols(ls_symbols2)
        #ls_symbols = fn.appendunique(ls_symbols,ls_symbols2)


        filepath = directory + "Buy-" + market + ".csv"        
        ls_symbols = addSymbols(filepath,ls_symbols)

        #in shortlist
        #filepath = directory + "shortlisted.csv"
        #ls_symbols = addSymbols(filepath,market,ls_symbols)

        ls_symbols = fn.uniquelist(ls_symbols)


        return ls_symbols
        

def writeSummary(odir, fnn):
        
        ofile = odir + fnn + ".csv"
        ofile2 = odir + fnn + ".txt"
        
        try:
            text_file1 = open(ofile, "w")
            outputfile = ofile
        except:
            print "Error in opening " + ofile
            text_file1 = open(ofile2, "w")
            outputfile = ofile2
        #text_file2 = open(ofile2, "w")
        for r in results:
                line = ''
                for c in r:
                        line = line + str(c) + ','
                line = line + '\n'
                text_file1.write(line)
                #text_file2.write(line)
        text_file1.close()
        #text_file2.close()
        
        return outputfile

def runWeka(s, hresult,lresult):

        #filepath1 = "weka\\runVIX.bat"
        print s + " running Weka "
        odir = "weka\\"
        ofile = odir + 'run.bat '

        fnn = fn.filenameFormatter(s)
        try:
                cmd = ofile + fnn + " " + str(lresult) + " " + str(hresult)
                
                cmd = "start /min " + cmd
                #os.system(cmd)
                print check_output(cmd, shell=True).decode()
        except:
                'Error running ' + cmd

        return

def _deleteResultFiles(s):
        print "deleteResultFiles remaked"

def deleteResultFiles(s):

        print s + " deleting result files "
        odir = "weka\\"
        ofile = odir + 'deleteResult.bat '

        fnn = fn.filenameFormatter(s)
        try:
                cmd = ofile + fnn
                cmd = "start /min " + cmd
                #os.system(cmd)
                print check_output(cmd, shell=True).decode()
        except:
                print 'Error deleting result files ' + cmd

        return

def readResult(fnn,sym,dataset):

        global results 
        global flag1

                
        filepath2 = "weka\\results\\"+ fnn + "-HIGH-RESULT.csv"
        with open(filepath2) as f2:
                highs = f2.read().splitlines()

        filepath3 = "weka\\results\\"+ fnn + "-LOW-RESULT.csv"
        with open(filepath3) as f3:
                lows = f3.read().splitlines()

        dataset[0].append('HIGH_PREDICT')
        dataset[0].append('LOW_PREDICT')
        dataset[0].append('HIGH_ACTUAL')
        dataset[0].append('LOW_ACTUAL')
        headers = dataset[0]

        columnName = "CLOSE"
        h = headers.index(columnName)

        columnName = "HIGH"
        i = headers.index(columnName)                  
        columnName = "LOW"
        j = headers.index(columnName)

        columnName = "HIGH_PREDICT"
        k = headers.index(columnName)                  
        columnName = "LOW_PREDICT"
        l = headers.index(columnName)

        c = len(dataset)
        os = 4 #SKIPPING HEADER LINES

        high = str(highs[c -2 + os]).split(',')
        low = str(lows[c -2 + os]).split(',')

        lcount = 0
        hcount = 0
        fcount = 0
        hlcount = 0

        #Classifier UP/DOWN
        lcount2 = 0
        hcount2 = 0
        fcount2 = 0
        hlcount2 = 0

        hvars = []
        lvars = []

        hvars2 = []
        lvars2 = []

        for x in range(1, c):
                high = str(highs[x + os]).split(',')
                low = str(lows[x + os]).split(',')

                try:
                        phighf = float(high[2])
                        plowf = float(low[2])
                        
                        ahighf = float(high[1])
                        alowf = float(low[1])

                        vhighf = ahighf / phighf
                        vlowf = alowf / plowf

                        hvar = phighf /ahighf
                        lvar = plowf/alowf

                        hlcount = 0
                        hlcount2 = 0
        
                        if vhighf >= 0.995 and vhighf <= 1:
                                hvars.append(hvar)
                                hcount = hcount + 1
                                hlcount = hlcount + 1
        
                        if vlowf <= 1.005 and vlowf >= 1:
                                lvars.append(lvar)
                                lcount = lcount + 1
                                hlcount = hlcount + 1

                        if (ahighf >= 1 and phighf >= 1) or (ahighf <= 1 and phighf <= 1):
                                hvars2.append(hvar)
                                hcount2 = hcount2 + 1
                                hlcount2 = hlcount2 + 1
                                
                        
                        if (alowf >= 1 and plowf >= 1) or (alowf <= 1 and plowf <= 1):
                                lvars2.append(lvar)
                                lcount2 = lcount2 + 1
                                hlcount2 = hlcount2 + 1
                        
                        if hlcount > 1:
                                fcount = fcount + 1

                        if hlcount2 > 1:
                                fcount2 = fcount2 + 1

                except:
                        ahighf = high[1]
                        alowf = low[1]

                dataset[x].append(phighf)
                dataset[x].append(plowf)
                dataset[x].append (ahighf)
                dataset[x].append (alowf)

        hadj = 1 - np.var(hvars)
        ladj = 1 - np.var(lvars)

        hadj2 = 1 - np.var(hvars2)
        ladj2 = 1 - np.var(lvars2)
        
        
        tot = float(c)
        hpct = round(hcount/tot,4)
        lpct = round(lcount/tot,4)
        fpct = round(fcount/tot,4)

        hpct2 = round(hcount2/tot,4)
        lpct2 = round(lcount2/tot,4)
        fpct2 = round(fcount2/tot,4)        

        dfile = "results\\prediction\\" + fnn + ".csv"
        if flag1 == True:
                fn.writecsv(dataset, dfile)

        lclose = dataset[-1][h]
        lhigh = dataset[-1][i]
        llow = dataset[-1][j]
        hchg = dataset[-1][k]
        lchg = dataset[-1][l]

        phigh = float(lhigh) * (float(hchg) * hadj)  
        plow = float(llow) * (float(lchg) * ladj)

        phigh2 = float(lhigh) * (float(hchg) * hadj2)
        plow2 = float(llow) * (float(lchg) * ladj2)        
        
        hresult = str(lhigh) + " > " + str(phigh)
        lresult = str(low) + " > " + str(plow)

        closeplow = (float(lclose) - float(plow)) / float(plow)
        phighplow = (float(phigh) - float(plow)) / float(plow)

        result = [sym,dataset[-1][0],str(forecastDay), closeplow, phighplow, lclose,lhigh,phigh,phigh2,hchg,llow,plow,plow2,lchg,hpct,lpct,hadj,ladj,fpct,hpct2,lpct2,hadj2,ladj2,fpct2,fnn]

        c = len(result)
        for x in range(2,c-1):
                result[x] = float(result[x])
                result[x] = str("%.4f" %result[x])

        results.append(result)

def main(addsymbols,ls_symbols,ofnn):

        print "Stock price prediction " + market

        if len(ls_symbols) == 0:
                return

        global ls_symbols3
        global forecastDay

        global results
        headers = ['SYMBOL','DATE','FORECAST', 'CLOSE-PLOW','PHIGH-PLOW','CLOSE','HIGH','PHIGH','PHIGH2','PHIGHCHG','LOW','PLOW','PLOW2','PLOWCHG','HPCT','LPCT','HADJ','LADJ','FPCT','HPCT2','LPCT2','HADJ2','LADJ2','FPCT2','INDEX']

        dirt = "data\\knndata\\"
        dirt2 = "data\\weka\\"
        odir = "results\\prediction\\"
        sdir = "results\\"
        file1 = ''
        addsymbols2 = []        #for valid symbols in addsymbols

        for asym in addsymbols:
                try:
                        #For market opens before HKEX does in the same day
                        openindex = ['INDEXNIKKEI-NI225','INDEXASX:XJO']
                        if asym in openindex:
                                #Read Opening only
                                df_rawdata2 = knndata.getRawData(asym,True)
                                df_rawdata2 = df_rawdata2[(df_rawdata2['Open'] > 0)]
                                df_rawdata2 = readOpening(df_rawdata2)
                        else:
                                df_rawdata2 = knndata.getRawData(asym,False)                       
                        dataset2 = knndata.prepareData(df_rawdata2,asym)
                        addsymbols2.append(asym)
                except:
                         print "Failed in preparing " + asym       

        #removing processed symbols, i.e. onhand
        for s in ls_symbols3:
                try:
                        ls_symbols.remove(s)                       
                except:
                        fn.dprint(s + " is not in the list") 

        for fd in forecastDays:

                forecastDay = fd
                results = []
                if len(results) == 0:
                        results.append(headers)
                        
                for s in ls_symbols:
                        ls_symbols3.append(s)

                        df_rawdata = knndata.getRawData(s,False)
                        fs = fn.filenameFormatter(s)
                        dataset = knndata.prepareData(df_rawdata,fs)
                        df = pd.read_csv(dirt + fs + ".csv")
                        del df['ACTION']

                        allsymbols = fs

                        for asym in addsymbols2:
                                f = dirt + asym + ".csv"
                                df2 = pd.read_csv(f)
                                if df2.iloc[-1][0] >= df.iloc[-1][0]:
                                        allsymbols = allsymbols + "-" + asym
                                        print asym + " joined " + str(df2.iloc[-1][0])
                                        df = datajoin(df, df2, asym)
                                else:
                                        print asym + " skipped - data outdated - " + str(df2.iloc[-1][0])
                                
                        df['ACTION'] = ''

                        df3 = df

                        tfile = dirt2 + allsymbols + ".csv"
                        df3.to_csv(tfile, index=False)

                        rc = len(df3.index)

                        dataset = []
                        dataset.append(list(df3.columns.values))

                        for r in range(0, rc):
                                dataset.append(df3.iloc[r].values.tolist())               

                        fdataset, rdataset = prepareData(allsymbols, dataset)

                        dlen = len(fdataset[0])
                        
                        lresult = dlen 
                        hresult = dlen -1
                        runWeka(allsymbols, hresult, lresult)

                        readResult(allsymbols,s,rdataset)
                        deleteResultFiles(allsymbols)

                        if ofnn == '':
                                ofnn = 'test'
                                if len(addsymbols) > 0:
                                        ofnn = "-".join(addsymbols)

                        file1 = writeSummary(odir, "_" + ofnn + "-" + str(fd))

                file2 = odir + ofnn + "-" + str(fd) + ".csv"
                copyfile(file1,file2)
                os.remove(file1)

                file3 = odir + ofnn + "-" + str(fd) + ".htm"
                formatter.convertfile(file2,file3)

                print str(forecastDay) + " day(s) forecast completed"

        return


def datajoin(df1, df2, suffix):

        #eliminate absolute values
        e = absoluteValueFields()
        e.remove('DATE')
        for n in e:
                del df2[n]

        #weka cannot handle nan value
        #df3 = pd.merge(df1, df2,on=['DATE'], how='left',suffixes=('', suffix))
        df3 = pd.merge(df1, df2,on=['DATE'], how='inner',suffixes=('', suffix))

        return df3

def absoluteValueFields():
        ret = ['DATE','OPEN','HIGH','LOW','CLOSE','VOLUME','ADJ CLOSE','ACTION']
        d = [5,10,20,50,100,200,252]
        c = len(d)
        for i in range(1, c):
                ret.append('HIGH' + str(d[i]))
                ret.append('LOW' + str(d[i]))
                ret.append('PIHIGH' + str(d[i]))
                ret.append('PILOW' + str(d[i]))                

                
        d = [5,10,20,50,100,200]
        c = len(d)
        for i in range(1, c):
                ret.append('SMA' + str(d[i]))


        return ret

def prepareData(s, dataset):

        testSize = 100
        fnn = fn.filenameFormatter(s)

        dataset[0][-1] = "HIGH_RESULT"
        dataset[0].append('LOW_RESULT')
        headers = dataset[0]
                                     
        columnName = "LOW"
        i = headers.index(columnName + 'CHG')
        #j = headers.index(columnName)

        columnName = "HIGH"
        k = headers.index(columnName + 'CHG')
        #l = headers.index(columnName)

        c = len(dataset)
        for x in range(1, c):
                dataset[x].append('')

        dataset2 = []
        dataset2.append(dataset[0])

        #12 FEB 2017
        #Set date as result in training set for referencing training set from result                
        for x in range(1, c-forecastDay):
                #classifier = ''
                #if dataset[x+1][i] > 0:
                #        classifier = 'UP'
                #elif dataset[x+1][i] < 0:
                #        classifier = 'DOWN'
                #else:
                #        classifier = 'NOCHG'                        
##                dataset[x][-2] = dataset[x+1][k]        #HIGH_RESULT
##                dataset[x][-1] = dataset[x+1][i]        #LOW_RESULT

                hchg = 1
                lchg = 1
                for y  in range(x,x+forecastDay):
                        hchg = hchg * dataset[y+1][k]
                        lchg = lchg * dataset[y+1][i]
                
                #dataset[x][-2] = dataset[x+forecastDay][k]        #HIGH_RESULT
                #dataset[x][-1] = dataset[x+forecastDay][i]        #LOW_RESULT
                dataset[x][-2] = hchg       #HIGH_RESULT
                dataset[x][-1] = lchg      #LOW_RESULT

                dataset2.append(dataset[x])                

        dataset2.append(dataset[-1])
        dataset = dataset2

        dfile = "data\\weka\\" + fnn + "-DATASET.csv"        
        fn.writecsv(dataset, dfile)

        #e = ['OPEN','HIGH','LOW','CLOSE','VOLUME','ADJ CLOSE','HIGH52','LOW52','SMA5','SMA10','SMA20','SMA50','SMA100','SMA200']

        #for f in headers:
        #        #['RSI','ROC','SMA','B-BAND','MACD','TREND','VOLUME','CHG']
        #        for i in ['ROC','SMA','B-BAND','MACD','TREND','VOLUME']:
        #                if f.find(i) > -1:
        #                        e.append(f)
                                
        #e = ['DATE','OPEN','HIGH','LOW','CLOSE','VOLUME','ADJ CLOSE','HIGH52','LOW52','SMA5','SMA10','SMA20','SMA50','SMA100','SMA200']

        e = absoluteValueFields()
        columns = knndata.getFieldIndexExclude(headers,e)
        
        c = len(dataset)
        #COMPLETE SET
        fullData = knn.selectRows(dataset,0,c,columns)
        dfile = "data\\weka\\" + fnn + "-COMPLETE.csv"
        
        fn.writecsv(fullData, dfile)
        
        arffData = ARFFFormatter(fullData, s + '-COMPLETE')
        arffData[-1][-1] = '?'
        arffData[-1][-2] = '?'
        dfile = "data\\weka\\" + fnn + "-COMPLETE.arff"       
        fn.writecsv(arffData, dfile)

        #TRAINING DATA
        trainingData = knn.selectRows(dataset,0,c -testSize,columns)
        dfile = "data\\weka\\" + fnn + "-TRAINING.csv"       
        fn.writecsv(trainingData, dfile)
        
        arffData = ARFFFormatter(trainingData, fnn + '-TRAINING')
        dfile = "data\\weka\\" + fnn + "-TRAINING.arff"       
        fn.writecsv(arffData, dfile)

        #TEST DATA
        testData = knn.selectRows(dataset,c -testSize,c,columns)
        #INSERT HEADER
        testData.insert(0,trainingData[0])

        dfile = "data\\weka\\" + s + "-TEST.csv"       
        fn.writecsv(testData, dfile)

        arffData = ARFFFormatter(testData, fnn + '-TEST')
        arffData[-1][-1] = '?'
        arffData[-1][-2] = '?'
        dfile = "data\\weka\\" + fnn + "-TEST.arff"       
        fn.writecsv(arffData, dfile)

        fn.dprint(s + " data file ready - " + str(dataset[-1][0]))

        #return
        #1. fullData(Weka) with absolute value removed
        #2. dataset - raw data with absolute value
        return fullData, dataset

#3  May 2017, For Weka
def ARFFFormatter(dataset,datasetName):

        headers = dataset[0]
        output = []
        line = "@relation " + datasetName
        output.append(line.split(','))
        output.append('')
        
        for h in headers:
                line = "@attribute '" + h + "' numeric"
                output.append(line.split(','))
                
        output.append('')
        line = "@data"
        output.append(line.split(','))

        c = len(dataset)

        for x in range(1, c):
                output.append(dataset[x])                        

        return output


def readOpening(df_data):

        #Read day open only, set all value as open
        df_data['Close'] = df_data['Open']        
        df_data['High'] = df_data['Open']
        df_data['Low'] = df_data['Open']
        df_data['Adj Close'] = df_data['Open']

        #Date back for 1 day for data join
        #Stock value (HKEX) dated as at 1 Sep
        #Index value dated as at 4 Sep <- date back to 1 Sep
        df_data.Open = df_data.Open.shift(-1)
        df_data.Close = df_data.Close.shift(-1)
        df_data.High = df_data.High.shift(-1)
        df_data.Low = df_data.Low.shift(-1)
        df_data['Adj Close'] = df_data['Adj Close'].shift(-1)

        df_data = df_data[:-1]

        return df_data
        

if __name__ == '__main__':

    argv = sys.argv
    para = ""
    outputfile = ''
    flag1 = False #Write result file by symbol

    if len(argv)>1:
            
        para = ",".join(argv)
        addsymbols = []
        if argv[1] == 'HSI':
                addsymbols = ['INDEXHANGSENG-HSI']
                market = 'HSI'
        elif argv[1] == 'HKUS':
                market = 'HSI'
                addsymbols = ['VIX','INDEXHANGSENG-HSI','INDEXNASDAQ-.IXIC','INDEXDJX-.DJI','INDEXNIKKEI-NI225']
        elif argv[1] == 'ASX':
                market = 'ASX'
                addsymbols = ['VIX','INDEXNASDAQ-.IXIC','INDEXDJX-.DJI']
        elif argv[1] == 'NYSE':
                market = 'NYSE'
                addsymbols = ['VIX','INDEXHANGSENG-HSI','INDEXNASDAQ-.IXIC','INDEXDJX-.DJI']                

        ls_symbols = selectOnhandSymbols(market)
        main(addsymbols, ls_symbols, 'onhand-' + market)    

        ls_symbols = selectSymbols(market)
        main(addsymbols, ls_symbols, 'predict-' + market)

    else:
            
        flag1 = True #Write result file by symbol            
        market = 'HSI'
        addsymbols = ['INDEXHANGSENG-HSI']
       
        
