# compass_facing.py
#
# <pep8-80 compliant>

# UNLICENSE
# This is free and unencumbered software released into the public domain.
# For more information, please refer to <http://unlicense.org>
#
# Authored in 2019 by Nicky Nym <https://github.com/nicky-nym>

from enum import Enum, unique

LEFT = 90    # degrees
RIGHT = 270  # degrees


@unique
class CompassFacing(Enum):
    """Compass bearings: North, South, East, and West."""
    NORTH = 0    # degrees
    EAST = 270   # degrees
    SOUTH = 180  # degrees
    WEST = 90    # degrees

    NORTHEAST = 315
    SOUTHEAST = 225
    SOUTHWEST = 135
    NORTHWEST = 45

    def opposite():
        return CompassFacing(360 - self.value)
