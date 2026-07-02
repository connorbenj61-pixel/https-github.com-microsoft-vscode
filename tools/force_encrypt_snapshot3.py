import os
from pathlib import Path
from cryptography.fernet import Fernet
import base64

SNAPSHOT_DIR = Path.cwd() / 'snapshots'
raw = SNAPSHOT_DIR / 'snapshot_3.json.gz'
enc = SNAPSHOT_DIR / 'snapshot_3.json.gz.enc'
keyfile = SNAPSHOT_DIR / 'snapshot.key'

if not raw.exists():
    print('raw snapshot not found:', raw)
    raise SystemExit(1)

if not keyfile.exists():
    key = Fernet.generate_key()
    keyfile.write_bytes(key)
else:
    key = keyfile.read_bytes()

f = Fernet(key)
payload = raw.read_bytes()
token = f.encrypt(payload)
enc.write_bytes(base64.b64encode(token))
print('Wrote encrypted snapshot to', enc)
