REM 13 Seo 2018
REM File backup, exclude data files

xcopy \python D:\GitHub\PyStock /e /v /c /i /y /exclude:excludedfiles-github.txt
