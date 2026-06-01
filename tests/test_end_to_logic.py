import pytest
from mc_enchant.app import build_give_command, build_item_index


@pytest.fixture
def item_index():
    return build_item_index({})


def test_end_to_end_sword_with_enchants_and_name(item_index):
    enchants = {
        "sharpness": 5,
        "unbreaking": 3,
    }

    cmd = build_give_command(
        item_key="diamond_sword",
        enchantments=enchants,
        custom_name="Dragon Slayer",
    )

    assert cmd.startswith("/give @p minecraft:diamond_sword[")
    assert '"minecraft:sharpness":5' in cmd
    assert '"minecraft:unbreaking":3' in cmd
    assert "minecraft:custom_name='Dragon Slayer'" in cmd


def test_end_to_end_elytra_unbreaking(item_index):
    enchants = {"unbreaking": 3}

    cmd = build_give_command(
        item_key="elytra",
        enchantments=enchants,
        custom_name=None,
    )

    assert "/give @p minecraft:elytra" in cmd
    assert '"minecraft:unbreaking":3' in cmd
