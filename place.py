# place.py
#
# <pep8-80 compliant>

# UNLICENSE
# This is free and unencumbered software released into the public domain.
# For more information, please refer to <http://unlicense.org>
#
# Authored in 2019 by Nicky Nym <https://github.com/nicky-nym>

from enum import Enum, auto


class Place(Enum):
    """The types of places in our building model."""
    STREET = auto()
    BIKEPATH = auto()
    WALKWAY = auto()
    ROOM = auto()
    BARE = auto()
    PARCEL = auto()
    CANAL = auto()

    WALL = auto()
    ROOF = auto()
    DOOR = auto()
