import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from snapshot_manager import load_snapshot, create_snapshot, SNAPSHOT_DIR

raw = SNAPSHOT_DIR / 'snapshot_3.json.gz'
if not raw.exists():
    print('No raw snapshot found at', raw)
    raise SystemExit(1)

data = load_snapshot(raw, decrypt=False)
enc_path = create_snapshot(3, data, encrypt=True)
print('Created encrypted snapshot at', enc_path)
