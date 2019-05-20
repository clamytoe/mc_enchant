from os import path
from urllib.request import urlretrieve

import pandas as pd
from bs4 import BeautifulSoup as Soup

FILE = path.join("/tmp", "enchantment_list_pc.html")
OUTFILE = "enchantments.csv"
URL = "https://www.digminecraft.com/lists/enchantment_list_pc.php"


def clean_up_names(table):
    unwanted = (".png", "_sm", "iron_", "enchanted_")
    valid = []

    for img in table.find_all("img"):
        item_types = img["data-src"].split("/")[-1]
        if "fishing_rod" in item_types:
            item_types = item_types.replace("fishing_rod", "fishingrod")

        for s in unwanted:
            if s in item_types:
                item_types = item_types.replace(s, "")

        item_types = item_types.split("_")
        item_types = [
            "fishing_rod" if item == "fishingrod" else item for item in item_types
        ]
        valid.append(" ".join(item_types))

    return valid


def enchants_permitted():
    with open(FILE) as file:
        soup = Soup(file, "html.parser")

    table = soup.find("table", {"id": "minecraft_items"})
    return clean_up_names(table)


def gen_df(permitted):
    raw_data = pd.read_html(FILE)[0]
    names = raw_data["Enchantment(Minecraft ID Name)"].apply(
        lambda name: name.split("(")[0]
    )
    id_names = raw_data["Enchantment(Minecraft ID Name)"].apply(
        lambda name: name.split("(")[1].replace(")", "")
    )
    data = pd.DataFrame(
        dict(
            id_name=id_names,
            name=names,
            max_level=raw_data["Max Level"],
            description=raw_data["Description"],
            items=raw_data["Items"],
        )
    )
    data["items"] = pd.Series(permitted)
    data.set_index("id_name", inplace=True)

    return data


def main():
    if not path.isfile(FILE):
        urlretrieve(URL, FILE)

    permitted = enchants_permitted()
    enchantment_data = gen_df(permitted)
    enchantment_data.to_csv(OUTFILE)


if __name__ == "__main__":
    main()
