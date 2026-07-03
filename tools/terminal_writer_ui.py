import os
import random
import shutil
import subprocess
import sys
import threading
import http.server
import socketserver
import socket
import urllib.parse
import json
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


BACKGROUND_TASKS: list[threading.Thread] = []


def _cleanup_background_tasks():
    global BACKGROUND_TASKS
    BACKGROUND_TASKS = [t for t in BACKGROUND_TASKS if t.is_alive()]


def run_in_background(target, *args, name: str | None = None, **kwargs):
    def wrapper():
        thread_name = name or getattr(target, '__name__', 'background_task')
        print(f"[BACKGROUND] Starting {thread_name}")
        try:
            target(*args, **kwargs)
            print(f"[BACKGROUND] Finished {thread_name}")
        except Exception as exc:
            print(f"[BACKGROUND] {thread_name} failed: {exc}")

    thread = threading.Thread(target=wrapper, daemon=True, name=name or 'background_task')
    BACKGROUND_TASKS.append(thread)
    thread.start()
    _cleanup_background_tasks()
    return thread


def show_background_tasks():
    _cleanup_background_tasks()
    if not BACKGROUND_TASKS:
        print("No active background tasks.")
        return
    print("Active background tasks:")
    for t in BACKGROUND_TASKS:
        print(f"  {t.name} - {'alive' if t.is_alive() else 'done'}")


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
    print("7) Publish a script (create exe or wrapper + shortcut)")
    print("8) Toggle autopublish on save")
    print("9) Start/Stop autopublish watcher")
    print("10) Run hello_world.py")
    print("11) Run sorter.py")
    print("12) Run demo_logger.py")
    print("13) Publish example scripts (hello_world, sorter, demo_logger)")
    print("14) Publish this UI (tools/terminal_writer_ui.py)")
    print("15) Publish script to browser (Pyodide HTML)")
    print("16) Design & publish custom HTML (create mini-browser)")
    print("17) Toggle periodic self-test")
    print("18) Toggle multitask mode (run long tasks in background)")
    print("19) Show active background tasks")
    print("20) Exit")
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
    if AUTOPUBLISH_ENABLED:
        run_in_background(publish_script, dest, name=f"autopublish:{dest.name}")


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
    # watcher state
    watcher_thread = None
    watcher_stop_event = None
    # periodic self-test state
    periodic_thread = None
    periodic_stop_event = None
    periodic_interval = 60  # seconds
    # multitask flag
    multitask_enabled = False

    def start_watcher():
        nonlocal watcher_thread, watcher_stop_event
        if watcher_thread and watcher_thread.is_alive():
            print("Watcher already running.")
            return
        watcher_stop_event = threading.Event()

        def _watch():
            seen = {}
            while not watcher_stop_event.is_set():
                for p in BASE_DIR.rglob('*.py'):
                    try:
                        m = p.stat().st_mtime
                    except Exception:
                        continue
                    if p not in seen or m > seen[p]:
                        seen[p] = m
                        # publish new/changed files
                        try:
                            publish_script(p)
                        except Exception as exc:
                            print(f"Watcher publish failed for {p}: {exc}")
                time.sleep(5)

        watcher_thread = threading.Thread(target=_watch, daemon=True)
        watcher_thread.start()
        print("Autopublish watcher started.")

    def run_in_background(fn, *args, **kwargs):
        """Run a function in background thread if multitask enabled, otherwise run inline."""
        if multitask_enabled:
            t = threading.Thread(target=lambda: fn(*args, **kwargs), daemon=True)
            t.start()
            return t
        else:
            return fn(*args, **kwargs)

    def _periodic_selftest():
        while not periodic_stop_event.is_set():
            try:
                # run a quick syntax check on this UI file
                subprocess.run([sys.executable, '-m', 'py_compile', str(BASE_DIR / 'tools' / 'terminal_writer_ui.py')], check=False)
            except Exception:
                pass
            # sleep with cancellation
            periodic_stop_event.wait(periodic_interval)

    def start_periodic_selftest():
        nonlocal periodic_thread, periodic_stop_event
        if periodic_thread and periodic_thread.is_alive():
            print('Periodic self-test already running.')
            return
        periodic_stop_event = threading.Event()
        periodic_thread = threading.Thread(target=_periodic_selftest, daemon=True)
        periodic_thread.start()
        print('Periodic self-test started.')

    def stop_periodic_selftest():
        nonlocal periodic_thread, periodic_stop_event
        if periodic_thread and periodic_thread.is_alive():
            periodic_stop_event.set()
            periodic_thread.join(timeout=3)
            periodic_thread = None
            periodic_stop_event = None
            print('Periodic self-test stopped.')
        else:
            print('Periodic self-test not running.')

    def stop_watcher():
        nonlocal watcher_thread, watcher_stop_event
        if watcher_thread and watcher_thread.is_alive():
            watcher_stop_event.set()
            watcher_thread.join(timeout=3)
            watcher_thread = None
            watcher_stop_event = None
            print("Autopublish watcher stopped.")
        else:
            print("Watcher not running.")

    global AUTOPUBLISH_ENABLED
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
            fn = input('Enter script to publish (relative or absolute): ').strip()
            if fn:
                p = Path(fn)
                if not p.is_absolute():
                    p = Path.cwd() / p
                run_in_background(publish_script, p)
            pause()
        elif choice == '8':
            AUTOPUBLISH_ENABLED = not AUTOPUBLISH_ENABLED
            print(f"AUTOPUBLISH_ENABLED = {AUTOPUBLISH_ENABLED}")
            pause()
        elif choice == '9':
            if watcher_thread and watcher_thread.is_alive():
                stop_watcher()
            else:
                start_watcher()
            pause()
        elif choice == '10':
            try:
                subprocess.run([sys.executable, str(BASE_DIR / 'hello_world.py')], cwd=str(BASE_DIR))
            except Exception as exc:
                print(f"Failed to run hello_world.py: {exc}")
            pause()
        elif choice == '11':
            try:
                subprocess.run([sys.executable, str(BASE_DIR / 'sorter.py')], cwd=str(BASE_DIR))
            except Exception as exc:
                print(f"Failed to run sorter.py: {exc}")
            pause()
        elif choice == '12':
            try:
                subprocess.run([sys.executable, str(BASE_DIR / 'demo_logger.py')], cwd=str(BASE_DIR))
            except Exception as exc:
                print(f"Failed to run demo_logger.py: {exc}")
            pause()
        elif choice == '13':
            def _publish_examples():
                for s in ('hello_world.py', 'sorter.py', 'demo_logger.py'):
                    try:
                        publish_script(BASE_DIR / s)
                    except Exception as exc:
                        print(f"Publish failed for {s}: {exc}")
            run_in_background(_publish_examples)
            pause()
        elif choice == '14':
            # Publish the UI script itself
            run_in_background(publish_script, BASE_DIR / 'tools' / 'terminal_writer_ui.py')
            pause()
        elif choice == '15':
            # Publish arbitrary script to HTML using Pyodide
            script = input("Path to script to publish in browser (relative to repo): ").strip()
            if not script:
                print("No script provided.")
            else:
                from tools.publish_web import publish_to_browser
                try:
                    full = BASE_DIR / script
                    run_in_background(publish_to_browser, full)
                except Exception as exc:
                    print(f"Publish to browser failed: {exc}")
            pause()
        elif choice == '16':
            # Design and publish custom HTML/JS/CSS with live preview server
            name = input("Output name (no extension, e.g. my_browser): ").strip()
            if not name:
                print("No name provided.")
                pause()
                continue

            out_dir = BASE_DIR / 'dist' / 'web'
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / f"{name}.html"

            # find a free local port
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('127.0.0.1', 0))
            port = s.getsockname()[1]
            s.close()

            class LiveHandler(http.server.SimpleHTTPRequestHandler):
                def __init__(self, *args, directory=None, **kwargs):
                    super().__init__(*args, directory=str(out_dir), **kwargs)

                def do_GET(self):
                    parsed = urllib.parse.urlparse(self.path)
                    if parsed.path.startswith('/_meta/'):
                        _, _, tail = parsed.path.partition('/_meta/')
                        requested = urllib.parse.unquote(tail)
                        if Path(requested).name != requested:
                            self.send_error(400, 'Invalid meta request')
                            return
                        target = out_dir / requested
                        payload = {'mtime': None}
                        if target.exists() and target.is_file():
                            try:
                                payload['mtime'] = target.stat().st_mtime
                            except Exception:
                                payload['mtime'] = None
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json; charset=utf-8')
                        self.end_headers()
                        self.wfile.write(json.dumps(payload).encode('utf-8'))
                        return
                    return super().do_GET()

            httpd = socketserver.ThreadingTCPServer(('127.0.0.1', port), LiveHandler)
            httpd.allow_reuse_address = True

            def server_thread():
                try:
                    httpd.serve_forever()
                except Exception:
                    pass

            t = threading.Thread(target=server_thread, daemon=True)
            t.start()

            print(f"Live preview server started at http://127.0.0.1:{port}/")
            print("Enter your HTML/JS/CSS below. End with a single line containing only .END")
            print("Each save will update the served page and the browser will auto-reload.")

            def wrap_with_reload(html_content: str) -> str:
                reload_snippet = (
                    f"""
<script>
;(function() {{
  const metaUrl = '/_meta/' + encodeURIComponent({json.dumps(name)});
  let lastMtime = null;
  async function check() {{
    try {{
      const r = await fetch(metaUrl, {{ cache: 'no-store' }});
      if (!r.ok) return;
      const j = await r.json();
      if (lastMtime && j.mtime && j.mtime !== lastMtime) {{
        location.reload(true);
      }}
      lastMtime = j.mtime;
    }} catch (e) {{
      console.warn('Live preview reload check failed', e);
    }}
  }}
  setInterval(check, 1000);
  check();
}})();
</script>
"""
                )
                return html_content + '\n' + reload_snippet

            while True:
                lines = []
                while True:
                    try:
                        ln = input()
                    except EOFError:
                        ln = '.END'
                    if ln.strip() == '.END':
                        break
                    lines.append(ln)
                if not lines:
                    print("No content entered. Exiting live-edit.")
                    break
                content = '\n'.join(lines)
                full = wrap_with_reload(content)
                try:
                    out_path.write_text(full, encoding='utf-8')
                    print(f"Wrote {out_path}")
                    try:
                        subprocess.run(['powershell', '-NoProfile', '-Command', f"Get-Content -Raw '{out_path}' | Set-Clipboard"], check=False)
                    except Exception:
                        pass
                    try:
                        import webbrowser
                        webbrowser.open(f'http://127.0.0.1:{port}/{out_path.name}')
                    except Exception:
                        pass
                except Exception as exc:
                    print(f"Failed to write file: {exc}")
                print("Enter new content to update (or just .END to finish live session):")

            try:
                httpd.shutdown()
            except Exception:
                pass
            pause()
        elif choice == '17':
            # Toggle periodic self-test
            if periodic_thread and periodic_thread.is_alive():
                stop_periodic_selftest()
            else:
                start_periodic_selftest()
            pause()
        elif choice == '18':
            # Toggle multitask mode
            multitask_enabled = not multitask_enabled
            print(f"Multitask mode = {multitask_enabled}")
            pause()
        elif choice == '19':
            show_background_tasks()
            pause()
        elif choice == '20':
            print("Goodbye. Keep coding and having fun.")
            stop_watcher()
            stop_periodic_selftest()
            break
        else:
            print("Unknown option. Please choose a valid menu number.")
            pause()


if __name__ == '__main__':
    main()
