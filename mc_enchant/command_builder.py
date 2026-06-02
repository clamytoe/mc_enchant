from __future__ import annotations


def build_give_command(item_key, enchantments, custom_name):
    components = []

    if enchantments:
        ench_parts = [f'"minecraft:{k}":{v}' for k, v in enchantments.items()]
        components.append("minecraft:enchantments={" + ",".join(ench_parts) + "}")

    if custom_name:
        components.append(f"minecraft:custom_name='{custom_name}'")

    comp_str = ",".join(components)
    return f"/give @p minecraft:{item_key}[{comp_str}] 1"

