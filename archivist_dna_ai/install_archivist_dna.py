
import os
import sys
import subprocess

INSTALL_PATH = os.path.join(os.path.expanduser("~"), "ArchivistDNA")
SCRIPT_NAME = "archivist_dna.py"
BATCH_NAME = "run_archivist_dna.bat"

REQUIRED_PACKAGES = []  # Add any required pip packages here

def ensure_install_dir():
    if not os.path.exists(INSTALL_PATH):
        os.makedirs(INSTALL_PATH)
        print(f"[Installer] Created install directory: {INSTALL_PATH}")
    else:
        print(f"[Installer] Install directory already exists: {INSTALL_PATH}")

def copy_script():
    src = os.path.join(os.path.dirname(__file__), SCRIPT_NAME)
    dst = os.path.join(INSTALL_PATH, SCRIPT_NAME)
    if not os.path.exists(dst):
        with open(src, "r", encoding="utf-8") as fsrc, open(dst, "w", encoding="utf-8") as fdst:
            fdst.write(fsrc.read())
        print(f"[Installer] Copied {SCRIPT_NAME} to {INSTALL_PATH}")
    else:
        print(f"[Installer] {SCRIPT_NAME} already exists at {INSTALL_PATH}, not overwriting.")

def copy_batch():
    src = os.path.join(os.path.dirname(__file__), BATCH_NAME)
    dst = os.path.join(INSTALL_PATH, BATCH_NAME)
    if not os.path.exists(dst):
        with open(src, "r", encoding="utf-8") as fsrc, open(dst, "w", encoding="utf-8") as fdst:
            fdst.write(fsrc.read())
        print(f"[Installer] Copied {BATCH_NAME} to {INSTALL_PATH}")
    else:
        print(f"[Installer] {BATCH_NAME} already exists at {INSTALL_PATH}, not overwriting.")

def install_packages():
    for pkg in REQUIRED_PACKAGES:
        subprocess.run([sys.executable, "-m", "pip", "install", pkg], check=False)

def create_shortcut():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    shortcut_path = os.path.join(desktop, "ArchivistDNA.lnk")
    target = os.path.join(INSTALL_PATH, BATCH_NAME)
    # Use powershell to create a shortcut to the batch file
    ps = f'''$s=(New-Object -COM WScript.Shell).CreateShortcut('{shortcut_path}');$s.TargetPath='{target}';$s.Save()'''
    subprocess.run(["powershell", "-Command", ps], check=False)
    print(f"[Installer] Shortcut created on Desktop: ArchivistDNA.lnk")

def main():
    print("[Installer] Archivist DNA AI Self-Installer")
    ensure_install_dir()
    copy_script()
    copy_batch()
    install_packages()
    create_shortcut()
    print("[Installer] Installation complete. You can now run ArchivistDNA from your Desktop.")

if __name__ == "__main__":
    main()
