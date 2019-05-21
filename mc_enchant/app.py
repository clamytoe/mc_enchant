#!/usr/bin/env python3
"""
app.py

Minecraft Enchantments Generator
"""
from os import path
from urllib.request import urlretrieve

from mc_enchant.tools import enchants_permitted, gen_df, gen_file

FILENAME = "enchantments"
TMP_FILE = path.join("/tmp", "enchantment_list_pc.html")
URL = "https://www.digminecraft.com/lists/enchantment_list_pc.php"


def main():
    if not path.isfile(TMP_FILE):
        urlretrieve(URL, TMP_FILE)

    permitted = enchants_permitted(TMP_FILE)
    enchantment_data = gen_df(TMP_FILE, items=permitted)
    gen_file(enchantment_data, FILENAME)
    gen_file(enchantment_data, FILENAME, "json")


if __name__ == "__main__":
    main()
