# wurster.py
#
# <pep8-80 compliant>

# UNLICENSE
# This is free and unencumbered software released into the public domain.
# For more information, please refer to <http://unlicense.org>
#
# Authored in 2019 by Nicky Nym <https://github.com/nicky-nym>

from typing import Tuple, Sequence, Iterable, Any, List, Optional, Union
from random import randint
from importlib import reload

from xyz import Num, Xyz, X, Y, Z, xy2xyz, yzwh2rect, nudge
from compass_facing import CompassFacing as Facing
from place import Place
from plato import Plato

# in feet
NUM_TOWER_FLOORS = 10
NUM_SOUTH_WING_FLOORS = 4
NUM_NORTH_WING_FLOORS = 3
NUM_CENTER_WING_FLOORS = 3

STORY_HEIGHT = 13
PARAPET_HEIGHT = 4

NUM_TOWER_CRENELS_X = 12
CRENEL_SPACING = 9.333

AWNING_SEPERATOR_DEPTH = 2.5
AWNING_DEPTH = 5
AWNING_LENGTH = 9

SOUTH_WING_DX = 170
SOUTH_WING_DY = 85
SOUTH_WING_X0 = 100
SOUTH_WING_Y0 = 140

SOUTH_WING = [(0, 0, 0),
              (SOUTH_WING_DX, 0, 0),
              (SOUTH_WING_DX, SOUTH_WING_DY, 0),
              (0, SOUTH_WING_DY, 0)]

CENTER_WING_DX = 53
CENTER_WING_DY = 116
CENTER_WING_X0 = SOUTH_WING_X0
CENTER_WING_Y0 = SOUTH_WING_Y0 + SOUTH_WING_DY

CENTER_WING = [(0, 0, 0),
               (CENTER_WING_DX, 0, 0),
               (CENTER_WING_DX, CENTER_WING_DY, 0),
               (0, CENTER_WING_DY, 0)]

NUM_SOUTH_WING_CRENELS_X = 18
NUM_SOUTH_WING_CRENELS_Y = 9

TOWER_DX = 110
TOWER_DY = 70
TOWER_X0 = CENTER_WING_X0 + CENTER_WING_DX
TOWER_Y0 = CENTER_WING_Y0 + CENTER_WING_DY

TOWER = [(0, 0, 0),
         (TOWER_DX, 0, 0),
         (TOWER_DX, TOWER_DY, 0),
         (0, TOWER_DY, 0)]

TOWER_EAST_DX = 29
TOWER_EAST_DY = 56
TOWER_EAST_X0 = TOWER_X0 + TOWER_DX
TOWER_EAST_Y0 = TOWER_Y0 + 5

TOWER_EAST = [(0, 0, 0),
              (TOWER_EAST_DX, 0, 0),
              (TOWER_EAST_DX, TOWER_EAST_DY, 0),
              (0, TOWER_EAST_DY, 0)]

TOWER_WEST_DX = 29
TOWER_WEST_DY = 44
TOWER_WEST_OFFSET_Y = 17
TOWER_WEST_X0 = TOWER_X0 - TOWER_EAST_DX
TOWER_WEST_Y0 = TOWER_Y0 + TOWER_WEST_OFFSET_Y

TOWER_WEST = [(0, 0, 0),
              (TOWER_WEST_DX, 0, 0),
              (TOWER_WEST_DX, TOWER_WEST_DY, 0),
              (0, TOWER_WEST_DY, 0)]

ATRIUM_DX = 22
ATRIUM_DY = 46
ATRIUM_OFFSET_Y = -7
ATRIUM_X0 = TOWER_WEST_X0 - ATRIUM_DX
ATRIUM_Y0 = TOWER_WEST_Y0 + ATRIUM_OFFSET_Y

NORTH_WING_DX = 227
NORTH_WING_DY = 113
NORTH_WING_X0 = SOUTH_WING_X0 - (NORTH_WING_DX - TOWER_DX - CENTER_WING_DX)
NORTH_WING_Y0 = TOWER_Y0

NORTH_WING = [(0, 0, 0),
              (NORTH_WING_DX - TOWER_DX, 0, 0),
              (NORTH_WING_DX - TOWER_DX, TOWER_WEST_OFFSET_Y, 0),
              (NORTH_WING_DX - TOWER_DX - TOWER_WEST_DX, TOWER_WEST_OFFSET_Y, 0),
              (NORTH_WING_DX - TOWER_DX - TOWER_WEST_DX, TOWER_WEST_OFFSET_Y + ATRIUM_OFFSET_Y, 0),
              (NORTH_WING_DX - TOWER_DX - TOWER_WEST_DX - ATRIUM_DX, TOWER_WEST_OFFSET_Y + ATRIUM_OFFSET_Y, 0),
              (NORTH_WING_DX - TOWER_DX - TOWER_WEST_DX - ATRIUM_DX, TOWER_WEST_OFFSET_Y + ATRIUM_OFFSET_Y + ATRIUM_DY, 0),
              (NORTH_WING_DX - TOWER_DX - TOWER_WEST_DX, TOWER_WEST_OFFSET_Y + ATRIUM_OFFSET_Y + ATRIUM_DY, 0),
              (NORTH_WING_DX - TOWER_DX - TOWER_WEST_DX, TOWER_WEST_OFFSET_Y + TOWER_WEST_DY, 0),
              (NORTH_WING_DX - TOWER_DX, TOWER_WEST_OFFSET_Y + TOWER_WEST_DY, 0),
              (NORTH_WING_DX - TOWER_DX, TOWER_DY, 0),
              (NORTH_WING_DX, TOWER_DY, 0),
              (NORTH_WING_DX, NORTH_WING_DY, 0),
              (0, NORTH_WING_DY, 0)]

