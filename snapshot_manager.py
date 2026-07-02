import os
import json
import gzip
import base64
from pathlib import Path
from typing import Any, Dict

try:
    from cryptography.fernet import Fernet
    _have_crypto = True
except Exception:
    _have_crypto = False

SNAPSHOT_DIR = Path(os.getcwd()) / "snapshots"
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)


def _generate_key(path: Path):
    key = Fernet.generate_key()
    path.write_bytes(key)
    return key


def _load_or_create_key(path: Path):
    if not _have_crypto:
        return None
    if not path.exists():
        return _generate_key(path)
    return path.read_bytes()


def create_snapshot(number: int, data: Dict[str, Any], encrypt: bool = True) -> Path:
    """Create a timestamped snapshot file with optional encryption.

    Returns the path to the snapshot file.
    """
    fname = SNAPSHOT_DIR / f"snapshot_{number}.json.gz"
    # Serialize to JSON and gzip
    payload = json.dumps(data, default=str).encode("utf-8")
    compressed = gzip.compress(payload)

    if encrypt and _have_crypto:
        key_path = SNAPSHOT_DIR / "snapshot.key"
        key = _load_or_create_key(key_path)
        f = Fernet(key)
        token = f.encrypt(compressed)
        # Save base64 for easier handling
        fname = SNAPSHOT_DIR / f"snapshot_{number}.json.gz.enc"
        fname.write_bytes(base64.b64encode(token))
    else:
        # Save raw gzip
        fname.write_bytes(compressed)
    return fname


def load_snapshot(path: Path, decrypt: bool = True) -> Dict:
    raw = path.read_bytes()
    if decrypt and _have_crypto and path.suffix == ".enc":
        key_path = SNAPSHOT_DIR / "snapshot.key"
        key = _load_or_create_key(key_path)
        from cryptography.fernet import Fernet

        f = Fernet(key)
        token = base64.b64decode(raw)
        data = f.decrypt(token)
        return json.loads(gzip.decompress(data).decode("utf-8"))
    else:
        return json.loads(gzip.decompress(raw).decode("utf-8"))
