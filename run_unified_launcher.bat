@echo off
REM Unified Windows launcher for repository tools.
setlocal
set REPO_DIR=%~dp0
set PYTHON=%REPO_DIR%.venv\Scripts\python.exe
if not exist "%PYTHON%" (
  echo Python virtual environment not found at %PYTHON%
  exit /b 1
)
pushd "%REPO_DIR%"
"%PYTHON%" tools\unified_launcher.py
popd
endlocal
