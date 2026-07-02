# Quick Start Guide

This guide helps you run the repository using the local terminal tools and batch shortcuts.

## Prerequisites

- Open the repository in Visual Studio Code.
- Ensure the local virtual environment is available at `.venv`.
- Use the workspace Python interpreter from `.venv`.

## Helpful Files

- `tools/README.md` — documentation for the tools directory
- `tools/terminal_launcher_vs.py` — terminal launcher wrapper for VS Code
- `run_terminal_launcher_vs.bat` — run module launcher from Windows
- `run_terminal_upgrade_vs.bat` — update the current repository from Windows
- `run_terminal_clone_vs.bat` — clone a repository from Windows

## Run the App

From PowerShell or cmd:

```powershell
.\run_terminal_launcher_vs.bat run upgrade-console
```

## Run the GUI Launcher

Start the desktop launcher directly:

```powershell
.venv\Scripts\python.exe launch_ai_desktop.py
```

This opens the GUI window for:

- avatar demo
- upgrade console
- house MIDI generation
- continuous repo updates
- panic snapshot mode

## Upgrade the Repo

```powershell
.\run_terminal_upgrade_vs.bat
```

## Clone a Repository

```powershell
.\run_terminal_clone_vs.bat https://github.com/example/repo.git .\tools\cloned_repo
```

## Alternative Python Commands

If you prefer Python directly:

```powershell
.venv\Scripts\python.exe tools\terminal_launcher_vs.py run upgrade-console
.venv\Scripts\python.exe tools\terminal_launcher_vs.py upgrade --target . --branch main
.venv\Scripts\python.exe tools\terminal_launcher_vs.py clone https://github.com/example/repo.git
```
