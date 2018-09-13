import pandas as pd
import sharedfunctions as fn
import datetime as dt
import os.path
import pandas as pd
import numpy


def run(df, fname, title,market):
	if market== 'HSI':
		run_HSI(df, fname, title)

	return

def run_HSI(df, fname, title):

    html = []

    html.append("	<html>	")
    html.append("	<head>	")
    html.append("	<title>	")
    html.append("	" + title +"	")
    html.append("	</title>	")
    html.append("	</head>	")
    html.append("	<body bgcolor=\"#CCCCCC\">	")
    html.append("	<h1>" + title + "</h1>	")
    html.append("	<table width=\"100%\">	")

    c = 0

    r = len(df)

    for i in range(0,r):

        symbol = fn.filenameFormatter(df.iloc[i]['SYMBOL'])

        if c == 0:
            html.append("	<tr>	")
    
        html.append("	<td align=\"center\">	")
        closechg = str(round((df.iloc[i]['CLOSECHG']-1)*100,4))
        str1 = "	<b>" + str(df.iloc[i]['SYMBOL']) + " " + df.iloc[i]['NAME'] + " <br/> " + str(df.iloc[i]['CLOSE']) + " (" + str(closechg) + "%)</b>"
        str1 = str1 + "- RSI9: " + str(round(df.iloc[i]['RSI9'],0)) + "<br/>"
        html.append(str1)
        url1 = "<a href=\"http://finance.now.com/stock/index.php?s=" + symbol +"&range=3m&chartType=candlesticks&overlays=sma&indicator1=rsi#chart\">"
        html.append(url1)
        html.append("	<img src=\"g:\python\data\charts\\" + str(symbol) + ".png\">")
        html.append("</a>")
        html.append("	<br/>	")

        url = "http://charts.aastocks.com/servlet/Charts?com=50004&stockid=" + str(symbol) +".HK&period=0&lang=0&scheme=0&height=213&footerStyle=1&width=174"
        html.append(url1)
        html.append("	<img src=\"" + url + "\">")
        html.append("</a>")
        html.append("	<br>	")
        html.append("	OS: " + str(df.iloc[i]['OVERSOLD']))
        html.append("	L: " + str(df.iloc[i]['LOW']))        
        html.append("	<br>	")
        html.append("	OB: " + str(df.iloc[i]['OVERBOUGHT']))
        html.append("	H: " + str(df.iloc[i]['HIGH']))
        if df.iloc[i]['PHIGH'] > 0 and df.iloc[i]['PLOW'] > 0:
            html.append("	<br>	")
            html.append("	PLOW: " + str(df.iloc[i]['PLOW']))
            html.append("	PHIGH: " + str(df.iloc[i]['PHIGH']))
        if df.iloc[i]['ONHAND'] > 0:
            try:
                html.append("	<br>	")
                str1 = "	PL: " + str(df.iloc[i]['PL'])
                str1 = str1 + " (" + str(df.iloc[i]['PL%']) + ")"
                html.append(str1)
            except Exception, e:
                print e
        
        html.append("	<br>	")
        html.append("	</td>	")
        html.append("		")

        c = c + 1

        if c >= 5:
            html.append("	</tr>	")
            c = 0

    if c <> 0:
        html.append("	</tr>	")        
            
    html.append("	</table>	")
    html.append("	<hr>	")
    html.append("	<center>	")
    html.append("	Galileo Stock Analyzer	")
    html.append("		")
    html.append("	</center>	")
    html.append("		")
    html.append("	</body>	")
    html.append("	</html>	")

    directory = "results\\"
    fname = directory + fname + ".htm"
    hf = open(fname, "w")

    for l in html:
        hf.write(l + chr(13))

    hf.close()

    return html