NUM_NORTH_WING_CRENELS_Y = 12

NUM_CENTER_WING_CRENELS_Y = 12

FLOOR_TEN_BALCONY_DX = 10
FLOOR_TEN_BALCONY_DY = 23
FLOOR_TEN_BALCONY_X0 = TOWER_WEST_X0 - FLOOR_TEN_BALCONY_DX
FLOOR_TEN_BALCONY_Y0 = TOWER_WEST_Y0

FLOOR_TEN_BALCONY = [(0, 0, 0),
                     (FLOOR_TEN_BALCONY_DX, 0, 0),
                     (FLOOR_TEN_BALCONY_DX, FLOOR_TEN_BALCONY_DY, 0),
                     (0, FLOOR_TEN_BALCONY_DY, 0)]
PARCEL_DX = 360
PARCEL_DY = 540

PARCEL = [(0, 0, 0),
          (PARCEL_DX, 0, 0),
          (PARCEL_DX, PARCEL_DY, 0),
          (0, PARCEL_DY, 0)]


class Wurster:
    """Wurster objects know how to describe UC Berkeley's Wurster Hall."""

    def __init__(self, plato: Plato):
        self._plato = plato

    def add_parcel(self):
        self._plato.goto(x=0, y=0, z=0)
        self._plato.add_place(Place.PARCEL, shape=PARCEL)
        return self

    def add_south_wing(self):
        for i in range(NUM_SOUTH_WING_FLOORS):
            z = i * STORY_HEIGHT
            self._plato.goto(x=SOUTH_WING_X0, y=SOUTH_WING_Y0, z=z)
            self._plato.add_place(Place.ROOM, shape=SOUTH_WING, wall=STORY_HEIGHT)
        self._plato.goto(x=SOUTH_WING_X0, y=SOUTH_WING_Y0, z=z+STORY_HEIGHT)
        self._plato.add_place(Place.ROOF, shape=SOUTH_WING, wall=PARAPET_HEIGHT)
        return self

    def add_center_wing(self):
        for i in range(NUM_CENTER_WING_FLOORS):
            z = i * STORY_HEIGHT
            self._plato.goto(x=CENTER_WING_X0, y=CENTER_WING_Y0, z=z)
            self._plato.add_place(Place.ROOM, shape=CENTER_WING, wall=STORY_HEIGHT)
        self._plato.goto(x=CENTER_WING_X0, y=CENTER_WING_Y0, z=z+STORY_HEIGHT)
        self._plato.add_place(Place.ROOF, shape=CENTER_WING, wall=PARAPET_HEIGHT)
        return self

    def add_north_wing(self):
        for i in range(NUM_NORTH_WING_FLOORS):
            z = i * STORY_HEIGHT
            self._plato.goto(x=NORTH_WING_X0, y=NORTH_WING_Y0, z=z)
            self._plato.add_place(Place.ROOM, shape=NORTH_WING, wall=STORY_HEIGHT)
        self._plato.goto(x=NORTH_WING_X0, y=NORTH_WING_Y0, z=z+STORY_HEIGHT)
        self._plato.add_place(Place.ROOF, shape=NORTH_WING, wall=PARAPET_HEIGHT)
        return self

    def add_tower(self):
        for i in range(NUM_TOWER_FLOORS):
            z = i * STORY_HEIGHT

            self._plato.goto(x=TOWER_X0, y=TOWER_Y0, z=z)
            self._plato.add_place(Place.ROOM, shape=TOWER, wall=STORY_HEIGHT)

            self._plato.goto(x=TOWER_EAST_X0, y=TOWER_EAST_Y0, z=z)
            self._plato.add_place(Place.ROOM, shape=TOWER_EAST, wall=STORY_HEIGHT)

            self._plato.goto(x=TOWER_WEST_X0, y=TOWER_WEST_Y0, z=z)
            self._plato.add_place(Place.ROOM, shape=TOWER_WEST, wall=STORY_HEIGHT)

        self._plato.goto(x=TOWER_X0, y=TOWER_Y0, z=z+STORY_HEIGHT)
        self._plato.add_place(Place.ROOF, shape=TOWER, wall=PARAPET_HEIGHT)

        self._plato.goto(x=TOWER_EAST_X0, y=TOWER_EAST_Y0, z=z+STORY_HEIGHT)
        self._plato.add_place(Place.ROOF, shape=TOWER_EAST, wall=PARAPET_HEIGHT)

        z += STORY_HEIGHT
        self._plato.goto(x=TOWER_WEST_X0, y=TOWER_WEST_Y0, z=z)
        self._plato.add_place(Place.ROOM, shape=TOWER_WEST, wall=STORY_HEIGHT)

        self._plato.goto(x=FLOOR_TEN_BALCONY_X0, y=FLOOR_TEN_BALCONY_Y0, z=z)
        self._plato.add_place(Place.ROOM, shape=FLOOR_TEN_BALCONY, wall=PARAPET_HEIGHT)

        self._plato.goto(x=TOWER_WEST_X0, y=TOWER_WEST_Y0, z=z+STORY_HEIGHT)
        self._plato.add_place(Place.ROOF, shape=TOWER_WEST, wall=PARAPET_HEIGHT)

        return self

    def add_buildings(self, num: Num=1):
        self.add_parcel()
        self.add_south_wing()
        self.add_center_wing()
        self.add_north_wing()
        self.add_tower()
        return self
