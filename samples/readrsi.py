import csv
import pandas as pd
import math


def printout(str):

    print str   

    return


if __name__ == '__main__':
    directory = "C:\\Python27\\Examples\\EventProfiler\\analysis\\rsi9\\output\\"
    filepath = directory + "seasonalrsi.csv"
    #reader = csv.reader(open(filepath,'rU'),delimiter=',')
    df_rsi_an = pd.read_csv(filepath)
    #for row in reader:
    #    printout(row[0])
    s = "0808.HK"
    
    r1 = df_rsi_an[(df_rsi_an.SYMBOL == s)]
    print r1
    
    r = df_rsi_an[(df_rsi_an.SYMBOL == s) & (df_rsi_an.MONTH==2)]
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
        print "MONTHLY OVERBOUGHT / OVERSOLD: " + str("%.2f" %round(b,1)) + ":" + str("%.2f" %round(s,1))

               
