#!/usr/bin/env python3
"""
Minecraft Enchantments Generator (Bullet TUI)
"""

import argparse
from bullet import Bullet, Check, Input
from mc_enchant import load_data
from mc_enchant.command_builder import build_give_command


MATERIAL_ITEMS = {
    "sword",
    "axe",
    "pickaxe",
    "shovel",
    "hoe",
    "helmet",
    "chestplate",
    "leggings",
    "boots",
    "mace",
}
MATERIALS = [
    "wooden",
    "stone",
    "iron",
    "golden",
    "diamond",
    "netherite",
]
CONFLICTS = {
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


def detect_conflicts(selected_ids):
    """Return a list of (a, b) conflicting enchantment pairs."""
    conflicts = []
    selected_set = set(selected_ids)

    for ench in selected_set:
        if ench in CONFLICTS:
            for bad in CONFLICTS[ench]:
                if bad in selected_set:
                    conflicts.append((ench, bad))

    return conflicts


def choose_item(data):
    """Let the user pick which item type they want to enchant."""
    items = sorted(data.keys())

    cli = Bullet(
        prompt="Which item do you want to spawn?",
        choices=items,
        bullet="•",
        margin=2,
        pad_right=4,
    )
    return cli.launch()


from bullet import Bullet

def choose_material(item_key):
    """Return material prefix for items that require it."""
    if item_key not in MATERIAL_ITEMS:
        return ""  # armor like 'armor', 'bow', 'trident', etc.

    cli = Bullet(
        prompt=f"Choose material for your {item_key}:",
        choices=MATERIALS,
        bullet="•",
        margin=2,
        pad_right=4,
    )
    return cli.launch()


def choose_enchantments(item_key, data):
    """Show enchantments for the selected item."""
    ench_list = data[item_key]["enchantments"]

    choices = [
        f"{e['name']} (max {e['max_level']})"
        for e in ench_list
    ]

    cli = Check(
        prompt=f"Select enchantments for {item_key}:",
        choices=choices,
        check="✓",
        margin=2,
        pad_right=4,
    )

    selected = cli.launch()

    # Convert back to enchantment dicts
    chosen = []
    for sel in selected:
        name = sel.split(" (")[0]
        for ench in ench_list:
            if ench["name"] == name:
                chosen.append(ench)
                break

    return chosen


def choose_levels(chosen):
    """Ask user for level of each chosen enchantment, unless max_level == 1."""
    final = {}
    for ench in chosen:
        max_lvl = ench["max_level"]

        # If only one level exists, auto‑assign it
        if max_lvl == 1:
            final[ench["id_name"]] = 1
            continue

        # Otherwise prompt the user
        prompt = f"{ench['name']} level (1–{max_lvl}): "
        lvl = Input(prompt=prompt).launch()

        try:
            lvl = int(lvl)
        except ValueError:
            lvl = 1

        lvl = max(1, min(lvl, max_lvl))
        final[ench["id_name"]] = lvl

    return final


def choose_custom_name():
    name = Input(prompt="Custom item name: ").launch()
    return name.strip() or "MC Enchanted Item"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--levels",
        action="store_true",
        help="Ask for enchantment levels instead of auto-selecting max levels"
    )
    args = parser.parse_args()

    data = load_data()

    item_key = choose_item(data)
    material = choose_material(item_key)
    full_item_key = f"{material}_{item_key}" if material else item_key

    # Enchantment selection loop (with conflict detection)
    while True:
        chosen = choose_enchantments(item_key, data)
        selected_ids = [e["id_name"] for e in chosen]
        conflicts = detect_conflicts(selected_ids)

        if not conflicts:
            break

        print("\n⚠️  Enchantment conflicts detected:")
        for a, b in conflicts:
            print(f"   - {a} conflicts with {b}")
        print("\nPlease adjust your selection.\n")

    # NEW: auto-max or manual levels
    if args.levels:
        levels = choose_levels(chosen)
    else:
        levels = {e["id_name"]: e["max_level"] for e in chosen}

    custom_name = choose_custom_name()

    cmd = build_give_command(
        item_key=full_item_key,
        enchantments=levels,
        custom_name=custom_name,
    )

    print("\nYour Minecraft command:\n")
    print(cmd)
    print("\nPaste this into your Minecraft chat window.\n")


if __name__ == "__main__":
    main()
