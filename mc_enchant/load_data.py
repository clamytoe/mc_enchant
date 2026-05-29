from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

DATA_FILE = Path(__file__).parent / "enchantments.json"


def data_exists() -> bool:
    return DATA_FILE.exists()


def load_data() -> Dict[str, Any]:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: Dict[str, Any]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
