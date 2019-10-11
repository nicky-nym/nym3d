# xyz.py
#
# <pep8-80 compliant>

# UNLICENSE
# This is free and unencumbered software released into the public domain.
# For more information, please refer to <http://unlicense.org>
#
# Authored in 2019 by Nicky Nym <https://github.com/nicky-nym>

from typing import Tuple, Sequence, Iterable, Any, List, Optional, Union

# Data types
Num = Union[int, float]
Xyz = Sequence[Num]  # xyz = (7, 5, 9)
X = 0                # x = xyz[X]
Y = 1                # y = xyz[Y]
Z = 2                # z = xyz[Z]


def xy2xyz(xyz: Xyz, delta_z: Num=0):
    z = xyz[Z] + delta_z if len(xyz) > 2 else delta_z
    return (xyz[X], xyz[Y], z)


def yzwh2rect(y: Num, z: Num, width: Num, height: Num):
    # [(3, 2), (8, 2), (8, 6), (3, 6)] == yzwh2rect(3, 2, 5, 4)
    return [(y, z), (y+width, z), (y+width, z+height), (y, z+height)]


def nudge(xyz: Xyz, dx: Num=0, dy: Num=0, dz: Num=0, dxyz: Xyz=(0, 0, 0)):
    (x, y, z) = xyz
    (d_x, d_y, d_z) = dxyz
    return (x + dx + d_x, y + dy + d_y, z + dz + d_z)
