@echo off
tasklist | findstr /i python.except
if %errorlevel% neq 0 goto restart
goto end
:restart
python TwitterStreamer.py
:end
exit
