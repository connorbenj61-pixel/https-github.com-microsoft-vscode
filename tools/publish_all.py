import os
import py_compile
import shutil
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _desktop_path() -> Path:
    return Path(os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop'))


def _create_shortcut_powershell(shortcut_path: Path, target: str, working_dir: str) -> None:
    ps = (
        f"$WshShell = New-Object -ComObject WScript.Shell;"
        f"$sc = $WshShell.CreateShortcut('{shortcut_path}');"
        f"$sc.TargetPath = '{target}';"
        f"$sc.WorkingDirectory = '{working_dir}';"
        f"$sc.Save();"
    )
    subprocess.run(["powershell", "-Command", ps], check=False)


def publish_script(script: Path) -> None:
    script = Path(script)
    if not script.exists():
        print(f"Skipping missing file: {script}")
        return

    name = script.stem

    # Try PyInstaller first
    pyinstaller = shutil.which('pyinstaller')
    venv_pi = BASE_DIR / '.venv' / 'Scripts' / 'pyinstaller.exe'
    if not pyinstaller and venv_pi.exists():
        pyinstaller = str(venv_pi)

    if pyinstaller:
        print(f"Packaging {script} with PyInstaller...")
        dist_dir = BASE_DIR / 'dist' / 'apps'
        dist_dir.mkdir(parents=True, exist_ok=True)
        cmd = [pyinstaller, '--onefile', '--distpath', str(dist_dir), str(script)]
        try:
            subprocess.run(cmd, check=True, cwd=str(BASE_DIR))
        except subprocess.CalledProcessError as exc:
            print(f"PyInstaller packaging failed for {script}: {exc}")
            return
        exe_path = dist_dir / (name + ('.exe' if os.name == 'nt' else ''))
        if exe_path.exists():
            print(f"Built executable: {exe_path}")
            shortcut = _desktop_path() / f"{name}.lnk"
            _create_shortcut_powershell(shortcut, str(exe_path), str(dist_dir))
            print(f"Shortcut created: {shortcut}")
        else:
            print("Expected executable not found after PyInstaller run.")
    else:
        # Fallback: create a batch wrapper that uses the current Python interpreter
        print(f"PyInstaller not found. Creating wrapper for {script}...")
        wrapper = BASE_DIR / f"run_{name}.bat"
        python_exe = Path(sys.executable)
        wrapper.write_text(f'"{python_exe}" "{script}" %*\n', encoding='utf-8')
        shortcut = _desktop_path() / f"{name}.lnk"
        _create_shortcut_powershell(shortcut, str(wrapper), str(BASE_DIR))
        print(f"Wrapper and shortcut created for {name}: {wrapper} -> {shortcut}")


def compile_all_python():
    print("Compiling all Python files to bytecode...")
    for p in BASE_DIR.rglob('*.py'):
        try:
            py_compile.compile(p, doraise=True)
        except py_compile.PyCompileError as exc:
            print(f"Compile failed for {p}: {exc}")
    print("Compilation complete.")


def main(argv):
    if not argv:
        print("Usage: publish_all.py <script1.py> [script2.py ...]")
        print("You can pass relative paths; default behavior is to compile all files only.")
        return 1

    compile_all_python()

    for a in argv:
        p = Path(a)
        if not p.is_absolute():
            p = Path.cwd() / p
        publish_script(p)

    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
