from pathlib import Path
import os, yaml, json

def load_config(path='config.yaml'):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f'Config not found: {path}')
    return yaml.safe_load(p.read_text())

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def save_json(obj, path):
    ensure_dir(Path(path).parent)
    Path(path).write_text(json.dumps(obj, indent=2), encoding='utf-8')
