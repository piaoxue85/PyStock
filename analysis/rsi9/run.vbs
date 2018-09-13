	Dim Connstr
	Dim Rs
	Dim delimiter
	Dim SQL
	Dim CurrentDirectory
	Dim fs
	Dim rowText
	
	Dim Title
	Dim WshShell, i
	Set WshShell = CreateObject("WScript.Shell")
	Dim Idx

	set fs = CreateObject("Scripting.FileSystemObject")

	CurrentDirectory = fs.GetAbsolutePathName(".")

	Connstr = "Provider=MSDASQL.1;Persist Security Info=False;Extended Properties=""DSN=Text;DBQ=" & CurrentDirectory &";DefaultDir=" & CurrentDirectory &";DriverId=27;FIL=text;MaxBufferSize=2048;PageTimeout=5;"""
	
	Connstr ="Provider=MSDASQL.1;Persist Security Info=False;Extended Properties=""DSN=Text;DBQ=C:\Python27\Examples\EventProfiler\analysis\rsi9;DefaultDir=C:\Python27\Examples\EventProfiler\analysis\rsi9;DriverId=27;FIL=text;MaxBufferSize=2048;PageTimeout=5;"""

	Set Conn = CreateObject("adodb.connection")
	Conn.Open Connstr
	
	outputFilename = "seasonalrsi.csv"
	set ts=fs.CreateTextFile(outputFilename,true)

	SQL = "select * from [rsi9.csv]"
	Set SymbolRs = CreateObject("adodb.recordset")
	SymbolRs.Open SQL, Conn, 1, 1

	Set ResultRs = CreateObject("adodb.recordset")

	rowText = "SEASONAL PATTERN OF RSI OF SELECTED SHARES"
	ts.writeline(rowText)
	rowText = "SYMBOL,MONTH,OVERBOUGHT, OVERSOLD, ACTION"
	ts.writeline(rowText)

	for i = 1 to SymbolRs.fields.count -1

		SQL = "select MONTH, INDICATOR, COUNT(YEAR) as OCCURENCE from ( select distinct  [YEAR], [MONTH], INDICATOR from (select year(NoName) as [YEAR], month(NoName) as [MONTH], NoName, [0002] as RSI, iif([0002] < 30, 'Oversold', iif([0002] > 70, 'Overbought', '')) as [INDICATOR] from [rsi9.csv]) where Indicator <> '' ) group by MONTH, INDICATOR"
		SQL = replace(SQL, "[0002]", "[" & SymbolRs(i).Name & "]")

		ResultRs.open SQL, Conn, 1, 1

		WshShell.Popup "Processing " & SymbolRs(i).name, 1, "Progress" ' show message box for a second and close
			
		Redim val1(12)
		Redim val2(12)

		Do Until ResultRs.Eof

			if lcase(ResultRs(1)) = "overbought" then
			
				val1(ResultRs(0)) = ResultRs(2)

			elseif lcase(ResultRs(1)) = "oversold" then
			
				val2(ResultRs(0)) = ResultRs(2)
			end if
	
			ResultRs.Movenext
		Loop

		for j = 1 to 12

			rowText = symbolRs(i).Name &".HK"
			rowText = rowText & "," & j & ","
			rowText = rowText & val1(j) & ","
			rowText = rowText & val2(j) & ","
			if val1(j) > val2(j) then
				rowText = rowText & "SELL"
			elseif val1(j) = val2(j) then
				rowText = rowText & "TRADE"
			else
				rowText = rowText & "BUY"
			end if
			
			ts.writeline(rowText)				
		
		next	

		ResultRs.Close

	next

	Symbolrs.close
	