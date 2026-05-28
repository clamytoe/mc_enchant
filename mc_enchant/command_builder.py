from __future__ import annotations
import json


def build_give_command(item_key, enchantments, custom_name=None):
    """
    Minecraft Java 1.21+ (26.x) data components syntax.
    """

    item_id = f"minecraft:{item_key.lower()}"

    components = []

    # minecraft:enchantments={"minecraft:flame":1,...}
    if enchantments:
        ench_pairs = ",".join(
            f'"minecraft:{eid}":{lvl}'
            for eid, lvl in enchantments.items()
        )
        components.append(f'minecraft:enchantments={{{ench_pairs}}}')

    # minecraft:custom_name='Mighty Bow'
    if custom_name:
        # No JSON, no escaping — literal string is correct for 26.1.2
        components.append(f"minecraft:custom_name='{custom_name}'")

    comp_str = ""
    if components:
        comp_str = "[" + ",".join(components) + "]"

    return f"/give @p {item_id}{comp_str} 1"
