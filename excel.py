import csv
import random
import math
import operator

import os
import sys, getopt

import itertools

from lib import sharedfunctions as fn
from lib import download as dl

from dateutil.relativedelta import relativedelta
from timeit import default_timer as timer
import datetime as dt

from lib import knn as knn
from lib import knndata as knndata

import pandas as pd
import numpy as np

import copy

# if we read f.csv we will write f.xlsx
#wb = xlsxwriter.Workbook(sys.argv[1].replace(".csv",".xlsx"))

fnn = 'results\\BUY-NYSE.csv'

##wb = xlsxwriter.Workbook(fnn.replace(".csv",".xlsx"))
##
##ws = wb.add_worksheet("WS1")    # your worksheet title here
##with open(fnn,'r') as csvfile:
##    table = csv.reader(csvfile)
##    i = 0
##    # write each row from the csv file as text into the excel file
##    # this may be adjusted to use 'excel types' explicitly (see xlsxwriter doc)
##    for row in table:
##        ws.write_row(i, 0, row)
##        i += 1
##wb.close()

df= pd.read_csv(fnn)

writer = pd.ExcelWriter(fnn.replace(".csv",".xlsx"), engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')
writer.save()
