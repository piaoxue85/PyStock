from lib import download as dl
import os.path
import pandas as pd
import numpy
import sys
from lib import globaldf


ldt_timestamps = []
df_confile = []

def readconfigfile(key):

    df_result = df_confile[df_confile.KEY==key]    
    return df_result['VALUE'].iloc[0]
            
if __name__ == '__main__':

    argv = sys.argv
    df_confile = globaldf.read('getexchrate.cfg')
    df = dl.asdf(readconfigfile('EXCHRATE'))
    df.to_csv('data\google\exchrate.csv',index=False)
    print df.head()
    
    
      


