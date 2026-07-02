# Tools Launcher

This directory contains helpers for running the repository from the terminal.

## Terminal Launcher

Use the Visual Studio-friendly wrapper to run app modules and manage the repository:

```powershell
.venv\Scripts\python.exe tools\terminal_launcher_vs.py run upgrade-console
.venv\Scripts\python.exe tools\terminal_launcher_vs.py run avatar-demo
.venv\Scripts\python.exe tools\terminal_launcher_vs.py run midi
.venv\Scripts\python.exe tools\terminal_launcher_vs.py upgrade --target . --branch main
.venv\Scripts\python.exe tools\terminal_launcher_vs.py clone https://github.com/example/repo.git
```

## GUI Launcher

Start the desktop GUI launcher:

```powershell
.venv\Scripts\python.exe launch_ai_desktop.py
```

This opens the AI Desktop launcher window for:

- avatar demo
- upgrade console
- house MIDI generation
- continuous repo updates
- panic snapshot mode

## Windows Batch Shortcuts

These batch files provide one-line Windows launch commands:

```powershell
.\run_terminal_launcher_vs.bat run upgrade-console
.\run_terminal_upgrade_vs.bat
.\run_terminal_clone_vs.bat https://github.com/example/repo.git .\tools\cloned_repo
```

## Notes

- Ensure the repository virtual environment is available at `.venv`.
- The wrapper adds the repo root to `PYTHONPATH` so module imports work correctly.
