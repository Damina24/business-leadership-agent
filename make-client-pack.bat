@echo off
rem Builds the client PDF for the ACTIVE client. Double-click, or run in CMD.
cd /d "%~dp0"
py scripts\build_client_pack.py %*
if errorlevel 1 echo.& echo The PDF was not built. Read the message above.
pause
