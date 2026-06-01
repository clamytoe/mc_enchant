from __future__ import annotations

import argparse
from typing import Dict, List, Tuple

from bullet import Bullet, Check, Input

from .enchantments_data import ENCHANTMENTS


# ─────────────────────────────────────────────────────────────
# Item → Material mapping
# ─────────────────────────────────────────────────────────────

MATERIAL_MAP = {
    # Tools
    "sword": ["wooden", "stone", "iron", "golden", "diamond", "netherite"],
    "axe": ["wooden", "stone", "iron", "golden", "diamond", "netherite"],
    "pickaxe": ["wooden", "stone", "iron", "golden", "diamond", "netherite"],
    "shovel": ["wooden", "stone", "iron", "golden", "diamond", "netherite"],
    "hoe": ["wooden", "stone", "iron", "golden", "diamond", "netherite"],

    # Armor
    "helmet": ["leather", "iron", "golden", "diamond", "netherite"],
    "chestplate": ["leather", "iron", "golden", "diamond", "netherite"],
    "leggings": ["leather", "iron", "golden", "diamond", "netherite"],
    "boots": ["leather", "iron", "golden", "diamond", "netherite"],

    # Single-material items (represented as [""])
    "shears": [""],
    "fishing_rod": [""],
    "flint_and_steel": [""],
    "carrot_on_a_stick": [""],
    "warped_fungus_on_a_stick": [""],
    "bow": [""],
    "crossbow": [""],
    "trident": [""],
    "mace": [""],
    "shield": [""],
    "elytra": [""],
    "brush": [""],
    "book": [""],
}

NO_MATERIAL_ITEMS = {
    "trident",
    "crossbow",
    "shield",
    "fishing_rod",
    "shears",
    "flint_and_steel",
    "carrot_on_a_stick",
    "warped_fungus_on_a_stick",
    "bow",
    "mace",
    "elytra",
    "brush",
    "book",
}


# ─────────────────────────────────────────────────────────────
# Enchantment conflict rules
# ─────────────────────────────────────────────────────────────

CONFLICTS: Dict[str, set[str]] = {
    "silk_touch": {"fortune"},
    "fortune": {"silk_touch"},
    "sharpness": {"smite", "bane_of_arthropods"},
    "smite": {"sharpness", "bane_of_arthropods"},
    "bane_of_arthropods": {"sharpness", "smite"},
    "protection": {"fire_protection", "blast_protection", "projectile_protection"},
    "fire_protection": {"protection", "blast_protection", "projectile_protection"},
    "blast_protection": {"protection", "fire_protection", "projectile_protection"},
    "projectile_protection": {"protection", "fire_protection", "blast_protection"},
    "depth_strider": {"frost_walker"},
    "frost_walker": {"depth_strider"},
    "multishot": {"piercing"},
    "piercing": {"multishot"},
    "riptide": {"channeling", "loyalty"},
    "channeling": {"riptide"},
    "loyalty": {"riptide"},
}


def detect_conflicts(selected_ids: List[str]) -> List[Tuple[str, str]]:
    """Return a list of unique conflicting enchantment pairs."""
    conflicts: List[Tuple[str, str]] = []
    selected_set = set(selected_ids)

    for ench in selected_set:
        if ench in CONFLICTS:
            for bad in CONFLICTS[ench]:
                if bad in selected_set:
                    conflicts.append((ench, bad))

    # Deduplicate symmetric pairs
    unique: set[Tuple[str, str]] = set()
    result: List[Tuple[str, str]] = []
    for a, b in conflicts:
        key = tuple(sorted((a, b)))
        if key not in unique:
            unique.add(key)
            result.append((a, b))
    return result


# ─────────────────────────────────────────────────────────────
# Build reverse index: item → enchantments
# ─────────────────────────────────────────────────────────────

def build_item_index(_: Dict[str, object] | None = None) -> Dict[str, List[Dict[str, object]]]:
    """
    Build a reverse index: item_key -> list of enchantment dicts.

    The optional argument is kept for backward compatibility and ignored.
    """
    item_index: Dict[str, List[Dict[str, object]]] = {}

    for ench_id, ench_data in ENCHANTMENTS.items():
        entry = {
            "id_name": ench_id,
            "name": ench_id.replace("_", " ").title(),
            "max_level": ench_data["max"],
            "items": ench_data["items"],
        }

        for item in ench_data["items"]:
            item_index.setdefault(item, []).append(entry)

    return item_index


