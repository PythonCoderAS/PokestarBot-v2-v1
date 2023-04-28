"""This package will export functions to calculte XP values. There are pure Python
implementations and C implementations. To improve speed, since the first 30-or-so
levels require a different formula, they have been precalculated."""
import functools

xp_for_precalculated = {
    0: 0,
    1: 7,
    2: 9,
    3: 11,
    4: 13,
    5: 15,
    6: 17,
    7: 19,
    8: 21,
    9: 23,
    10: 25,
    11: 27,
    12: 29,
    13: 31,
    14: 33,
    15: 35,
    16: 37,
    17: 42,
    18: 47,
    19: 52,
    20: 57,
    21: 62,
    22: 67,
    23: 72,
    24: 77,
    25: 82,
    26: 87,
    27: 92,
    28: 97,
    29: 102,
    30: 107,
}

xp_at_precalculated = {
    0: 0,
    1: 7,
    2: 16,
    3: 27,
    4: 40,
    5: 55,
    6: 72,
    7: 91,
    8: 112,
    9: 135,
    10: 160,
    11: 187,
    12: 216,
    13: 247,
    14: 280,
    15: 315,
    16: 352,
    17: 394,
    18: 441,
    19: 493,
    20: 550,
    21: 612,
    22: 679,
    23: 751,
    24: 828,
    25: 910,
    26: 997,
    27: 1089,
    28: 1186,
    29: 1288,
    30: 1395,
}


def _py_xp_for(level: int):
    """Precondition: level > 31"""
    return 9 * (level - 1) - 158


def _py_xp_at(level: int):
    """Precondition: level > 31"""
    return int(4.5 * pow(level, 2) - 162.5 * level + 2220)


@functools.lru_cache()
def py_calculate_level(experience: int) -> int:
    xp = experience
    current_level = 0
    while xp >= 0:
        current_level += 1
        xp -= py_xp_for(current_level)
    return current_level - 1


def py_xp_for(level: int):
    return xp_for_precalculated.get(level, _py_xp_for(level))


def py_xp_at(level: int):
    return xp_at_precalculated.get(level, _py_xp_at(level))


try:
    from pokestarbot_c import xp_at, xp_for, calculate_level
except (ModuleNotFoundError, ImportError):  # pragma: no cover
    xp_at = py_xp_at
    xp_for = py_xp_for
    calculate_level = py_calculate_level
