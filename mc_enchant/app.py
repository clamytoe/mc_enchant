#!/usr/bin/env python3
"""
app.py

Minecraft Enchantments Generator
"""

from bullet import Bullet, Check, styles

from mc_enchant import (
    export_data,
    generate_items,
    get_soup,
    generate_enchantments,
    load_data,
)


def item_selection(data):
    minecraft_items = set()
    for item in data:
        minecraft_items.add(item)

    minecraft_items = sorted(minecraft_items)

    cli = Bullet(
        prompt="Which item are you wanting to spawn? ",
        choices=minecraft_items,
        indent=0,
        align=2,
        margin=2,
        shift=0,
        bullet="",
        pad_right=5,
    )
    item = cli.launch()
    print(f"You have chosen: {item}")


def main():
    """This function is here to help you test your final code"""
    json_file = load_data()
    item_selection(json_file)


if __name__ == "__main__":
    main()
