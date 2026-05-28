from __future__ import annotations

import re
from typing import Dict, List, Tuple

import requests
from bs4 import BeautifulSoup

from .models import Enchantment

ENCHANTMENTS_URL = "https://www.digminecraft.com/lists/enchantment_list_pc.php"


def _parse_max_level(text: str) -> int:
    # e.g. "V (5)" or "III (3)" or "1"
    m = re.search(r"(\d+)", text)
    return int(m.group(1)) if m else 1


def fetch_enchantments() -> Tuple[List[Enchantment], List[str]]:
    """
    Scrape DigMinecraft enchantment list and return:
    - list of Enchantment objects
    - sorted list of unique item labels (e.g. "Sword", "Helmet")
    """
    resp = requests.get(ENCHANTMENTS_URL, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")  # avoid lxml default

    table = soup.find("table", {"class": "minecraft_table"})
    if not table:
        raise RuntimeError("Could not find enchantment table on page")

    enchantments: List[Enchantment] = []
    item_labels: set[str] = set()

    # Skip header row
    rows = table.find_all("tr")[1:]

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 5:
            continue

        name = cols[0].get_text(strip=True)
        # Minecraft ID column often contains "minecraft:sharpness"
        mc_id_text = cols[2].get_text(strip=True)
        mc_id_match = re.search(r"minecraft:([a-z0-9_]+)", mc_id_text)
        if not mc_id_match:
            # Fallback: use raw text, last token, etc.
            mc_id = mc_id_text.split()[-1].lower()
        else:
            mc_id = mc_id_match.group(1)

        max_level_text = cols[1].get_text(strip=True)
        max_level = _parse_max_level(max_level_text)

        items_text = cols[4].get_text(" ", strip=True)
        # Items are usually comma-separated: "Sword, Axe"
        items = [i.strip() for i in items_text.split(",") if i.strip()]

        for it in items:
            item_labels.add(it)

        enchantments.append(
            Enchantment(
                name=name,
                mc_id=mc_id,
                max_level=max_level,
                items=items,
            )
        )

    return enchantments, sorted(item_labels)
