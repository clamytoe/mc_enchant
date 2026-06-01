import pytest

from mc_enchant.enchantments_data import ENCHANTMENTS
from mc_enchant.app import MATERIAL_MAP, NO_MATERIAL_ITEMS


def test_enchantments_is_not_empty():
    assert isinstance(ENCHANTMENTS, dict)
    assert len(ENCHANTMENTS) > 0


def test_each_enchantment_has_required_fields():
    for ench_id, ench_data in ENCHANTMENTS.items():
        assert "max" in ench_data, f"{ench_id} missing 'max'"
        assert "items" in ench_data, f"{ench_id} missing 'items'"

        assert isinstance(ench_data["max"], int)
        assert ench_data["max"] >= 1

        assert isinstance(ench_data["items"], list)
        assert len(ench_data["items"]) > 0


def test_item_names_are_valid_strings():
    for ench_id, ench_data in ENCHANTMENTS.items():
        for item in ench_data["items"]:
            assert isinstance(item, str)
            assert item.strip() != ""


def test_items_exist_in_material_map_or_no_material_items():
    all_known_items = set(MATERIAL_MAP.keys()) | set(NO_MATERIAL_ITEMS)

    for ench_id, ench_data in ENCHANTMENTS.items():
        for item in ench_data["items"]:
            assert (
                item in all_known_items
            ), f"Unknown item '{item}' referenced in enchantment '{ench_id}'"


def test_material_map_items_are_valid():
    for item, materials in MATERIAL_MAP.items():
        assert isinstance(materials, list)
        for mat in materials:
            assert isinstance(mat, str)


def test_no_material_items_are_strings():
    for item in NO_MATERIAL_ITEMS:
        assert isinstance(item, str)
        assert item.strip() != ""


def test_every_item_is_used_by_at_least_one_enchantment():
    all_items = set(MATERIAL_MAP.keys()) | set(NO_MATERIAL_ITEMS)

    # Items that are valid but intentionally never appear in enchantment lists
    allowed_unused = {"book"}

    referenced_items = set()
    for ench_data in ENCHANTMENTS.values():
        referenced_items.update(ench_data["items"])

    unused = all_items - referenced_items - allowed_unused

    assert (
        len(unused) == 0
    ), f"These items exist but are not referenced by any enchantment: {unused}"

