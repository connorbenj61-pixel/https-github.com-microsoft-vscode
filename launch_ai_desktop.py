import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import messagebox

from repo_updater import RepoUpdater
from avatar_dance_learning import AvatarDanceLearner
from snapshot_manager import create_snapshot


class DesktopAIAssistant:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CodeSquared AI Desktop")
        self.root.geometry("720x420")
        self.root.configure(bg="#0b1020")

        tk.Label(
            self.root,
            text="CodeSquared AI Desktop",
            bg="#0b1020",
            fg="#f2f6ff",
            font=("Segoe UI", 18, "bold"),
        ).pack(pady=(20, 10))

        tk.Label(
            self.root,
            text="Launch your avatar, music, and self-learning tools from here.",
            bg="#0b1020",
            fg="#9fb3d8",
            font=("Segoe UI", 11),
        ).pack(pady=(0, 20))

        buttons = [
            ("Run Avatar Demo", "python avatar_dance_learning.py"),
            ("Run Upgrade Console", "python upgrade_console.py"),
            ("Generate House MIDI", "python house_generator.py"),
        ]

        for label, command in buttons:
            tk.Button(
                self.root,
                text=label,
                width=28,
                command=lambda c=command: self.run_command(c),
                bg="#223a63",
                fg="white",
                relief="flat",
                pady=8,
            ).pack(pady=6)

        # Continuous repo updater controls
        tk.Label(self.root, text="Repository URL:", bg="#0b1020", fg="#cbdff6").pack(pady=(12, 0))
        self.repo_url_var = tk.StringVar(value="")
        tk.Entry(self.root, textvariable=self.repo_url_var, width=72).pack(pady=2)

        tk.Label(self.root, text="Target Directory:", bg="#0b1020", fg="#cbdff6").pack(pady=(6, 0))
        self.repo_target_var = tk.StringVar(value=os.path.abspath(os.getcwd()))
        tk.Entry(self.root, textvariable=self.repo_target_var, width=72).pack(pady=2)

        self.update_interval_var = tk.IntVar(value=30)
        tk.Label(self.root, text="Update interval (s):", bg="#0b1020", fg="#cbdff6").pack(pady=(6, 0))
        tk.Entry(self.root, textvariable=self.update_interval_var, width=10).pack(pady=2)

        self.continuous_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.root, text="Enable Continuous Repo Updates", variable=self.continuous_var, bg="#0b1020", fg="#cbdff6", command=self.toggle_continuous).pack(pady=(6, 6))

        # Status log
        tk.Label(self.root, text="Status Log:", bg="#0b1020", fg="#cbdff6").pack()
        self.log_text = tk.Text(self.root, height=6, width=80, bg="#071022", fg="#cfe6ff")
        self.log_text.pack(pady=(4, 8))

        self._repo_thread = None
        self._repo_updater = None
        self._avatar = AvatarDanceLearner(name="Astra")

        # Prank Panic Button
        panic_frame = tk.Frame(self.root, bg="#0b1020")
        panic_frame.pack(pady=(6, 12))
        self.panic_button = tk.Button(
            panic_frame,
            text="DO NOT PUSH THIS BUTTON",
            width=36,
            bg="#8b0000",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            command=self.enter_panic_mode,
            relief="raised",
            pady=10,
        )
        self.panic_button.pack()

        tk.Button(
            self.root,
            text="Exit",
            width=28,
            command=self.root.destroy,
            bg="#5a1f2f",
            fg="white",
            relief="flat",
            pady=8,
        ).pack(pady=12)

        self._panic_mode = False

        self.root.mainloop()

    def run_command(self, command):
        try:
            subprocess.Popen(command, shell=True, cwd=os.getcwd())
            messagebox.showinfo("Launched", f"Started: {command}")
        except Exception as exc:
            messagebox.showerror("Launch failed", str(exc))

    def log(self, level: str, message: str):
        self.log_text.insert(tk.END, f"[{level.upper()}] {message}\n")
        self.log_text.see(tk.END)

    def toggle_continuous(self):
        if self.continuous_var.get():
            repo = self.repo_url_var.get().strip() or None
            target = self.repo_target_var.get().strip() or None
            interval = max(5, int(self.update_interval_var.get()))
            self._repo_updater = RepoUpdater(repo, target)
            def cb(kind, msg):
                self.log(kind, msg)
                if kind == 'change':
                    # teach avatar from update event
                    pattern = msg
                    self._avatar.learn_from_feedback(pattern, 'update')
            self._repo_thread = self._repo_updater.start_monitor_in_thread(interval=interval, on_change=cb)
            messagebox.showinfo("Updater", "Continuous updates enabled.")
        else:
            if self._repo_updater:
                self._repo_updater.stop()
            self.log('info', 'Continuous updates stopped.')

    def enter_panic_mode(self):
        if self._panic_mode:
            return
        self._panic_mode = True
        # Stop background updater if running
        if self._repo_updater:
            try:
                self._repo_updater.stop()
            except Exception:
                pass
        # Write a local panic lock file to indicate hidden state (non-destructive)
        try:
            with open(os.path.join(os.getcwd(), "panic.lock"), "w", encoding="utf-8") as fh:
                fh.write("panic_mode=1\n")
        except Exception:
            pass
        # Create Snapshot #3: capture avatar memory, repo target, and recent log
        try:
            snapshot_data = {
                "avatar_name": self._avatar.name,
                "avatar_memory": self._avatar.memory,
                "repo_target": self.repo_target_var.get(),
                "repo_url": self.repo_url_var.get(),
                "log": self.log_text.get("1.0", tk.END),
            }
            create_snapshot(3, snapshot_data, encrypt=True)
            self.log('info', 'Snapshot #3 created')
        except Exception as exc:
            self.log('error', f"Snapshot failed: {exc}")
        # Hide main window and show a decoy
        self.root.withdraw()
        self._show_decoy_window()

    def _show_decoy_window(self):
        # Decoy window that looks innocuous; includes a restore button
        self._decoy = tk.Toplevel()
        self._decoy.title("System Utilities")
        self._decoy.geometry("480x200")
        tk.Label(self._decoy, text="System Utilities", font=("Segoe UI", 14, "bold")).pack(pady=12)
        tk.Label(self._decoy, text="Your system is running normally.", font=("Segoe UI", 11)).pack(pady=6)
        tk.Button(self._decoy, text="Restore Session", command=self.exit_panic_mode, bg="#264653", fg="white").pack(pady=18)
        # Make decoy topmost and non-resizable
        try:
            self._decoy.attributes("-topmost", True)
        except Exception:
            pass
        self._decoy.resizable(False, False)

    def exit_panic_mode(self):
        # Remove panic lock
        try:
            os.remove(os.path.join(os.getcwd(), "panic.lock"))
        except Exception:
            pass
        # Destroy decoy and restore main window
        try:
            if hasattr(self, "_decoy") and self._decoy:
                self._decoy.destroy()
        except Exception:
            pass
        self.root.deiconify()
        self._panic_mode = False
        self.log('info', 'Panic mode exited; UI restored.')


if __name__ == "__main__":
    DesktopAIAssistant()