# ─────────────────────────────────────────────────────────────
# UI helpers
# ─────────────────────────────────────────────────────────────

def pretty_item_name(item_key: str) -> str:
    return item_key.replace("_", " ").title()


def choose_item(item_index: Dict[str, List[Dict[str, object]]]) -> str:
    choices = sorted(item_index.keys())
    labels = [pretty_item_name(c) for c in choices]

    cli = Bullet(
        prompt="Choose an item:",
        choices=labels,
        bullet="•",
        margin=2,
        pad_right=4,
    )
    label = cli.launch()
    return dict(zip(labels, choices))[label]


def choose_material(item_key: str) -> str:
    if item_key in NO_MATERIAL_ITEMS:
        return ""

    materials = MATERIAL_MAP.get(item_key, [""])
    cli = Bullet(
        prompt=f"Choose material for your {item_key}:",
        choices=materials,
        bullet="•",
        margin=2,
        pad_right=4,
    )
    return cli.launch()


def choose_enchantments(item_key: str, item_index: Dict[str, List[Dict[str, object]]]):
    enchants = sorted(item_index[item_key], key=lambda e: e["name"].lower())
    choices = [f"{e['name']} (max {e['max_level']})" for e in enchants]

    cli = Check(
        prompt=f"Choose enchantments for your {pretty_item_name(item_key)}:",
        choices=choices,
        check="✓",
        margin=2,
        pad_right=4,
    )
    selected_labels = cli.launch()
    return [dict(zip(choices, enchants))[l] for l in selected_labels]


def choose_levels(chosen: List[Dict[str, object]]) -> Dict[str, int]:
    final: Dict[str, int] = {}

    for ench in chosen:
        max_lvl = ench["max_level"]
        if max_lvl == 1:
            final[ench["id_name"]] = 1
            continue

        lvl_str = Input(prompt=f"{ench['name']} level (1–{max_lvl}): ").launch()
        try:
            lvl = int(lvl_str)
        except ValueError:
            lvl = max_lvl

        lvl = max(1, min(lvl, max_lvl))
        final[ench["id_name"]] = lvl

    return final


def choose_custom_name() -> str | None:
    name = Input(prompt="Custom name (leave blank for none): ").launch().strip()
    return name or None


# ─────────────────────────────────────────────────────────────
# Command builder
# ─────────────────────────────────────────────────────────────

def build_give_command(
    item_key: str, enchantments: Dict[str, int], custom_name: str | None
) -> str:
    components: List[str] = []

    if enchantments:
        ench_parts = [f'"minecraft:{k}":{v}' for k, v in enchantments.items()]
        components.append("minecraft:enchantments={" + ",".join(ench_parts) + "}")

    if custom_name:
        components.append(f"minecraft:custom_name='{custom_name}'")

    comp_str = ",".join(components)
    return f"/give @p minecraft:{item_key}[{comp_str}] 1"


# ─────────────────────────────────────────────────────────────
# Main CLI
# ─────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manual-levels",
        action="store_true",
        help="Ask for enchantment levels instead of auto-selecting max levels",
    )
    args = parser.parse_args()

    item_index = build_item_index()

    item_key = choose_item(item_index)
    material = choose_material(item_key)
    full_item_key = f"{material}_{item_key}" if material else item_key

    while True:
        chosen = choose_enchantments(item_key, item_index)
        selected_ids = [e["id_name"] for e in chosen]
        conflicts = detect_conflicts(selected_ids)

        if not conflicts:
            break

        print("\n⚠️  Enchantment conflicts detected:")
        for a, b in conflicts:
            print(f"   - {a} conflicts with {b}")
        print("\nPlease adjust your selection.\n")

    levels = (
        choose_levels(chosen)
        if args.manual_levels
        else {e["id_name"]: e["max_level"] for e in chosen}
    )

    custom_name = choose_custom_name()

    cmd = build_give_command(full_item_key, levels, custom_name)

    print("\nYour Minecraft command:\n")
    print(cmd)
    print("\nPaste this into your Minecraft chat window.\n")


def cli():
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
