import argparse

from .index import build_item_index
from .ui import choose_item, choose_material, choose_enchantments, choose_levels, choose_custom_name
from .conflicts import detect_conflicts
from .command_builder import build_give_command

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manual-levels", action="store_true")
    args = parser.parse_args()

    item_index = build_item_index()

    item_key = choose_item(item_index)
    material = choose_material(item_key)
    full_item_key = f"{material}_{item_key}" if material else item_key

    while True:
        chosen = choose_enchantments(item_key, item_index)
        conflicts = detect_conflicts([e["id_name"] for e in chosen])
        if not conflicts:
            break
        print("\n⚠️  Conflicts detected:")
        for a, b in conflicts:
            print(f" - {a} conflicts with {b}")
        print()

    levels = choose_levels(chosen) if args.manual_levels else {
        e["id_name"]: e["max_level"] for e in chosen
    }

    custom_name = choose_custom_name()

    cmd = build_give_command(full_item_key, levels, custom_name)
    print("\nYour Minecraft command:\n")
    print(cmd)
    print()

def cli():
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled.")

if __name__ == "__main__":
    main()
