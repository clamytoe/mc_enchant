#!/usr/bin/env python3
"""
app.py

Minecraft Enchantments Generator
"""
import json
from os import path
from urllib.request import urlretrieve

from bullet import Bullet, Check, styles

from mc_enchant.tools import enchants_permitted, gen_df, gen_file

FILENAME = "enchantments"
TMP_FILE = path.join("/tmp", "enchantment_list_pc.html")
URL = "https://www.digminecraft.com/lists/enchantment_list_pc.php"


def item_selection(filename):
    with open(filename) as file:
        data = json.loads(file.read())
    minecraft_items = set()
    for enchantment in data:
        items = enchantment["items"].split()
        for item in items:
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
        pad_right=5
    )
    item = cli.launch()
    print(f"You have chosen: {item}")


def main():
    if not path.isfile(TMP_FILE):
        urlretrieve(URL, TMP_FILE)

    permitted = enchants_permitted(TMP_FILE)
    enchantment_data = gen_df(TMP_FILE, items=permitted)
    # gen_file(enchantment_data, FILENAME)
    file = gen_file(enchantment_data, FILENAME, "json")

    item_selection(file)


if __name__ == "__main__":
    main()
