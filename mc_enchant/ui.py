from bullet import Bullet, Check, Input
from .data import MATERIAL_MAP, NO_MATERIAL_ITEMS
from .index import build_item_index

def pretty_item_name(key):
    return key.replace("_", " ").title()

def choose_item(item_index):
    choices = sorted(item_index.keys())
    labels = [pretty_item_name(c) for c in choices]
    cli = Bullet(prompt="Choose an item:", choices=labels, bullet="•", margin=2, pad_right=4)
    return dict(zip(labels, choices))[cli.launch()]

def choose_material(item_key):
    if item_key in NO_MATERIAL_ITEMS:
        return ""
    materials = MATERIAL_MAP.get(item_key, [""])
    cli = Bullet(prompt=f"Choose material for your {item_key}:", choices=materials, bullet="•", margin=2, pad_right=4)
    return cli.launch()

def choose_enchantments(item_key, item_index):
    enchants = sorted(item_index[item_key], key=lambda e: e["name"].lower())
    labels = [f"{e['name']} (max {e['max_level']})" for e in enchants]
    cli = Check(prompt=f"Choose enchantments for your {pretty_item_name(item_key)}:", choices=labels, check="✓", margin=2, pad_right=4)
    return [dict(zip(labels, enchants))[l] for l in cli.launch()]

def choose_levels(chosen):
    final = {}
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
        final[ench["id_name"]] = max(1, min(lvl, max_lvl))
    return final

def choose_custom_name():
    name = Input(prompt="Custom name (leave blank for none): ").launch().strip()
    return name or None
