@ECHO OFF

:BEGIN
CLS
ECHO.                 
ECHO            GALIEO STOCK ANALYSER
ECHO          ----- BY DAVID TSANG -----	     
ECHO.
ECHO.
ECHO        0=Auto
ECHO        1=Download historical data
ECHO        2=Download latest quotes
ECHO        3=Analyse
ECHO        4=Code backup
ECHO        5=Clean ram drive
ECHO        6=Exit To DOS
ECHO.
ECHO       To bring this menu back type GO.BAT at the dos prompt.
ECHO.
CHOICE /N /C:0123456 
rem PICK A NUMBER (0, 1, 2, 3, 4, 5, OR 6)%1
ECHO.
If ERRORLEVEL ==6 GOTO SIX
If ERRORLEVEL ==5 GOTO FIVE
If ERRORLEVEL ==4 GOTO FOUR
IF ERRORLEVEL ==3 GOTO THREE
IF ERRORLEVEL ==2 GOTO TWO
IF ERRORLEVEL ==1 GOTO ONE
IF ERRORLEVEL ==0 GOTO ZERO
GOTO END

:SIX
EXIT
GOTO QUIT

:FIVE
call cleanRamDrive.bat
GOTO END

:FOUR
call codebackup.bat
GOTO END

:THREE
call analyse.bat
GOTO END

:TWO
call updatequote.bat
GOTO END

:ONE
call updatehistorical.bat
GOTO END

:ZERO
call operator.bat
GOTO END

:END
cd\
REM ECHO Completed. Bringing up DOS menu again...
REM pause
REM f:go.bat

:QUIT
f: