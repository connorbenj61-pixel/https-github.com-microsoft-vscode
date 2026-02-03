"""Local diagnostics collector.

Provides a simple cross-platform system diagnostics report (no external deps).
Returns a JSON-serializable dict.
"""
from __future__ import annotations

import json
import os
import platform
import shutil
import socket
import sys
import time
from datetime import datetime


def gather_system_diagnostics() -> dict:
    """Collect basic system diagnostics and return as a dict.

    This intentionally avoids external dependencies so it can run on most
    Python environments.
    """
    now = datetime.utcnow().isoformat() + "Z"

    try:
        hostname = socket.gethostname()
        fqdn = socket.getfqdn()
    except Exception:
        hostname = fqdn = "unknown"

    try:
        cwd = os.getcwd()
    except Exception:
        cwd = None

    # Disk usage for the current working drive
    try:
        root = os.path.splitdrive(cwd)[0] + os.sep if cwd and os.path.splitdrive(cwd)[0] else os.sep
        disk = shutil.disk_usage(root)
        disk_info = {
            "total_bytes": disk.total,
            "used_bytes": disk.used,
            "free_bytes": disk.free,
        }
    except Exception:
        disk_info = None

    info = {
        "timestamp": now,
        "platform": {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
        },
        "host": {
            "hostname": hostname,
            "fqdn": fqdn,
            "cwd": cwd,
            "env_count": len(os.environ),
        },
        "resources": {
            "cpu_count": os.cpu_count(),
            "disk": disk_info,
        },
        "sys_argv": sys.argv,
    }

    return info


def save_report(path: str, report: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)


def pretty_print(report: dict) -> None:
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    r = gather_system_diagnostics()
    pretty_print(r)
