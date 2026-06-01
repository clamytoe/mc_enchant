import pytest

from mc_enchant.enchantments_data import ENCHANTMENTS
from mc_enchant.app import build_item_index, detect_conflicts


@pytest.fixture
def item_index():
    return build_item_index({})


def test_item_index_filters_correct_enchantments(item_index):
    # Elytra should only have unbreaking + mending
    ench_ids = {e["id_name"] for e in item_index["elytra"]}
    assert ench_ids == {"unbreaking", "mending"}


def test_enchantments_are_sorted_by_name(item_index):
    ench_list = item_index["sword"]
    names = [e["name"] for e in ench_list]
    assert names == sorted(names)


def test_conflict_detection_silk_touch_vs_fortune():
    conflicts = detect_conflicts(["silk_touch", "fortune"])
    assert ("silk_touch", "fortune") in conflicts or ("fortune", "silk_touch") in conflicts


def test_conflict_detection_sharpness_vs_smite():
    conflicts = detect_conflicts(["sharpness", "smite"])
    assert conflicts != []


def test_no_conflict_for_valid_combo():
    conflicts = detect_conflicts(["unbreaking", "mending"])
    assert conflicts == []


def test_auto_max_level_selection():
    # Simulate the logic your code uses: max_level is taken from ENCHANTMENTS
    ench = ENCHANTMENTS["sharpness"]
    assert ench["max"] == 5


def test_all_enchantments_have_valid_max_levels():
    for ench_id, ench_data in ENCHANTMENTS.items():
        assert isinstance(ench_data["max"], int)
        assert ench_data["max"] >= 1


def test_items_only_show_enchantments_they_support(item_index):
    # Pickaxe should NOT show bow enchantments
    pickaxe_enchants = {e["id_name"] for e in item_index["pickaxe"]}
    assert "power" not in pickaxe_enchants
    assert "punch" not in pickaxe_enchants
    assert "flame" not in pickaxe_enchants


def test_trident_only_shows_trident_enchantments(item_index):
    ench_ids = {e["id_name"] for e in item_index["trident"]}
    assert ench_ids == {"impaling", "loyalty", "riptide", "channeling", "unbreaking", "mending"}
