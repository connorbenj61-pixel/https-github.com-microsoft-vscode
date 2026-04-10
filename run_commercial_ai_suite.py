"""
Run Commercial AI Suite in Infinite Loop
This script runs the most commercially viable AI modules in sequence, looping forever.
"""
import subprocess
import sys
import time

# List of scripts to run (relative to workspace root)
SCRIPTS = [
    "animus_ai.py",
    "ai_camera_recognition.py",
    "quantum_3d_visualizer.py",
    "laser_printer_interface.py",
    "amalgamation_game/royal_ai_compiled.py",
    "amalgamation_game/ai_coordinator.py",
    "amalgamation_game/main.py",
]

PYTHON = sys.executable

while True:
    for script in SCRIPTS:
        print(f"\n[RUNNING] {script}\n" + "-"*40)
        try:
            result = subprocess.run([PYTHON, script], check=False)
            print(f"[FINISHED] {script} (exit code: {result.returncode})\n")
        except Exception as e:
            print(f"[ERROR] {script}: {e}\n")
        time.sleep(2)  # Short pause between scripts
    print("\n[LOOPING BACK TO START]\n" + "="*40)
    time.sleep(5)
