@echo off
REM Clone a repository using the Visual Studio terminal launcher.
setlocal
set REPO_DIR=%~dp0
set PYTHON=%REPO_DIR%.venv\Scripts\python.exe
if not exist "%PYTHON%" (
  echo Python virtual environment not found at %PYTHON%
  exit /b 1
)
if "%~1"=="" (
  echo Usage: %~nx0 <repo_url> [target_dir]
  exit /b 1
)
set REPO_URL=%~1
set TARGET_DIR=%~2
if "%TARGET_DIR%"=="" set TARGET_DIR=%REPO_DIR%cloned_repo
pushd "%REPO_DIR%"
"%PYTHON%" tools\terminal_launcher_vs.py clone "%REPO_URL%" --target "%TARGET_DIR%"
popd
endlocal
