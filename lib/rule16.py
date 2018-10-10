#PRICE LEVEL

def apply(data, row, days=10, lthreshold=0.1, hthreshold=0.8):

    headers = data[0]
    
    col = headers.index("CLOSELV" + str(days))
    closelv = data[row][col]  #Close  - price level
    col = headers.index('CLOSECHG')
    closechg = data[row][col]  #Close - price level change

    col = headers.index("LOWLV" + str(days))
    lowlv = data[row][col]  #Low  - price level
    col = headers.index('LOWCHG')
    lowchg = data[row][col]  #Low - price level change

    col = headers.index("HIGHLV" + str(days))
    highlv = data[row][col]  #High  - price level
    col = headers.index('HIGHCHG')
    highchg = data[row][col]  #High - price level change

    signal = ""
  
    comment = str(days) + 'D PRICE LEVEL IS ' + str(closelv)

    if (closelv <= lthreshold or lowlv <= lthreshold) and closechg > 1:
        signal = "BUY"
        
    if (closelv >= hthreshold or highlv >= hthreshold) and closechg <= 1:
        signal = "SELL"
		
    return signal, comment


