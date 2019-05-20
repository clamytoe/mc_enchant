import pandas as pd
import pytest
from bs4.element import Tag

from mc_enchant import clean_up_names, enchants_permitted, gen_df


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
