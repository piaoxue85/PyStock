REM g:
cd\python\weka

REM rem delete temp files

rem del results\*.*  /F /Q
rem del tempfiles\*.*  /F /Q

SET CLASSPATH = "C:\Program Files\Weka-3-8";C:\Program Files\Java\jdk1.8.0_131\bin;C:\Program Files (x86)\Java\jre1.8.0_144\bin"

java -cp .\weka.jar weka.filters.unsupervised.attribute.Remove -R %2 -i ..\data\weka\%1-COMPLETE.arff -o tempFiles\%1-HIGH.arff
java -cp .\weka.jar weka.filters.unsupervised.attribute.Remove -R %3 -i ..\data\weka\%1-COMPLETE.arff -o tempFiles\%1-LOW.arff

java -cp .\* weka.classifiers.functions.LinearRegression -S 0 -R 1.0E-8 -no-cv -num-decimal-places 4 -t tempFiles\%1-HIGH.arff -classifications "weka.classifiers.evaluation.output.prediction.CSV" >Results\%1-HIGH-RESULT.csv
java -cp .\* weka.classifiers.functions.LinearRegression -S 0 -R 1.0E-8 -no-cv -num-decimal-places 4 -t tempFiles\%1-LOW.arff -classifications "weka.classifiers.evaluation.output.prediction.CSV" >Results\%1-LOW-RESULT.csv

REM rem delete temp files

rem del tempFiles\%1-HIGH.arff
rem del tempFiles\%1-LOW.arff

rem del ..\data\weka\%1-TEST.arff
rem del ..\data\weka\%1-TEST.csv

rem del ..\data\weka\%1-TRAINING.arff
rem del ..\data\weka\%1-TRAINING.csv

rem del ..\data\weka\%1-COMPLETE.arff
rem del ..\data\weka\%1-COMPLETE.csv

exit

