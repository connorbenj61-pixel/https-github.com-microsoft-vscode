import os
import time
import threading
import subprocess
from typing import Optional, Callable

from upgrade_console import resolve_repo_target, clone_repository, update_repository, run_git_command


class RepoUpdater:
    def __init__(self, repo_url: Optional[str], target_dir: Optional[str], branch: Optional[str] = None):
        self.repo_url = repo_url
        self.target_dir = resolve_repo_target(target_dir, os.getcwd())
        self.branch = branch
        self._stop_event = threading.Event()

    def _git_head(self) -> Optional[str]:
        if not os.path.isdir(os.path.join(self.target_dir, '.git')):
            return None
        res = run_git_command(["-C", self.target_dir, "rev-parse", "HEAD"], cwd=self.target_dir)
        if res.returncode != 0:
            return None
        return res.stdout.strip()

    def ensure_cloned(self):
        if not os.path.isdir(self.target_dir) or not os.path.isdir(os.path.join(self.target_dir, '.git')):
            if not self.repo_url:
                raise RuntimeError("No repository URL provided to clone.")
            clone_repository(self.repo_url, self.target_dir)

    def stop(self):
        self._stop_event.set()

    def monitor(self, interval: int = 30, on_change: Optional[Callable[[str, str], None]] = None):
        # Ensure repo present
        try:
            self.ensure_cloned()
        except Exception as exc:
            if on_change:
                on_change("error", f"Clone failed: {exc}")
            return

        last_head = self._git_head()
        if on_change:
            on_change("info", f"Monitoring {self.target_dir} (HEAD={last_head})")

        while not self._stop_event.is_set():
            try:
                # Fetch and pull
                update_repository(self.target_dir, remote="origin", branch=self.branch)
                new_head = self._git_head()
                if new_head and new_head != last_head:
                    if on_change:
                        on_change("change", f"Updated: {last_head} -> {new_head}")
                    last_head = new_head
                else:
                    if on_change:
                        on_change("idle", f"No change detected (HEAD={last_head})")
            except Exception as exc:
                if on_change:
                    on_change("error", str(exc))
            # sleep with small increments so stop() is responsive
            for _ in range(max(1, int(interval))):
                if self._stop_event.is_set():
                    break
                time.sleep(1)

    def start_monitor_in_thread(self, interval: int = 30, on_change: Optional[Callable[[str, str], None]] = None) -> threading.Thread:
        t = threading.Thread(target=self.monitor, args=(interval, on_change), daemon=True)
        t.start()
        return t


__all__ = ["RepoUpdater"]
