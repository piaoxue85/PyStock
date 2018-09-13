from lib import download as dl
import pandas as pd
from lib import sharedfunctions as fn
import datetime as dt
import os.path
import pandas as pd
import numpy

def main():

    print "Getting charts - aastock"

    directory = "data\\google\\"
    filepath = directory + "gdata.csv"
    global df_googleData
    df_googleData = pd.read_csv(filepath)
    market = 'HSI'

    ls_symbols = fn.readsymbols(df_googleData,market)

    for s in ls_symbols:
        try:
            url = "http://charts.aastocks.com/servlet/Charts?com=50004&stockid=" + s +".HK&period=0&lang=0&scheme=0&height=213&footerStyle=1&width=174"
            filepath= "data\charts\\" + s +".png"
            dl.downloadfromgoogle(url, filepath)
        except SystemExit as e:
            print "SystemExit " + str(e)
        except Exception as e:
            print "exception " + str(e)            

main()




