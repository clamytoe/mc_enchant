import pytest

from mc_enchant.app import build_give_command


def test_basic_item_no_enchantments_no_name():
    cmd = build_give_command(
        item_key="diamond_sword",
        enchantments={},
        custom_name=None,
    )
    assert cmd == "/give @p minecraft:diamond_sword[] 1"


def test_single_enchantment():
    cmd = build_give_command(
        item_key="diamond_sword",
        enchantments={"sharpness": 5},
        custom_name=None,
    )
    assert cmd == (
        '/give @p minecraft:diamond_sword[minecraft:enchantments={"minecraft:sharpness":5}] 1'
    )


def test_multiple_enchantments_preserve_order():
    # Order must match the dict order (Python 3.7+ preserves insertion order)
    cmd = build_give_command(
        item_key="diamond_sword",
        enchantments={"sharpness": 5, "unbreaking": 3},
        custom_name=None,
    )
    assert (
        cmd
        == '/give @p minecraft:diamond_sword[minecraft:enchantments={"minecraft:sharpness":5,"minecraft:unbreaking":3}] 1'
    )


def test_custom_name_only():
    cmd = build_give_command(
        item_key="bow",
        enchantments={},
        custom_name="Mighty Bow",
    )
    assert cmd == "/give @p minecraft:bow[minecraft:custom_name='Mighty Bow'] 1"


def test_enchantments_and_custom_name():
    cmd = build_give_command(
        item_key="bow",
        enchantments={"power": 5, "flame": 1},
        custom_name="Burninator",
    )
    assert (
        cmd
        == '/give @p minecraft:bow[minecraft:enchantments={"minecraft:power":5,"minecraft:flame":1},minecraft:custom_name=\'Burninator\'] 1'
    )


def test_empty_custom_name_is_ignored():
    cmd = build_give_command(
        item_key="elytra",
        enchantments={"unbreaking": 3},
        custom_name="",
    )
    assert (
        cmd
        == '/give @p minecraft:elytra[minecraft:enchantments={"minecraft:unbreaking":3}] 1'
    )
