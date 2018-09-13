from lib import download as dl
import csv
from lib import sharedfunctions as fn
import datetime as dt

ldt_timestamps = []
    
def run():

    global ls_symbols
    ls_symbols = fn.readsymbols('currencies')
    
    directory = "data\\exchrate\\"

    for s in ls_symbols:
        filepath = directory + s + ".csv"
        dl.exchrate(s, filepath)
        reader = csv.reader(open(filepath,'rU'),delimiter=',')
            
if __name__ == '__main__':
    run()


