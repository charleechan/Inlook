:@echo off : Hide the Command, Only display the result, until it comes a @echo on
@echo off

if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit
REM


:begin your scripts below
.\PythonLibs\python.exe main.pyw