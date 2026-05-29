from __future__ import annotations

import re
from typing import Any, Dict, List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.digminecraft.com"
ENCHANTMENTS_URL = f"{BASE_URL}/lists/enchantment_list_pc.php"

ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5}


def _normalize_name(text: str) -> str:
    text = text.strip().lower()
    text = text.replace("'", "")
    text = re.sub(r"[^a-z0-9_ ]+", "", text)
    text = re.sub(r"\s+", " ", text)  # collapse multiple spaces
    text = text.replace(" ", "_")
    # text = text.replace("__", "_")
    text = re.sub(r"_+", "_", text)  # collapse multiple underscores
    return text


def _parse_max_level(text: str) -> int:
    """Parse max level from text like 'V (5)' or 'I (1)' or '1'."""
    text = text.strip()
    if text in ROMAN:
        return ROMAN[text]
    m = re.search(r"\((\d+)\)", text)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d+)", text)
    if m:
        return int(m.group(1))
    return 1


def _find_enchantment_table(soup: BeautifulSoup):
    """Find the enchantment table in a robust way."""
    tables = soup.find_all("table")
    for table in tables:
        headers = [th.get_text(strip=True).lower() for th in table.find_all("th")]
        if any("enchant" in h for h in headers):
            return table
    raise RuntimeError("Could not find enchantment table on page")


def _parse_main_list() -> List[Dict[str, Any]]:
    """Scrape the main list page and return basic enchantment info + detail URLs."""
    resp = requests.get(ENCHANTMENTS_URL, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    table = _find_enchantment_table(soup)

    enchantments: List[Dict[str, Any]] = []
    rows = table.find_all("tr")
    if not rows:
        raise RuntimeError("Enchantment table has no rows")

    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        # Column 0: Name + (id) + link
        name_cell = cols[0]
        raw_name = name_cell.get_text(" ", strip=True)
        if not raw_name:
            continue

        m = re.match(r"^(.*?)\s*\(([^)]+)\)\s*$", raw_name)
        if m:
            name = m.group(1).strip()
            raw_id = m.group(2).strip()
            id_name = _normalize_name(raw_id)
        else:
            # If DigMinecraft ever omits the (id), fall back to normalizing the name
            # BUT collapse whitespace first
            name = raw_name.strip()
            cleaned = re.sub(r"\s+", " ", name)
            id_name = _normalize_name(cleaned)

        link_tag = name_cell.find("a", href=True)
        detail_url = urljoin(BASE_URL, link_tag["href"]) if link_tag else None

        # Column 1: Max level
        max_level_text = cols[1].get_text(strip=True)
        max_level = _parse_max_level(max_level_text)

        # Column 2: Description
        description = cols[2].get_text(" ", strip=True)

        enchantments.append(
            {
                "id_name": id_name,
                "name": name,
                "max_level": max_level,
                "description": description,
                "detail_url": detail_url,
            }
        )

    return enchantments


APPLIES_MAP: Dict[str, List[str]] = {
    "helmet": ["helmet"],
    "helmets": ["helmet"],
    "chestplate": ["chestplate"],
    "chestplates": ["chestplate"],
    "leggings": ["leggings"],
    "boots": ["boots"],
    "sword": ["sword"],
    "swords": ["sword"],
    "axe": ["axe"],
    "axes": ["axe"],
    "pickaxe": ["pickaxe"],
    "pickaxes": ["pickaxe"],
    "shovel": ["shovel"],
    "shovels": ["shovel"],
    "hoe": ["hoe"],
    "hoes": ["hoe"],
    "bow": ["bow"],
    "bows": ["bow"],
    "crossbow": ["crossbow"],
    "crossbows": ["crossbow"],
    "trident": ["trident"],
    "tridents": ["trident"],
    "fishing rod": ["fishing_rod"],
    "fishing rods": ["fishing_rod"],
    "shield": ["shield"],
    "shields": ["shield"],
    "shears": ["shears"],
    "mace": ["mace"],
    "maces": ["mace"],
    "book": ["book"],
    "books": ["book"],
}


def _normalize_applies_to(text: str) -> List[str]:
    text = text.strip().lower()
    parts = [p.strip() for p in re.split(r",| and ", text) if p.strip()]
    result: List[str] = []
    for p in parts:
        if p in APPLIES_MAP:
            result.extend(APPLIES_MAP[p])
    return sorted(set(result))


def _parse_detail_page(url: str | None) -> List[str]:
    """Follow the enchantment detail page and extract 'Applies To' items."""
    if not url:
        return []

    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
    except Exception:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    # Look through all tables for a row whose first cell says "Applies To"
    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            cells = row.find_all(["th", "td"])
            if len(cells) < 2:
                continue

            label = cells[0].get_text(" ", strip=True).lower()
            if "applies to" not in label:
                continue

            applies_cell = cells[1]

            # First try: use <img alt="..."> values
            alts = [
                img.get("alt", "").strip().lower()
                for img in applies_cell.find_all("img")
            ]
            alts = [a for a in alts if a]

            if alts:
                items: List[str] = []
                for a in alts:
                    if a in APPLIES_MAP:
                        items.extend(APPLIES_MAP[a])
                return sorted(set(items))

            # Fallback: use text content
            text = applies_cell.get_text(" ", strip=True).lower()
            return _normalize_applies_to(text)

    return []


def scrape_all() -> Dict[str, Any]:
    """Scrape all enchantment data and return it as a dict."""
    base_list = _parse_main_list()
    enchantments: List[Dict[str, Any]] = []

    for ench in base_list:
        items = _parse_detail_page(ench.get("detail_url"))
        enchantments.append(
            {
                "id_name": ench["id_name"],
                "name": ench["name"],
                "max_level": ench["max_level"],
                "description": ench["description"],
                "items": items,
            }
        )

    return {"enchantments": enchantments}
