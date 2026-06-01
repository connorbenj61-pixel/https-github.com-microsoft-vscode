@echo off
REM Enhanced Archivist Terminal Launcher
REM Simple one-click launch of the improved Archivist Terminal

cd /d "%~dp0"
call .venv\Scripts\activate.bat
python archivist_terminal.py
pause
