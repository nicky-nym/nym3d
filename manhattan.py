# manhattan.py
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
BLOCK_DX = 600
BLOCK_DY = 200

BUILDINGS_PER_STREET = 2
BUILDINGS_PER_AVENUE = 6

BUILDING_DX = BLOCK_DX / BUILDINGS_PER_AVENUE
BUILDING_DY = BLOCK_DY / BUILDINGS_PER_STREET

SIDEWALK_WIDTH_STREETS = 16
SIDEWALK_WIDTH_AVENUES = 20
STREET_WIDTH = 32
AVENUE_WIDTH = 60
HALF_STREET = 32 / 2
HALF_AVENUE = 60 / 2

STORY_HEIGHT = 10

BUILDING = [(0, 0, 0),
            (BUILDING_DX, 0, 0),
            (BUILDING_DX, BUILDING_DY, 0),
            (0, BUILDING_DY, 0)]
INTERSECTION = [(0, 0, 0),
                (HALF_AVENUE, 0, 0),
                (HALF_AVENUE, HALF_STREET, 0),
                (0, HALF_STREET, 0)]
STREET = [(0, 0, 0),
          (BLOCK_DX, 0, 0),
          (BLOCK_DX, HALF_STREET, 0),
          (0, HALF_STREET, 0)]
AVENUE = [(0, 0, 0),
          (HALF_AVENUE, 0, 0),
          (HALF_AVENUE, BLOCK_DY, 0),
          (0, BLOCK_DY, 0)]
SIDEWALK_FOR_STREET = [(0, 0, 0),
                       (BLOCK_DX, 0, 0),
                       (BLOCK_DX, SIDEWALK_WIDTH_STREETS, 0),
                       (0, SIDEWALK_WIDTH_STREETS, 0)]
SIDEWALK_FOR_AVENUE = [(0, 0, 0),
                       (0, BLOCK_DY, 0),
                       (SIDEWALK_WIDTH_AVENUES, BLOCK_DY, 0),
                       (SIDEWALK_WIDTH_AVENUES, 0, 0)]
BLOCK = [(0, 0, 0),
         (BLOCK_DX, 0, 0),
         (BLOCK_DX, BLOCK_DY, 0),
         (0, BLOCK_DY, 0)]
REPEAT_DX = BLOCK_DX + AVENUE_WIDTH + (SIDEWALK_WIDTH_AVENUES * 2)
REPEAT_DY = BLOCK_DY + STREET_WIDTH + (SIDEWALK_WIDTH_STREETS * 2)


class Manhattan:
    """Manhattan objects know how to describe the city blocks in New York."""

    def __init__(self, plato: Plato):
        self._plato = plato

    def add_place(self,
                  place: Place,
                  *,
                  shape: Sequence[Xyz],
                  x: Num=0,
                  y: Num=0,
                  z: Num=0,
                  dx: Num=0,
                  dy: Num=0,
                  wall: Num=0,
                  openings: Sequence[Tuple]=[]):
        self._plato.goto(x=x+dx, y=y+dy, z=z)
        self._plato.add_place(place=place, shape=shape, wall=wall, openings=openings)

    def add_building_at(self, x: Num=0, y: Num=0):
        # print("  NYC building: {:,.0f}, {:,.0f}".format(x, y))
        self.add_place(Place.PARCEL, shape=BUILDING, x=x, y=y, z=0)
        num_floors = randint(4, 60)
        story_height = randint(9, 12)
        for i in range(num_floors):
            z = i * story_height
            self.add_place(Place.ROOM, shape=BUILDING, x=x, y=y, z=z, wall=story_height, openings=[])
        self.add_place(Place.ROOF, shape=BUILDING, x=x, y=y, z=z+story_height)

    def add_block(self, row: Num=0, col: Num=0):
        x = row * REPEAT_DX
        y = col * REPEAT_DY

        for bx in range(BUILDINGS_PER_AVENUE):
            for by in range(BUILDINGS_PER_STREET):
                x0 = HALF_AVENUE + SIDEWALK_WIDTH_AVENUES + x
                y0 = HALF_STREET + SIDEWALK_WIDTH_STREETS + y
                dx = bx * BUILDING_DX
                dy = by * BUILDING_DY
                self.add_building_at(dx + x0, dy + y0)

        self.add_place(Place.STREET, shape=STREET, x=x, y=y, dx=HALF_AVENUE+SIDEWALK_WIDTH_AVENUES)
        self.add_place(Place.STREET, shape=STREET, x=x, y=y, dx=HALF_AVENUE+SIDEWALK_WIDTH_AVENUES, dy=HALF_STREET+(SIDEWALK_WIDTH_STREETS*2)+BLOCK_DY)
        self.add_place(Place.STREET, shape=AVENUE, x=x, y=y, dy=HALF_STREET+SIDEWALK_WIDTH_STREETS)
        self.add_place(Place.STREET, shape=AVENUE, x=x, y=y, dx=HALF_AVENUE+(SIDEWALK_WIDTH_AVENUES*2)+BLOCK_DX, dy=HALF_STREET+SIDEWALK_WIDTH_STREETS)

        self.add_place(Place.STREET, shape=INTERSECTION, x=x, y=y)
        self.add_place(Place.STREET, shape=INTERSECTION, x=x, y=y, dx=HALF_AVENUE+(SIDEWALK_WIDTH_AVENUES*2)+BLOCK_DX)
        self.add_place(Place.STREET, shape=INTERSECTION, x=x, y=y, dy=HALF_STREET+(SIDEWALK_WIDTH_STREETS*2)+BLOCK_DY)
        self.add_place(Place.STREET, shape=INTERSECTION, x=x, y=y, dx=HALF_AVENUE+(SIDEWALK_WIDTH_AVENUES*2)+BLOCK_DX, dy=HALF_STREET+(SIDEWALK_WIDTH_STREETS*2)+BLOCK_DY)

        self.add_place(Place.WALKWAY, shape=SIDEWALK_FOR_STREET, x=x, y=y, dx=HALF_AVENUE+SIDEWALK_WIDTH_AVENUES, dy=HALF_STREET)
        self.add_place(Place.WALKWAY, shape=SIDEWALK_FOR_STREET, x=x, y=y, dx=HALF_AVENUE+SIDEWALK_WIDTH_AVENUES, dy=HALF_STREET+SIDEWALK_WIDTH_STREETS+BLOCK_DY)
        self.add_place(Place.WALKWAY, shape=SIDEWALK_FOR_AVENUE, x=x, y=y, dx=HALF_AVENUE, dy=HALF_STREET+SIDEWALK_WIDTH_STREETS)
        self.add_place(Place.WALKWAY, shape=SIDEWALK_FOR_AVENUE, x=x, y=y, dx=HALF_AVENUE+SIDEWALK_WIDTH_AVENUES+BLOCK_DX, dy=HALF_STREET+SIDEWALK_WIDTH_STREETS)

        return self

    def add_blocks(self, num_rows: int=2, num_cols: int=2):
        for row in range(num_rows):
            for col in range(num_cols):
                self.add_block(row, col)
        return self
