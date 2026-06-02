from typing import Dict, List

from .enchantments_data import ENCHANTMENTS

def build_item_index(_=None):
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
