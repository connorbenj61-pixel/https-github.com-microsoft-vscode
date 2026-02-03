"""Helpers to run the PowerShell diagnostics script on remote Windows machines
using PowerShell Remoting (Invoke-Command). This uses the local PowerShell
call and will send the local script to the remote host (no agent required on
the remote host, but PowerShell Remoting (WinRM) must be enabled there).

Security note: Passing plaintext passwords on the command line is insecure.
Prefer using certificate-based authentication, SSH remoting, or prompting
for credentials interactively.
"""
from __future__ import annotations

import json
import shlex
import subprocess
from getpass import getpass
from pathlib import Path
from typing import Optional


def run_remote_diagnostics(host: str, username: str, password: Optional[str] = None, script_path: str = "tools/diag.ps1", timeout: int = 60) -> dict:
    """Run the local PowerShell script on a remote Windows host via Invoke-Command.

    Returns the parsed JSON dict from the remote script output.

    Requirements on the remote host:
      - PowerShell Remoting (WinRM) enabled (Enable-PSRemoting -Force)
      - The caller must be able to authenticate with the supplied credentials

    WARNING: This implementation may expose the password on the local command
    line. Use with caution. For production, use a secure auth method.
    """
    if password is None:
        password = getpass(f"Password for {username}@{host}: ")

    script_path = Path(script_path).resolve()
    if not script_path.exists():
        raise FileNotFoundError(f"Local script not found: {script_path}")

    # Build a PowerShell command that constructs a PSCredential from the
    # plaintext password, then calls Invoke-Command with -FilePath to send the
    # local script to the remote host.
    # NOTE: this uses simple quoting; be careful with special characters in password.
    escaped_pass = password.replace('"', '\\"')
    ps_command = (
        f"$p = ConvertTo-SecureString \"{escaped_pass}\" -AsPlainText -Force; "
        f"$c = New-Object System.Management.Automation.PSCredential(\"{username}\",$p); "
        f"Invoke-Command -ComputerName \"{host}\" -Credential $c -FilePath \"{script_path}\" | ConvertTo-Json -Depth 6"
    )

    # Use powershell.exe on Windows. If pwsh is available and preferred, adjust accordingly.
    cmd = ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", ps_command]

    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)

    if proc.returncode != 0:
        raise RuntimeError(f"Remote command failed: {proc.stderr.strip()}")

    out = proc.stdout.strip()
    if not out:
        return {}

    try:
        return json.loads(out)
    except json.JSONDecodeError:
        # Sometimes PowerShell emits extra newlines or warnings; try to recover by
        # finding the first '{' and last '}' and parsing that substring.
        start = out.find('{')
        end = out.rfind('}')
        if start != -1 and end != -1 and end > start:
            sub = out[start:end+1]
            return json.loads(sub)
        raise


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="Run diag.ps1 on a remote Windows host via PowerShell Remoting")
    p.add_argument("host")
    p.add_argument("username")
    p.add_argument("--script", default="tools/diag.ps1")
    p.add_argument("--timeout", type=int, default=60)
    args = p.parse_args()

    try:
        data = run_remote_diagnostics(args.host, args.username, password=None, script_path=args.script, timeout=args.timeout)
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error: {e}")
