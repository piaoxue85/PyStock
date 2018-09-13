import urllib
import urllib2
import csv
import pandas


def downloadfromgoogle(url):
    df = pandas.DataFrame()
    try:
        df = asdf(url)
        df['Date'] =  pandas.to_datetime(df['Date']).apply(lambda x: x.date())
        df = df.sort('Date')
    except Exception as e:
        print url + " - Error" + str(e)

    return df


def quotefromgoogle(url):
    df = pandas.DataFrame()
    try:
        df = asdf(url)
        
    except Exception as e:
        print url + " - Error" + str(e)

    return df

def quote(symbol, filepath):
    url = "http://download.finance.yahoo.com/d/quotes.csv?s=" + symbol + "&f=sl1d1t1c1ohgv&e=.csv"
    print "Downloading " + symbol + " from Yahoo"
    try:
        #urllib.urlretrieve (url, filepath)
        print "- Stopped"
    except:
        print symbol + " - Error"


def exchrate(symbol, filepath):
    url = "http://download.finance.yahoo.com/d/quotes.csv?s=" + symbol +"=X&f=sl1d1t1c1ohgv&e=.csv"
    print "Downloading " + symbol
    try:
        urllib.urlretrieve (url, filepath)
    except:
        print symbol + " - Error"

def symbolgroup():
    url = readconfigfile('SYMBOLGROUP')
    filepath = "data\\google\\symbolgroup.csv"
    print "Downloading Symbol Groups"
    #try:
    urllib.urlretrieve (url, filepath)

def transactions():
    filepath = "data\\google\\transactions.csv"
    url = readconfigfile('TRANSACTIONS')
        
    df_data = asdf(url)
    df_data['DATE'] =  pandas.to_datetime(df_data['DATE']).apply(lambda x: x.date())    
    df_data.to_csv(filepath,index =False)
    return df_data


def asdf(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    reader = csv.reader(response)
    ls_data = list(reader)
    headers = ls_data[0]
    df_data = pandas.DataFrame.from_records(ls_data[1:], columns=headers)
    return df_data

def historicalindex():
    url = readconfigfile('HISTORICALINDEX')
    filepath = "data\\google\\historical-data-index.csv"
    print "Downloading historical data index"
    #try:
    urllib.urlretrieve (url, filepath)    
    
def googleData():    
    #Stock list, now used as download index
    url = readconfigfile('GOOGLEDATA')
    filepath = "data\\google\\gdata.csv"
    print "Downloading Google Data"
    #try:
    urllib.urlretrieve (url, filepath)
    #except:
    #    print "Google Data - Error"

#Read url in config file
#31 AUG 2018
def readconfigfile(filename): 
    df_confile = pandas.read_csv('lib\\download.cfg')
    df_result = df_confile[df_confile.FILENAME==filename]    
    return df_result['URL'].iloc[0]    


