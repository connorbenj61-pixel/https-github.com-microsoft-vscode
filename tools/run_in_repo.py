import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def run_script(script: str, args: list[str] | None = None) -> int:
    args = args or []
    script_path = Path(script)
    if not script_path.is_absolute():
        script_path = BASE_DIR / script_path
    if not script_path.exists():
        print(f"Script not found: {script_path}")
        return 2
    env = os.environ.copy()
    # Ensure the repo root is on PYTHONPATH so scripts import local modules
    env['PYTHONPATH'] = str(BASE_DIR) + os.pathsep + env.get('PYTHONPATH', '')
    python_exe = sys.executable
    cmd = [python_exe, str(script_path)] + args
    print(f"Running: {' '.join(cmd)} (cwd={BASE_DIR})")
    return subprocess.run(cmd, cwd=str(BASE_DIR), env=env).returncode


def main(argv):
    if not argv:
        print("Usage: run_in_repo.py <script.py> [args...]")
        return 1
    script = argv[0]
    return run_script(script, argv[1:])


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
