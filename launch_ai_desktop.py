import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox


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

        self.root.mainloop()

    def run_command(self, command):
        try:
            subprocess.Popen(command, shell=True, cwd=os.getcwd())
            messagebox.showinfo("Launched", f"Started: {command}")
        except Exception as exc:
            messagebox.showerror("Launch failed", str(exc))


if __name__ == "__main__":
    DesktopAIAssistant()
