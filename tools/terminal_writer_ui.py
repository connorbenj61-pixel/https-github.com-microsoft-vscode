import os
import random
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# If enabled, newly written scripts will be published automatically
AUTOPUBLISH_ENABLED = False

WELCOME_BANNER = """
========================================
  TERMINAL CODE WRITER + ENTERTAINMENT
========================================
"""

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I told my terminal a joke. It didn't laugh, but it returned a code.",
    "There are only 10 kinds of people in the world: those who understand binary and those who don’t.",
    "My software never has bugs. It just develops random features.",
    "If at first you don’t succeed, call it version 1.0.",
]

PROMPTS = [
    "Write a 5-line Python helper for sorting a list of custom objects.",
    "Create a terminal scoreboard for a game using ANSI colors.",
    "Generate a small story where a chatbot learns to dance to MIDI.",
    "Design a function that logs adventure events to a file.",
]

COMPLETIONS = [
    "import os",
    "import sys",
    "from pathlib import Path",
    "def main():",
    "if __name__ == '__main__':",
    "for i in range(10):",
    "while True:",
    "class MyClass:",
    "with open('file.txt', 'r') as f:",
    "try:",
    "except Exception as e:",
    "print()",
    "return",
    "path = Path('.')",
    "data = []",
    "config = {}",
    "logger.info('Starting...')",
    "sys.exit(0)",
]

COMPLETION_DEMO_CODE = """import os
from pathlib import Path

def list_python_files(path='.'): 
    path = Path(path)
    return [str(p.name) for p in path.iterdir() if p.suffix == '.py']


def greet(name: str):
    print(f'Hello, {name}!')


def main():
    print('=== Terminal Code Completion Demo ===')
    print('Python files in the current directory:')
    print('\n'.join(list_python_files('.')))
    greet('Terminal User')


if __name__ == '__main__':
    main()
"""


def autocomplete_suggestions(prefix: str) -> list[str]:
    prefix = prefix.strip()
    if not prefix:
        return COMPLETIONS[:8]
    return [item for item in COMPLETIONS if item.startswith(prefix)][:12]


def suggest_line(prefix: str) -> str | None:
    suggestions = autocomplete_suggestions(prefix)
    if not suggestions:
        print("No suggestions available.")
        return None
    print("Autocomplete suggestions:")
    for idx, item in enumerate(suggestions, 1):
        print(f"  {idx}) {item}")
    choice = input("Choose a suggestion number or press Enter to cancel: ").strip()
    if not choice:
        return None
    if choice.isdigit():
        num = int(choice)
        if 1 <= num <= len(suggestions):
            return suggestions[num - 1]
    print("Invalid choice.")
    return None


def show_completion_example():
    print("=== Code Completion Example ===")
    print("Type 'TAB' while editing to get suggestions for your current code line.")
    print("Example prefix: 'im'")
    suggestions = autocomplete_suggestions('im')
    for idx, item in enumerate(suggestions, 1):
        print(f"  {idx}) {item}")
    demo_path = BASE_DIR / 'tools' / 'completion_demo.py'
    demo_path.parent.mkdir(parents=True, exist_ok=True)
    demo_path.write_text(COMPLETION_DEMO_CODE, encoding='utf-8')
    print(f"\nCreated demo script: {demo_path}")
    print("Running the completion demo script now...\n")
    subprocess.run([sys.executable, str(demo_path)], cwd=str(demo_path.parent))


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input("\nPress Enter to continue...")


