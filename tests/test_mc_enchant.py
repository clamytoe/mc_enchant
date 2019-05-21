"""
test_mc_enchant.py

Tests for mc_enchant.
"""
import pytest

from mc_enchant import __version__
from mc_enchant.tools import clean_up_names


def test_version():
    assert __version__ == '0.1.0'


@pytest.mark.parametrize(
    "img, expected",
    [
        ("enchanted_iron_helmet.png", "helmet"),
        ("sword_axe_sm.png", "sword axe"),
        ("armor_sm.png", "armor"),
        ("enchanted_trident.png", "trident"),
        (
            "sword_chestplate_pickaxe_fishing_rod_sm.png",
            "sword chestplate pickaxe fishing_rod",
        ),
        ("enchanted_iron_boots.png", "boots"),
    ],
)
def test_clean_up_names(img, expected):
    assert clean_up_names(img) == expected
