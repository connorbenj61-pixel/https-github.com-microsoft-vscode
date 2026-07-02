import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TOOLS_DIR = BASE_DIR / "tools"

MENU = [
    ("Open GUI launcher (launch_ai_desktop.py)", [sys.executable, str(BASE_DIR / "launch_ai_desktop.py")]),
    ("Run upgrade console in terminal", [sys.executable, str(BASE_DIR / "upgrade_console.py")]),
    ("Run avatar demo", [sys.executable, str(BASE_DIR / "avatar_dance_learning.py")]),
    ("Generate house MIDI", [sys.executable, str(BASE_DIR / "house_generator.py")]),
    ("Run terminal writer UI", [sys.executable, str(TOOLS_DIR / "terminal_writer_ui.py")]),
    ("Run Visual Studio terminal launcher", [sys.executable, str(TOOLS_DIR / "terminal_launcher_vs.py"), "run", "upgrade-console"]),
    ("Self-update this repository", None),
    ("Clone a repository", None),
    ("Find terminal-related code files", None),
    ("Exit", None),
]

SEARCH_KEYWORDS = ["terminal", "launcher", "upgrade", "writer", "repo_updater", "snapshot"]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


def print_menu():
    clear_screen()
    print("============================================")
    print("  UNIFIED WINDOWS TOOL LAUNCHER")
    print("============================================")
    print("This program finds terminal tooling in the repo and starts the right script.")
    print("")
    for idx, (label, _) in enumerate(MENU, 1):
        print(f"{idx}) {label}")
    print("")


def run_command(args):
    print(f"Running: {' '.join(args)}")
    subprocess.run(args, cwd=str(BASE_DIR))


def self_update():
    print("Updating repository from origin/main...")
    result = subprocess.run(["git", "pull", "--ff-only", "origin", "main"], cwd=str(BASE_DIR), capture_output=True, text=True)
    if result.returncode == 0:
        print("Update completed successfully.")
        print(result.stdout.strip())
    else:
        print("Update failed:")
        print(result.stderr.strip() or result.stdout.strip())


def clone_repository():
    repo_url = input("Repository URL to clone: ").strip()
    if not repo_url:
        print("No URL provided.")
        return
    target = input("Target directory (relative or absolute): ").strip() or str(BASE_DIR / "cloned_repo")
    full_target = Path(target).expanduser().resolve()
    if full_target.exists() and any(full_target.iterdir()):
        print(f"Target already exists and is not empty: {full_target}")
        return
    print(f"Cloning {repo_url} into {full_target}")
    result = subprocess.run(["git", "clone", repo_url, str(full_target)], cwd=str(BASE_DIR), capture_output=True, text=True)
    if result.returncode == 0:
        print("Clone completed.")
    else:
        print("Clone failed:")
        print(result.stderr.strip() or result.stdout.strip())


def find_terminal_code():
    print("Searching for terminal-related code files...")
    matches = []
    for path in BASE_DIR.rglob("*.py"):
        try:
            text = path.read_text(errors="ignore").lower()
        except Exception:
            continue
        if any(keyword in text for keyword in SEARCH_KEYWORDS):
            matches.append(path.relative_to(BASE_DIR))
    matches = sorted(set(matches))
    if not matches:
        print("No terminal-related code found.")
        return
    print("Found files:")
    for item in matches:
        print(f"- {item}")
    print("\nYou can edit these files or run the unified launcher options.")


def main():
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(MENU)):
            print("Invalid entry. Choose a number from the menu.")
            pause()
            continue
        choice = int(choice)
        label, command = MENU[choice - 1]
        if label == "Exit":
            print("Exiting.")
            break
        if command:
            run_command(command)
            pause()
            continue
        if label == "Self-update this repository":
            self_update()
            pause()
            continue
        if label == "Clone a repository":
            clone_repository()
            pause()
            continue
        if label == "Find terminal-related code files":
            find_terminal_code()
            pause()
            continue


if __name__ == "__main__":
    main()