def _get_desktop_path() -> Path:
    return Path(os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop'))


def _create_windows_shortcut(target: str, working_dir: str, name: str) -> Path:
    """Create a .lnk shortcut on the user's Desktop pointing to target."""
    desktop = _get_desktop_path()
    try:
        import pythoncom  # type: ignore
    except Exception:
        # use COM via WScript shell through subprocess as fallback
        shortcut_path = desktop / f"{name}.lnk"
        ps = (
            f"$WshShell = New-Object -ComObject WScript.Shell;"
            f"$sc = $WshShell.CreateShortcut('{shortcut_path}');"
            f"$sc.TargetPath = '{target}';"
            f"$sc.WorkingDirectory = '{working_dir}';"
            f"$sc.Save();"
        )
        subprocess.run(["powershell", "-Command", ps], check=False)
        return shortcut_path
    else:
        # If pythoncom available, use it (rare in lightweight envs)
        from win32com.client import Dispatch  # type: ignore

        shell = Dispatch('WScript.Shell')
        shortcut_path = desktop / f"{name}.lnk"
        sc = shell.CreateShortcut(str(shortcut_path))
        sc.TargetPath = str(target)
        sc.WorkingDirectory = str(working_dir)
        sc.IconLocation = str(target)
        sc.Save()
        return shortcut_path


def publish_script(script_path: Path) -> None:
    """Attempt to publish a Python script as a Windows program and create a shortcut.

    Tries to use PyInstaller if available. If not, creates a batch wrapper
    and places a Desktop shortcut to the wrapper.
    """
    script_path = Path(script_path)
    if not script_path.exists():
        print(f"File not found for publishing: {script_path}")
        return

    # Try to find pyinstaller
    pyinstaller = shutil.which('pyinstaller')
    # also check venv
    venv_pyinstaller = BASE_DIR / '.venv' / 'Scripts' / 'pyinstaller.exe'
    if not pyinstaller and venv_pyinstaller.exists():
        pyinstaller = str(venv_pyinstaller)

    name = script_path.stem
    if pyinstaller:
        print(f"Packaging {script_path.name} with PyInstaller...")
        dist_dir = BASE_DIR / 'dist' / 'apps'
        dist_dir.mkdir(parents=True, exist_ok=True)
        cmd = [pyinstaller, '--onefile', '--distpath', str(dist_dir), str(script_path)]
        try:
            subprocess.run(cmd, check=True, cwd=str(BASE_DIR))
        except subprocess.CalledProcessError as exc:
            print(f"PyInstaller failed: {exc}")
            return
        exe_path = dist_dir / (name + ('.exe' if os.name == 'nt' else ''))
        if exe_path.exists():
            print(f"Built executable: {exe_path}")
            _create_windows_shortcut(str(exe_path), str(dist_dir), name)
            print(f"Shortcut created on Desktop for {name}.")
        else:
            print("Expected executable not found after packaging.")
    else:
        # Fallback: create batch wrapper that runs the script using the repo venv/python
        print("PyInstaller not found; creating batch wrapper and shortcut instead.")
        wrapper = BASE_DIR / f"run_{name}.bat"
        python_exe = Path(sys.executable)
        wrapper.write_text(f'"{python_exe}" "{script_path}" %*\n', encoding='utf-8')
        wrapper_path = str(wrapper)
        _create_windows_shortcut(wrapper_path, str(BASE_DIR), name)
        print(f"Wrapper created: {wrapper_path} and shortcut on Desktop.")


def print_header():
    clear_screen()
    print(WELCOME_BANNER)
    print("Your terminal is now a code-writing engine. Type code, run it, and get entertained.")
    print("Use option 1 to write a new Python file, option 2 to run it, and option 3 for a joke.")
    print("Press TAB while typing code to trigger autocomplete suggestions.")
    print("Option 6 runs a demo that writes and executes a completion example.")
    print("")


def display_menu():
    print_header()
    print("1) Write Python code to a file")
    print("2) Run an existing Python file")
    print("3) Entertain me")
    print("4) Self-update this repository")
    print("5) Show a creative prompt")
    print("6) Show code completion example")
    print("7) Exit")
    return input("Choose an option: ").strip()


def prompt_multiline(prompt: str) -> str:
    print(prompt)
    print("Enter your code below. Type EOF on a single line when finished.")
    print("Type 'TAB' on a new line to see completion suggestions for the current prefix.")
    lines = []
    while True:
        line = input()
        if line.strip() == "EOF":
            break
        if line.strip().upper() == "TAB":
            prefix = lines[-1] if lines else ""
            suggestion = suggest_line(prefix)
            if suggestion:
                if lines:
                    lines[-1] = suggestion
                else:
                    lines.append(suggestion)
                print(f"Replaced current line with: {suggestion}")
            continue
        lines.append(line)
    return "\n".join(lines) + "\n"


def write_code_file():
    filename = input("Enter Python filename (e.g. my_script.py): ").strip()
    if not filename:
        print("No filename entered.")
        return
    if not filename.endswith('.py'):
        filename += '.py'
    dest = Path(filename).resolve()
    if not dest.exists():
        print(f"Creating new file: {dest}")
    else:
        print(f"Editing existing file: {dest}")
    content = prompt_multiline("Write the Python code you want to save.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding='utf-8')
    print(f"Saved code to {dest}")


def run_python_file():
    filename = input("Enter the Python filename to run: ").strip()
    if not filename:
        print("No filename entered.")
        return
    if not filename.endswith('.py'):
        filename += '.py'
    dest = Path(filename).resolve()
    if not dest.exists():
        print(f"File not found: {dest}")
        return
    print(f"Running {dest}...\n")
    subprocess.run([sys.executable, str(dest)], cwd=str(dest.parent))


def entertain_me():
    joke = random.choice(JOKES)
    prompt = random.choice(PROMPTS)
    print("JOKE:")
    print(joke)
    print("\nCREATIVE PROMPT:")
    print(prompt)


def self_update_repo():
    print("Attempting to update the repository from origin/main...")
    result = subprocess.run(["git", "pull", "--ff-only", "origin", "main"], cwd=str(BASE_DIR), capture_output=True, text=True)
    if result.returncode == 0:
        print("Update complete. Output:")
        print(result.stdout.strip())
    else:
        print("Update failed:")
        print(result.stderr.strip() or result.stdout.strip())


def show_prompt():
    prompt = random.choice(PROMPTS)
    print("Try this:")
    print(prompt)


def main():
    while True:
        choice = display_menu()
        if choice == '1':
            write_code_file()
            pause()
        elif choice == '2':
            run_python_file()
            pause()
        elif choice == '3':
            entertain_me()
            pause()
        elif choice == '4':
            self_update_repo()
            pause()
        elif choice == '5':
            show_prompt()
            pause()
        elif choice == '6':
            show_completion_example()
            pause()
        elif choice == '7':
            print("Goodbye. Keep coding and having fun.")
            break
        else:
            print("Unknown option. Please choose 1-7.")
            pause()


if __name__ == '__main__':
    main()
