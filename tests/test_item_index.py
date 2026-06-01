import pytest

from mc_enchant.enchantments_data import ENCHANTMENTS
from mc_enchant.app import build_item_index, MATERIAL_MAP, NO_MATERIAL_ITEMS


@pytest.fixture
def item_index():
    # data arg is unused now, so pass empty dict
    return build_item_index({})


def test_item_index_is_not_empty(item_index):
    assert isinstance(item_index, dict)
    assert len(item_index) > 0


def test_every_item_in_index_is_known(item_index):
    all_known_items = set(MATERIAL_MAP.keys()) | set(NO_MATERIAL_ITEMS)

    for item in item_index.keys():
        assert item in all_known_items


def test_every_enchantment_appears_in_item_index(item_index):
    # Collect all enchantment IDs from the reverse mapping
    seen = set()
    for ench_list in item_index.values():
        for ench in ench_list:
            seen.add(ench["id_name"])

    # Every enchantment in ENCHANTMENTS must appear at least once
    missing = set(ENCHANTMENTS.keys()) - seen
    assert (
        len(missing) == 0
    ), f"These enchantments never appear in the item index: {missing}"


def test_enchantment_entries_have_required_fields(item_index):
    for ench_list in item_index.values():
        for ench in ench_list:
            assert "id_name" in ench
            assert "name" in ench
            assert "max_level" in ench


def test_item_index_matches_enchantment_data(item_index):
    # For each enchantment, ensure it appears under the correct items
    for ench_id, ench_data in ENCHANTMENTS.items():
        for item in ench_data["items"]:
            ench_list = item_index[item]
            ids = [e["id_name"] for e in ench_list]
            assert ench_id in ids, f"{ench_id} missing from item {item}"


def test_item_index_max_levels_are_correct(item_index):
    for item, ench_list in item_index.items():
        for ench in ench_list:
            expected = ENCHANTMENTS[ench["id_name"]]["max"]
            assert ench["max_level"] == expected


def test_item_index_name_formatting(item_index):
    # Ensure the dynamic name generation is correct
    for item, ench_list in item_index.items():
        for ench in ench_list:
            expected = ench["id_name"].replace("_", " ").title()
            assert ench["name"] == expected
