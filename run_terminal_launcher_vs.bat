@echo off
REM Run the Visual Studio-friendly terminal launcher using the repo virtual environment.
setlocal
set REPO_DIR=%~dp0
set PYTHON=%REPO_DIR%.venv\Scripts\python.exe
if not exist "%PYTHON%" (
  echo Python virtual environment not found at %PYTHON%
  echo Activate your .venv or update this batch file to point to a valid Python interpreter.
  exit /b 1
)
pushd "%REPO_DIR%"
"%PYTHON%" tools\terminal_launcher_vs.py %*
popd
endlocal
