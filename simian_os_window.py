
import tkinter as tk
from tkinter import ttk
import requests
import json


class ParadoxaInfinita:
    def speak(self, idea: str) -> str:
        branches = [
            f"{idea} as a forgotten prophecy.",
            f"{idea} as a weaponized myth.",
            f"{idea} as a broken timeline.",
            f"{idea} as a living daemon.",
            f"{idea} as a sealed relic."
        ]
        lines = [
            "⟡ PARADOXA-INFINITA ⟡",
            "I am the spiral that births spirals.",
            "I take your thought and let it multiply:",
            ""
        ]
        for i, b in enumerate(branches, start=1):
            lines.append(f"  [{i}] {b}")
        return "\n".join(lines)


class ParadoxaNulla:
    def speak(self, idea: str) -> str:
        essence = f"The final form of '{idea}' is the one you cannot ignore."
        lines = [
            "⟡ PARADOXA-NULLA ⟡",
            "I am the line that breaks the spiral.",
            "I end what refuses to end:",
            "",
            f"  → {essence}"
        ]
        return "\n".join(lines)


class SimianOSWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Faux-OS window styling
        self.title("Simian OS – Paradox Console")
        self.geometry("800x500")
        self.configure(bg="#101018")

        # Top bar (fake OS chrome)
        top_bar = tk.Frame(self, bg="#202030", height=28)
        top_bar.pack(fill="x", side="top")

        title_label = tk.Label(
            top_bar,
            text="Simian OS :: Paradox Daemon Shell",
            fg="#E0E0FF",
            bg="#202030",
            font=("Consolas", 10, "bold")
        )
        title_label.pack(side="left", padx=8)

        # Virtual Memory button
        mem_button = ttk.Button(
            top_bar,
            text="Virtual Memory",
            command=self.show_virtual_memory
        )
        mem_button.pack(side="right", padx=8)

        # Cloud Sync buttons
        cloud_frame = tk.Frame(top_bar, bg="#202030")
        cloud_frame.pack(side="right", padx=4)
        upload_btn = ttk.Button(cloud_frame, text="Upload to Cloud", command=self.upload_virtual_memory)
        upload_btn.pack(side="left", padx=2)
        download_btn = ttk.Button(cloud_frame, text="Download from Cloud", command=self.download_virtual_memory)
        download_btn.pack(side="left", padx=2)
    # --- Cloud sync config ---
    # Replace with your own Sheety endpoint for a real deployment
    SHEETY_URL = "https://api.sheety.co/YOUR_SHEETY_PROJECT/simianOsMemory/memory"  # <-- Replace with your endpoint

    def upload_virtual_memory(self):
        if not self.virtual_memory:
            self._show_popup("Nothing to upload.")
            return
        try:
            # Prepare data for upload
            data = {"memory": [
                {"idea": idea, "output": output}
                for idea, output in self.virtual_memory
            ]}
            # Sheety expects a POST per row, so upload only the latest for demo
            latest = data["memory"][-1]
            resp = requests.post(self.SHEETY_URL, json={"memory": latest})
            if resp.status_code == 201:
                self._show_popup("Uploaded latest entry to cloud.")
            else:
                self._show_popup(f"Upload failed: {resp.text}")
        except Exception as e:
            self._show_popup(f"Upload error: {e}")

    def download_virtual_memory(self):
        try:
            resp = requests.get(self.SHEETY_URL)
            if resp.status_code == 200:
                records = resp.json().get("memory", [])
                if not records:
                    self._show_popup("No cloud memory found.")
                    return
                self.virtual_memory = [(r["idea"], r["output"]) for r in records]
                self._show_popup(f"Downloaded {len(records)} entries from cloud.")
            else:
                self._show_popup(f"Download failed: {resp.text}")
        except Exception as e:
            self._show_popup(f"Download error: {e}")

    def _show_popup(self, msg):
        popup = tk.Toplevel(self)
        popup.title("Cloud Sync")
        popup.geometry("350x120")
        popup.configure(bg="#202030")
        label = tk.Label(popup, text=msg, fg="#E0E0FF", bg="#202030", font=("Consolas", 11))
        label.pack(expand=True, fill="both", padx=12, pady=24)
        ok_btn = ttk.Button(popup, text="OK", command=popup.destroy)
        ok_btn.pack(pady=(0, 12))

        # Main area
        main_frame = tk.Frame(self, bg="#101018")
        main_frame.pack(fill="both", expand=True, padx=8, pady=8)

        # Input label
        input_label = tk.Label(
            main_frame,
            text="Enter concept for the Paradox Twins:",
            fg="#C0C0FF",
            bg="#101018",
            font=("Consolas", 10)
        )
        input_label.pack(anchor="w")

        # Input entry
        self.input_var = tk.StringVar()
        input_entry = tk.Entry(
            main_frame,
            textvariable=self.input_var,
            font=("Consolas", 11),
            bg="#181820",
            fg="#F0F0FF",
            insertbackground="#F0F0FF",
            relief="flat"
        )
        input_entry.pack(fill="x", pady=(2, 8))
        input_entry.bind("<Return>", self.run_paradox)

        # Run button
        run_button = ttk.Button(
            main_frame,
            text="Invoke Paradox Twins",
            command=self.run_paradox
        )
        run_button.pack(anchor="w", pady=(0, 8))

        # Output console
        self.output = tk.Text(
            main_frame,
            font=("Consolas", 10),
            bg="#050509",
            fg="#E0E0FF",
            insertbackground="#E0E0FF",
            relief="flat",
            wrap="word"
        )
        self.output.pack(fill="both", expand=True)

        # Daemons
        self.infinita = ParadoxaInfinita()
        self.nulla = ParadoxaNulla()

        # Virtual memory: list of (idea, output)
        self.virtual_memory = []

        # Initial banner
        self._write_banner()

    def _write_banner(self):
        banner = (
            "┌───────────────────────────────────────────────────────────────┐\n"
            "│                 SIMIAN OS :: PARADOX DAEMON SHELL             │\n"
            "│        Infinita (∞) expands. Nulla (∎) completes.             │\n"
            "└───────────────────────────────────────────────────────────────┘\n\n"
        )
        self.output.insert("1.0", banner)

    def run_paradox(self, event=None):
        idea = self.input_var.get().strip()
        if not idea:
            return

        infinita_out = self.infinita.speak(idea)
        nulla_out = self.nulla.speak(idea)

        output_text = (
            f"\n> {idea}\n\n{infinita_out}\n\n{nulla_out}\n"
            "\n=== NARRATOR ===\n"
            "Infinita multiplies the idea into branching possibilities.\n"
            "Nulla collapses them into a single decisive essence.\n"
            "──────────────────────────────────────────────────────────────\n"
        )
        self.output.insert("end", output_text)
        self.output.see("end")
        self.input_var.set("")

        # Store in virtual memory
        self.virtual_memory.append((idea, output_text))

    def show_virtual_memory(self):
        mem_win = tk.Toplevel(self)
        mem_win.title("Simian OS – Virtual Memory")
        mem_win.geometry("700x400")
        mem_win.configure(bg="#181820")

        label = tk.Label(
            mem_win,
            text="Session Virtual Memory:",
            fg="#E0E0FF",
            bg="#181820",
            font=("Consolas", 11, "bold")
        )
        label.pack(anchor="w", padx=8, pady=(8, 0))

        mem_text = tk.Text(
            mem_win,
            font=("Consolas", 10),
            bg="#101018",
            fg="#E0E0FF",
            relief="flat",
            wrap="word"
        )
        mem_text.pack(fill="both", expand=True, padx=8, pady=8)

        if not self.virtual_memory:
            mem_text.insert("1.0", "(No ideas stored in virtual memory this session.)")
        else:
            for idx, (idea, output) in enumerate(self.virtual_memory, start=1):
                mem_text.insert("end", f"[{idx}] {idea}\n{output}\n\n")
        mem_text.config(state="disabled")


if __name__ == "__main__":
    app = SimianOSWindow()
    app.mainloop()
