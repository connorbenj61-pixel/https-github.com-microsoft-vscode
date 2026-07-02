import sys
import os
import tkinter as tk
# Ensure project root is on sys.path when running from tools/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from avatar_dance_learning import AvatarDanceLearner
from launch_ai_desktop import DesktopAIAssistant

# create assistant instance without running mainloop
app = DesktopAIAssistant.__new__(DesktopAIAssistant)
app.root = tk.Tk()
app.root.withdraw()
app.repo_url_var = tk.StringVar(value='https://example.com/repo.git')
app.repo_target_var = tk.StringVar(value='.')
app.update_interval_var = tk.IntVar(value=10)
app.continuous_var = tk.BooleanVar(value=False)
app.log_text = tk.Text()
app._repo_updater = None
app._avatar = AvatarDanceLearner(name='Test')
app._panic_mode = False

# call enter_panic_mode to create snapshot
app.enter_panic_mode()
print('panic invoked')
