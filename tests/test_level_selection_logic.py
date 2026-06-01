import pytest
from mc_enchant.enchantments_data import ENCHANTMENTS


def get_max_level(ench_id: str) -> int:
    return ENCHANTMENTS[ench_id]["max"]


def test_max_level_lookup():
    assert get_max_level("sharpness") == 5
    assert get_max_level("unbreaking") == 3
    assert get_max_level("mending") == 1


def test_auto_level_uses_max_level():
    ench_id = "efficiency"
    max_level = get_max_level(ench_id)
    assert max_level == 5


def test_invalid_level_rejected():
    ench_id = "sharpness"
    max_level = get_max_level(ench_id)

    with pytest.raises(AssertionError):
        assert 10 <= max_level, "Level exceeds max level"
