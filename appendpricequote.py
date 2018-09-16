import csv
from lib import sharedfunctions as fn
from lib import knndata
from lib import globaldf
import datetime as dt
import os.path
import pandas as pd
import numpy
import sys


def appendhistorical(s):

    directory = "data\historical\\"
    directory1 = directory
        
    fn1 = fn.filenameFormatter(s)
    filepath1 = directory1 + fn1 + ".csv"

    df_data = knndata.getRawData(s)
    df_data['DATE'] =  pd.to_datetime(df_data['DATE']).apply(lambda x: x.date())
    df_data.to_csv(filepath1, index=False)

    return df_data

def main(market):

    print "Appending quote to historical"

    directory = "data\\google\\"
    filepath = directory + "gdata.csv"
    df_googleData = globaldf.read(filepath)
    
    ls_symbols = fn.readsymbols(df_googleData,market)

    for s in ls_symbols:
        print s
        try:
            appendhistorical(s)
        except SystemExit as e:
            print "SystemExit " + str(e)
        except Exception as e:
            print "exception " + str(e)
            
if __name__ == '__main__':

    argv = sys.argv
    para = ""
    if len(argv)>1:
        para = ",".join(argv)
        main(argv[1])
        print "[" + para + "]"
    else:
        main('HSI')
        main('ASX')
        main('NYSE')




