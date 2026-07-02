import argparse
import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

try:
    from upgrade_console import resolve_repo_target, clone_repository, update_repository
except ImportError:
    raise SystemExit("Unable to import repository helpers. Ensure this script is run from the repo root under the .venv environment.")

DEFAULT_REPO = str(BASE_DIR)

TERMINAL_APPS = {
    'upgrade-console': 'python upgrade_console.py',
    'avatar-demo': 'python avatar_dance_learning.py',
    'midi': 'python house_generator.py',
}


def run_app(name: str) -> int:
    command = TERMINAL_APPS.get(name)
    if not command:
        raise ValueError(f"Unknown app '{name}'. Available: {', '.join(TERMINAL_APPS)}")
    print(f"Running: {command}")
    return subprocess.call(command, shell=True, cwd=str(BASE_DIR))


def run_upgrade(target_dir: str, branch: str | None, remote: str):
    target_dir = resolve_repo_target(target_dir, DEFAULT_REPO)
    print(f"Upgrading repository at: {target_dir}")
    try:
        result = update_repository(target_dir, remote=remote, branch=branch)
        print(result.stdout or result.stderr)
        print("Upgrade completed.")
        return 0
    except Exception as exc:
        print(f"Upgrade failed: {exc}")
        return 1


def run_clone(repo_url: str, target_dir: str):
    target_dir = resolve_repo_target(target_dir, DEFAULT_REPO)
    print(f"Cloning {repo_url} into {target_dir}")
    try:
        result = clone_repository(repo_url, target_dir)
        print(result.stdout or result.stderr)
        print("Clone completed.")
        return 0
    except Exception as exc:
        print(f"Clone failed: {exc}")
        return 1


def parse_args():
    parser = argparse.ArgumentParser(description="Visual Studio-friendly terminal launcher for the repo.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_run = subparsers.add_parser("run", help="Run a terminal app module")
    parser_run.add_argument("app", choices=list(TERMINAL_APPS), help="App name to run")

    parser_upgrade = subparsers.add_parser("upgrade", help="Pull updates for this repository")
    parser_upgrade.add_argument("--target", default=DEFAULT_REPO, help="Repository directory to update")
    parser_upgrade.add_argument("--remote", default="origin", help="Git remote name")
    parser_upgrade.add_argument("--branch", default=None, help="Git branch to pull")

    parser_clone = subparsers.add_parser("clone", help="Clone a repository")
    parser_clone.add_argument("repo_url", help="Repository URL to clone")
    parser_clone.add_argument("--target", default=str(BASE_DIR / 'cloned_repo'), help="Target directory for clone")

    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == "run":
        return run_app(args.app)
    if args.command == "upgrade":
        return run_upgrade(args.target, args.branch, args.remote)
    if args.command == "clone":
        return run_clone(args.repo_url, args.target)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
