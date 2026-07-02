import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from snapshot_manager import create_snapshot
from avatar_dance_learning import AvatarDanceLearner

# Gather state
avatar = AvatarDanceLearner(name='Snapshot2')
repo_target = os.path.abspath(os.getcwd())
# Try to read git remote URL if available
repo_url = ''
try:
    import subprocess
    if os.path.isdir(os.path.join(repo_target, '.git')):
        out = subprocess.run(['git', '-C', repo_target, 'config', '--get', 'remote.origin.url'], capture_output=True, text=True)
        if out.returncode == 0:
            repo_url = out.stdout.strip()
except Exception:
    repo_url = ''

log_text = ''
# If there's a launcher log file, include it
log_path = Path(repo_target) / 'launch_ai_desktop.log'
if log_path.exists():
    log_text = log_path.read_text(encoding='utf-8')[-2000:]

snapshot_data = {
    'avatar_name': avatar.name,
    'avatar_memory': avatar.memory,
    'repo_target': repo_target,
    'repo_url': repo_url,
    'log': log_text,
}

p = create_snapshot(2, snapshot_data, encrypt=True)
print('Created encrypted snapshot:', p)
