@echo off
REM Upgrade the repository using the Visual Studio terminal launcher.
setlocal
set REPO_DIR=%~dp0
set PYTHON=%REPO_DIR%.venv\Scripts\python.exe
if not exist "%PYTHON%" (
  echo Python virtual environment not found at %PYTHON%
  exit /b 1
)
pushd "%REPO_DIR%"
"%PYTHON%" tools\terminal_launcher_vs.py upgrade --target . --branch main
popd
endlocal
