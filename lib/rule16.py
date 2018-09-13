#PRICE LEVEL

def apply(data, row, days=10, lthreshold=0.1, hthreshold=0.8):

    headers = data[0]
    
    col = headers.index("LV" + str(days))
    val1 = data[row][col]  #Latest price

    col = headers.index('CLOSECHG')
    val2 = data[row][col]  #Price level Change

    signal = ""
  
    comment = str(days) + 'D PRICE LEVEL IS ' + str(val1)

    if val1 <= lthreshold and val2 > 1:
        signal = "BUY"
        
    if val1 >= hthreshold and val2 <= 1:
        signal = "SELL"
		
    return signal, comment


