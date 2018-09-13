
import os
import sys, getopt

import itertools


def html(ofile):
        
        newlines = []

        #try:
        f = open(ofile)
        lines = f.readlines()
        c = 0
        tblid = 0
        newlines.append("<html>")
        newlines.append("<head>")
        newlines.append("<title>")
        newlines.append(ofile)
        
        newlines.append("</title>")
        newlines.append("</head>")             

        jsfile = "lib\\sorttable.js"
        jsf = open(jsfile)
        scripts = jsf.readlines()
        newlines = newlines + scripts
        jsf.close()

        newlines.append("<body>")

        newlines.append("<b>" + ofile + "</b><br/>")

        for line in lines:
                if len(line.strip()) == 0:
                        if c > 0:
                                newline = '</table>'
                                newlines.append(newline)
                        newline = "<br/><br/>"
                        newlines.append(newline)
                        c = 0
                else:
                        if line.find(",") > 0:
                                
                                if c == 0:
                                        tblid = tblid + 1
                                        newline = "<table width='100%' border='1' id='tbl" + str(tblid) + "'>"
                                        newlines.append(newline)
                                        headers = line.split(",")
                                        newline = ''
                                        hc = 0
                                        for header in headers:
                                                newline = newline + "<th>"
                                                newline = newline +  "<h3 onclick='colorCol(" + str(tblid) + "," + str(hc) + ")'>" + header + "</h3>"
                                                newline = newline + "<i class='arrow down' onclick='sortTable(" + str(tblid) + "," + str(hc) + ")'></i>"
                                                newline = newline + "&nbsp<h3 onclick='sumCol(" + str(tblid) + "," + str(hc) + ")'>&sum;</h3>"
                                                newline = newline + "&nbsp<h3 onclick='hideCol(" + str(tblid) + "," + str(hc) + ")'>[-]</h3>"

                                                newline = newline + '</th>'
                                                hc = hc + 1
                                        newline = "<tr>" + newline + '</tr>'
                                                                               
                                        
                                else:
                                        cells = line.split(",")
                                        newline = ''

                                        lenh = len(headers)
                                        
                                        if len(line.strip()) == 0:
                                                newline = "&nbsp"
                                        else:
                                                
                                                for i in range(0,len(cells)):
                                                        ct = cells[0]
                                                        prop = ''                                                        
                                                        v = cells[i]
                                                        try:
                                                                v = v.replace("%","")
                                                                v = float(v)
                                                                prop = " align='right'"
                                                        except:
                                                                if v.find(" ") == -1:
                                                                        prop = " align='center'"
                                                                pass
                                                        
                                                        
                                                        if i < lenh:
                                                                ct = cells[0] + ", " + headers[i]
                                                        newline = newline + "<td title = '" + ct + "'" + prop + ">" + cells[i].strip() + "</td>"
                                        newline = "<tr onclick='color(this)'>" + newline + "</tr>"
                
                                newlines.append(newline)
                                c = c + 1

                        else:
                                newline = line + "<br/>"
                                newlines.append(newline)
                        
        f.close()
        #except:
        #        print 'Error in opening ' + ofile

        newlines.append("</body>") 
        newlines.append("</html>") 

                
        return newlines


def convertfile(csvfile,htmlfile):

        ret = html(csvfile)
        f = open(htmlfile, "w")

        for line in ret:
                line = line.strip('\n')
                if len(line) > 0:
                        f.write(line + "\n")

        f.close()
                
