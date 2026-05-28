#!/usr/bin/env python3
"""
Minecraft Enchantments Generator (Bullet TUI)
"""

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
    """Ask user for level of each chosen enchantment."""
    final = {}
    for ench in chosen:
        prompt = f"{ench['name']} level (1–{ench['max_level']}): "
        lvl = Input(prompt=prompt).launch()

        try:
            lvl = int(lvl)
        except ValueError:
            lvl = 1

        lvl = max(1, min(lvl, ench["max_level"]))
        final[ench["id_name"]] = lvl

    return final


def choose_custom_name():
    name = Input(prompt="Custom item name (optional): ").launch()
    return name.strip() or None


def main():
    data = load_data()

    item_key = choose_item(data)
    material = choose_material(item_key)

    if material:
        full_item_id = f"{material}_{item_key}"
    else:
        full_item_id = item_key

    chosen = choose_enchantments(item_key, data)
    levels = choose_levels(chosen)
    custom_name = choose_custom_name()

    # Build final command
    cmd = build_give_command(
        item_key=full_item_id,
        enchantments=levels,
        custom_name=custom_name,
    )

    print("\nYour Minecraft command:\n")
    print(cmd)
    print("\nPaste this into your Minecraft chat window.\n")


if __name__ == "__main__":
    main()
