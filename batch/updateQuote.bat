REM GET LATEST PRICE QUOTES
@echo off
cls
g:
cd\python
start /MIN /HIGH C:\Python27\python getpricequote.py %1
REM start /MIN  C:\Python27\python getexchrate.py

