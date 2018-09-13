REM 31 Jul 2018
REM File backup, exclude data files
echo %DATE%
set LOGFILE=Python%DATE:~10,4%%DATE:~4,2%%DATE:~7,2%
xcopy \python d:\projects\%LOGFILE% /e /v /c /i /y /exclude:excludedfiles.txt
