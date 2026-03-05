@echo off
REM Activate the virtual environment and run the Amalgamation Game demo as a module
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python -m amalgamation_game.demo
