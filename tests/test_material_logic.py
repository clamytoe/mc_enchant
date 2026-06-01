import pytest

from mc_enchant.app import MATERIAL_MAP, NO_MATERIAL_ITEMS


def test_material_map_is_not_empty():
    assert isinstance(MATERIAL_MAP, dict)
    assert len(MATERIAL_MAP) > 0


def test_no_material_items_is_not_empty():
    assert isinstance(NO_MATERIAL_ITEMS, set)
    assert len(NO_MATERIAL_ITEMS) > 0


def test_items_do_not_overlap():
    # Items with no materials must have exactly [""] in MATERIAL_MAP
    for item in NO_MATERIAL_ITEMS:
        assert item in MATERIAL_MAP, f"{item} missing from MATERIAL_MAP"
        assert MATERIAL_MAP[item] == [""], f"{item} should have no materials"


def test_material_map_values_are_valid_lists():
    for item, materials in MATERIAL_MAP.items():
        assert isinstance(materials, list), f"{item} materials must be a list"

        # Items with no materials must have exactly [""] and be in NO_MATERIAL_ITEMS
        if item in NO_MATERIAL_ITEMS:
            assert materials == [""], f"{item} should have no materials"
            continue

        # Items with materials must not contain empty strings
        for mat in materials:
            assert isinstance(mat, str), f"Material '{mat}' for {item} must be a string"
            assert mat.strip() != "", f"Material '{mat}' for {item} cannot be empty"


def test_no_material_items_are_strings():
    for item in NO_MATERIAL_ITEMS:
        assert isinstance(item, str)
        assert item.strip() != ""


def test_items_with_materials_have_at_least_one_material():
    for item, materials in MATERIAL_MAP.items():
        assert len(materials) > 0, f"{item} must have at least one material"


def test_no_material_items_have_no_materials():
    for item in NO_MATERIAL_ITEMS:
        assert item in MATERIAL_MAP, f"{item} must appear in MATERIAL_MAP"
        assert MATERIAL_MAP[item] == [""], f"{item} should have exactly [''] as materials"


def test_only_no_material_items_have_empty_material():
    for item, materials in MATERIAL_MAP.items():
        if materials == [""]:
            assert item in NO_MATERIAL_ITEMS, f"{item} has [''] but is not in NO_MATERIAL_ITEMS"


def test_materials_are_lowercase_and_valid_identifiers():
    for item, materials in MATERIAL_MAP.items():
        for mat in materials:
            assert mat == mat.lower(), f"Material '{mat}' for {item} must be lowercase"
            assert " " not in mat, f"Material '{mat}' for {item} must not contain spaces"
