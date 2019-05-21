import pandas as pd
from bs4 import BeautifulSoup as Soup


def clean_up_names(item_names):
    unwanted = (".png", "_sm", "iron_", "enchanted_")

    if "fishing_rod" in item_names:
        item_names = item_names.replace("fishing_rod", "fishingrod")

    for chars in unwanted:
        if chars in item_names:
            item_names = item_names.replace(chars, "")

    item_names = item_names.split("_")
    item_names = [
        "fishing_rod" if item == "fishingrod" else item for item in item_names
    ]

    return " ".join(item_names)


def enchants_permitted(filename):
    with open(filename) as file:
        soup = Soup(file, "html.parser")

    table = soup.find("table", {"id": "minecraft_items"})
    valid = [
        clean_up_names(img["data-src"].split("/")[-1]) for img in table.find_all("img")
    ]

    return valid


def gen_df(filename, items=None):
    raw_data = pd.read_html(filename)[0]
    title = "Enchantment(Minecraft ID Name)"
    id_names, names = split_title(raw_data, title)
    data = pd.DataFrame(
        dict(
            id_name=id_names,
            name=names,
            max_level=raw_data["Max Level"],
            description=raw_data["Description"],
            items=raw_data["Items"],
        )
    )
    if items:
        data["items"] = pd.Series(items)
    data.set_index("id_name", inplace=True)

    return data


def gen_file(df, output_format="csv"):
    file = OUTPUT[output_format]
    df.to_json(file)


def split_title(df, title):
    names = df[title].apply(lambda name: name.split("(")[0])
    id_names = df[title].apply(lambda name: name.split("(")[1].replace(")", ""))
    return id_names, names
