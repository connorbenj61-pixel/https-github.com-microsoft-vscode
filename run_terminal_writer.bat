@echo off
REM Launch the terminal code writer UI from the repository root.
setlocal
set REPO_DIR=%~dp0
set PYTHON=%REPO_DIR%.venv\Scripts\python.exe
if not exist "%PYTHON%" (
  echo Python virtual environment not found at %PYTHON%
  exit /b 1
)
pushd "%REPO_DIR%"
"%PYTHON%" tools\terminal_writer_ui.py
popd
endlocal
