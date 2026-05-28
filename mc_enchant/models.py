from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Enchantment:
    name: str
    mc_id: str          # e.g. "sharpness"
    max_level: int
    items: List[str]    # e.g. ["sword", "axe"]


@dataclass
class ItemSelection:
    item_label: str                 # e.g. "Sword"
    enchantments: Dict[str, int]    # mc_id -> level
    custom_name: Optional[str] = None
    item_id: Optional[str] = None   # e.g. "diamond_sword"
