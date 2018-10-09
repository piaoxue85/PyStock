from lib import download as dl
import csv
from lib import sharedfunctions as fn
from lib import main as main
import datetime as dt
import os.path
import pandas as pd
import numpy
import sys
from lib import globaldf


ldt_timestamps = []
df_confile = []

def run(url):

    directory = "data\\dayquote\\google\\"
    filepath = directory + "gquote.csv"
    print "Downloading quotes"

    df_data = dl.quotefromgoogle(url)

    df_data['SOURCE'] = 'GOOG-Q'

    #ERROR QUOTE
    df_data1 = df_data.iloc[(df_data['OPEN'] == "#N/A") | (df_data['OPEN'] == "Loading...")]

    #NORMAL QUOTE
    df_data = df_data.iloc[(df_data['OPEN'] <> "#N/A") & (df_data['OPEN'] <> "Loading...")]

    c = len(df_data)
    directory = "data\\dayquote\\"

    for i in range(0,c):
        
        fn1 = df_data.iloc[i]["SYMBOL2"]
        fn1 = fn.filenameFormatter(str(fn1))
        filepath = directory + fn1 + ".csv"
        s = df_data.iloc[i]["SYMBOL2"]
        
        print "Updating " + s
        items = []
        items.append(s)
        
        for j in range(2,11):
            items.append(df_data.iloc[i][j])

        thefile = open(filepath, 'w')

        myString = ','.join(map(str, items))
        thefile.write(myString)
        thefile.close()

    print "All quotes updated"

    return

##Bypassed rountine, to be revised
##Too many errors in data
##25 Sep 2018
def appendintraday(s):

    directory = "data\dayquote\\"
    directory1 = directory
    directory2 = directory + "intraday\\" #Stored
        
    try:

        fn1 = fn.filenameFormatter(s)
        
        filepath1 = directory1 + fn1 + ".csv"
        filepath2 = directory2 + fn1 + ".csv"
        append = False
        lastVol = 0
        
        reader1 = csv.reader(open(filepath1,'rU'),delimiter=',')

        for row in reader1:
            row1 = row

        if os.path.exists(filepath2):
            rowCount = 0
            reader2 = csv.reader(open(filepath2,'r'),delimiter=',')

            for row in reader2:
                row2 = row
                try:
                    lastVol = float(row2[8])
                    rowCount = rowCount + 1
                except:
                    rowCount= 0

            if rowCount > 0:

                if row1[2] <> row2[2]:
                    append = 1
                    lastVol = 0

                if row1[2] == row2[2] and row1[3] <> row2[3]:
                    append = 1
                    lastVol = float(row2[8])
                
        else:
            append = True

        if append == True:
            f = open(filepath1, 'r')
            newVolume = float(row1[8])
            if newVolume > 0:
                target = open(filepath2, 'a')
                increment = newVolume - lastVol
                proportion = increment / newVolume
                line = f.read() + ","+ str(increment)
                line = line.replace('\n', '')
                target.write(line + '\n')
            else:
                print "Error - Zero volume"
                
            f.close()

    except:
        
        print s + " - append intraday error"

def download(market):
    url = readconfigfile(market)
    run(url)

#Read url by market from config file
#11 Aug 2018
def readconfigfile(market):

    df_result = df_confile[df_confile.MARKET==market]    
    return df_result['URL'].iloc[0]
            
if __name__ == '__main__':

    argv = sys.argv
    df_confile = globaldf.read('getpricequote.cfg')
    markets = ['HSI','NYSE','ASX','CUSTOM']
    
    para = ""
    if len(argv)>1:
        para = ",".join(argv)
        print "[" + para + "]"
        download(argv[1])            
    else:
        for market in markets:
            download(market)
       


