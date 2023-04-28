import pytest
from pokestarbot_c import xp_at, xp_for, calculate_level

from bot_data.minecraft_utils import py_xp_for, py_xp_at, py_calculate_level


def test_xp_at():
    assert xp_at(0) == 0
    assert xp_at(1) == 7
    assert xp_at(2) == 16
    assert isinstance(xp_at(5), int)


def test_xp_for():
    assert xp_for(0) == 0
    assert xp_for(1) == 7
    assert xp_for(2) == 9
    assert isinstance(xp_for(5), int)


def test_xp_at_dependence():
    assert xp_at(30) == (xp_at(29) + xp_for(30))


def test_calculate_level():
    assert calculate_level(0) == 0
    assert calculate_level(1) == 0
    assert calculate_level(7) == 1
    assert calculate_level(16) == 2
    assert isinstance(calculate_level(1395), int)
    assert isinstance(calculate_level(1396), int)


@pytest.mark.parametrize("level", range(100))
def test_xp_at_c_compatibility(level: int):
    native = xp_at(level)
    python = py_xp_at(level)
    assert native == python and type(native) == type(python)


@pytest.mark.parametrize("level", range(100))
def test_xp_for_c_compatibility(level: int):
    native = xp_for(level)
    python = py_xp_for(level)
    assert native == python and type(native) == type(python)


@pytest.mark.parametrize(
    "experience", {*range(10), *[xp_at(level) for level in range(100)]}
)
def test_calculate_level_c_compatibility(experience: int):
    assert calculate_level(experience) is py_calculate_level(experience)
