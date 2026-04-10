@echo off
REM Launch Commercial AI Suite in workspace venv
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python run_commercial_ai_suite.py
pause
