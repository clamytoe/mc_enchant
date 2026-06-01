import pytest
from mc_enchant.app import build_give_command


def test_custom_name_included():
    cmd = build_give_command(
        item_key="diamond_sword",
        enchantments={},
        custom_name="Excalibur",
    )
    assert "minecraft:custom_name='Excalibur'" in cmd


def test_custom_name_ignored_when_empty():
    cmd = build_give_command(
        item_key="diamond_sword",
        enchantments={"sharpness": 5},
        custom_name="",
    )
    assert "custom_name" not in cmd


def test_custom_name_with_spaces():
    cmd = build_give_command(
        item_key="bow",
        enchantments={},
        custom_name="The Long Shot",
    )
    assert "minecraft:custom_name='The Long Shot'" in cmd


def test_custom_name_with_quotes():
    cmd = build_give_command(
        item_key="bow",
        enchantments={},
        custom_name="Martin's Bow",
    )
    assert "Martin's Bow" in cmd  # no escaping done by builder
