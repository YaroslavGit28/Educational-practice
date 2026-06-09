"""Загрузка переменных из .env в os.environ (без внешних зависимостей)."""
import os
from pathlib import Path


def load_env_file(path=None):
    if path is None:
        path = Path(__file__).resolve().parent.parent / ".env"
    else:
        path = Path(path)

    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)
