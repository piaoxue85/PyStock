g:
cd\python\weka

del results\%1-LOW-RESULT.csv
del results\%1-HIGH-RESULT.csv
del ..\results\prediction\%1.csv
del ..\data\weka\*.* /f /q

exit

