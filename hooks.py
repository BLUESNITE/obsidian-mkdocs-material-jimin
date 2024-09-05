import sys
from pathlib import Path

def on_config(config):
    sys.path.append(str(Path(__file__).parent))