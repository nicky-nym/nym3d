# cottage.py
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

# Feet: all measurements are in feet

PARCEL_DY = 50
PARCEL_X0_NORTH = -232.72
PARCEL_X0_SOUTH = -224.15
PARCEL = [(PARCEL_X0_SOUTH, 0, 0),
          (PARCEL_X0_NORTH, PARCEL_DY, 0),
          (0, PARCEL_DY, 0),
          (0, 0, 0)]

FENCE_HEIGHT = 6
FENCE_LINE = [(-52, 0, 0),
              (PARCEL_X0_SOUTH, 0, 0),
              (PARCEL_X0_NORTH, PARCEL_DY, 0),
              (0, PARCEL_DY, 0)]

DRIVEWAY = [(-194, 2, 0.01),
            (-194, 13, 0.01),
            (-181, 13, 0.01),
            (-181, 23, 0.01),
            (-165, 23, 0.01),
            (-165, 13, 0.01),
            (-0, 13, 0.01),
            (-0, 2, 0.01)]

DOORPATH = [(-15.5, 31.75, 0.01),
            (-0, 31.75, 0.01),
            (-0, 26.75, 0.01),
            (-15.5, 26.75, 0.01)]

GARAGE_HEIGHT = 8
GARAGE_SPEC = [((-185, 23, 0), []),
               ((-185, 44, 0), []),
               ((-161, 44, 0), []),
               ((-161, 23, 0), [])]
GARAGE = [entry[0] for entry in GARAGE_SPEC]

ADU_SPEC = [((-154, 23, 0), []),
            ((-154, 44, 0), []),
            ((-124, 44, 0), []),
            ((-124, 23, 0), [])]
ADU = [entry[0] for entry in ADU_SPEC]

ADU_DOORPATH = [(-160, 13, 0),
                (-160, 36, 0),
                (-155, 36, 0),
                (-155, 13, 0)]

# exterior walls (0.5 feet thick), clockwise from the back wall of the house
KITCHEN_WINDOWS = [yzwh2rect(3.958, 2.583, 5.750, 4.083)]
DINING_ROOM_WINDOWS = [yzwh2rect(4.166, 2.0, 2.250, 6.400),
                       yzwh2rect(7.083, 2.0, 2.250, 6.400)]
BAY_WINDOW_NORTHEAST = [yzwh2rect(1.000, 2.0, 2.750, 6.400)]
BAY_WINDOW_EAST = [yzwh2rect(1.525, 2.0, 4.333, 6.400)]
BAY_WINDOW_SOUTHEAST = [yzwh2rect(1.000, 2.0, 2.750, 6.400)]
PORCH_WINDOWS = [yzwh2rect(0.875, 0, 3.0, 7.0),       # door
                 yzwh2rect(07.583, 2.0, 2.250, 6.400),
                 yzwh2rect(10.500, 2.0, 2.250, 6.400)]
OFFICE_WINDOW = [yzwh2rect(6.916, 2.0, 2.250, 6.400)]
BED_AND_BATH_WINDOWS = [yzwh2rect(3.875, 2.166, 3.666, 6.250),   # bedroom
                        yzwh2rect(12.708, 4.166, 2.375, 3.083)]  # bathroom
HOUSE_SPEC = [((-57.792, 44.542, 0), KITCHEN_WINDOWS),
              ((-44.333, 44.542, 0), []),
              ((-44.333, 47, 0), DINING_ROOM_WINDOWS),
              ((-19.375, 47, 0), BAY_WINDOW_NORTHEAST),
              ((-16, 43.65, 0), BAY_WINDOW_EAST),
              ((-16, 36.1, 0), BAY_WINDOW_SOUTHEAST),
              ((-19.375, 32.75, 0), []),
              ((-25.792, 32.75, 0), PORCH_WINDOWS),
              ((-25.792, 14.75, 0), OFFICE_WINDOW),
              ((-41.167, 14.75, 0), []),
              ((-41.167, 16.75, 0), BED_AND_BATH_WINDOWS),
              ((-57.792, 16.75, 0), [])]
HOUSE = [entry[0] for entry in HOUSE_SPEC]
HOUSE_WINDOWS = [(i, entry[1]) for i, entry in enumerate(HOUSE_SPEC)]

WEST_WINDOWS = [yzwh2rect(1.500, 4.500, 1.750, 2.083),   # half-bath
                yzwh2rect(5.104, 2.583, 5.750, 4.083),   # laundry
                yzwh2rect(11.354, 0, 2.666, 6.666),      # door
                yzwh2rect(18.875, 4.333, 3.750, 2.083)]  # kitchen
ADDON_SPEC = [((-63.75, 43.625, 0), []),
              ((-57.792, 43.625, 0), []),
              ((-57.792, 17.833, 0), []),
              ((-63.75, 17.833, 0), WEST_WINDOWS)]

ADDON = [entry[0] for entry in ADDON_SPEC]
ADDON_WINDOWS = [(i, entry[1]) for i, entry in enumerate(ADDON_SPEC)]

ATTIC = [nudge(HOUSE[0], dx=-1, dy=1),
         nudge(HOUSE[1], dx=-1, dy=1),
         nudge(HOUSE[2], dx=-1, dy=1),
         nudge((HOUSE[4][X], HOUSE[3][Y], 0), dx=1, dy=1),
         nudge((HOUSE[5][X], HOUSE[6][Y], 0), dx=1, dy=-1),
         nudge(HOUSE[7], dx=1, dy=-1),
         nudge(HOUSE[8], dx=1, dy=-1),
         nudge(HOUSE[9], dx=-1, dy=-1),
         nudge(HOUSE[10], dx=-1, dy=-1),
         nudge(HOUSE[11], dx=-1, dy=-1)]
PORCH = [(-25.792, 32.75, 0),
         (-25.792 + 5.333, 32.75, 0),
         (-25.792 + 5.333, 32.75 - 17.083, 0),
         (-25.792, 32.75 - 17.083, 0)]
NUM_STAIR_STEPS = 5
STAIR_X = -25.792 + 5.333 + NUM_STAIR_STEPS
STAIR = [(STAIR_X, 31.75, 0),
         (STAIR_X + 1, 31.75, 0),
         (STAIR_X + 1, 26.75, 0),
         (STAIR_X, 26.75, 0)]

D1 = (ATTIC[0][Y] - ATTIC[9][Y]) / 2.0
PEAK_BACK = (HOUSE[0][X]+D1, HOUSE[0][Y]-D1, D1)
PEAK_BACK_INSET = (ATTIC[5][X] - D1, PEAK_BACK[Y], D1)

D2 = (ATTIC[5][X] - ATTIC[1][X]) / 2.0
PEAK_NORTH = (ATTIC[2][X] + D2, ATTIC[2][Y] - D2, D2)
PEAK_NORTH_INSET = (PEAK_NORTH[X], PEAK_NORTH[Y] - (ATTIC[2][Y] - ATTIC[1][Y]), D2)

D3 = (ATTIC[6][X] - ATTIC[7][X]) / 2.0
PEAK_OFFICE = (ATTIC[7][X] + D3, ATTIC[7][Y] + D3, D3)
PEAK_OFFICE_INSET = (PEAK_OFFICE[X], PEAK_OFFICE[Y] + (ATTIC[8][Y] - ATTIC[7][Y]), D3)

D4 = (ATTIC[3][Y] - ATTIC[4][Y]) / 2.0
PEAK_FRONT = (ATTIC[3][X], (ATTIC[3][Y] + ATTIC[4][Y])/2.0, D4)
PEAK_FRONT_INSET = (ATTIC[5][X] - D4, PEAK_FRONT[Y], D4)

# TODO: determine accurate locations
PEAK_DORMER = (ATTIC[5][X] - 1, PEAK_OFFICE_INSET[Y] + 1.5, PEAK_OFFICE_INSET[Z] - 1)
PEAK_DORMER_INSET = (ATTIC[5][X] - 7, PEAK_DORMER[Y], PEAK_DORMER[Z])
DORMER_NW = nudge(PEAK_DORMER_INSET, dx=2.5, dy=2.5, dz=-2.5)
DORMER_SW = nudge(PEAK_DORMER_INSET, dx=2.5, dy=-2.5, dz=-2.5)
DORMER_NE = (PEAK_DORMER[X], DORMER_NW[Y], DORMER_NW[Z])
DORMER_SE = (PEAK_DORMER[X], DORMER_SW[Y], DORMER_SW[Z])

PORCH_ROOF = [[ADDON[0], xy2xyz(ADDON[1], 2), xy2xyz(ADDON[2], 2), ADDON[3]],
              [xy2xyz(PORCH[0], 2), PORCH[1], PORCH[2], xy2xyz(PORCH[3], 2)]
              ]

ROOF = [[PEAK_BACK, ATTIC[0], ATTIC[9]],
        [PEAK_NORTH_INSET, PEAK_BACK_INSET, PEAK_BACK, ATTIC[0], ATTIC[1]],
        [PEAK_NORTH, PEAK_NORTH_INSET, ATTIC[1], ATTIC[2]],
        [PEAK_FRONT, PEAK_FRONT_INSET, PEAK_NORTH, ATTIC[2], ATTIC[3]],
        [PEAK_FRONT, ATTIC[3], ATTIC[4]],
        [PEAK_FRONT_INSET, PEAK_FRONT, ATTIC[4], ATTIC[5]],
        [PEAK_OFFICE, PEAK_OFFICE_INSET, PEAK_BACK_INSET, PEAK_NORTH_INSET, PEAK_NORTH, PEAK_FRONT_INSET, ATTIC[5], ATTIC[6]],
        [PEAK_OFFICE, ATTIC[6], ATTIC[7]],
        [PEAK_OFFICE_INSET, PEAK_OFFICE, ATTIC[7], ATTIC[8]],
        [PEAK_BACK, PEAK_BACK_INSET, PEAK_OFFICE_INSET, ATTIC[8], ATTIC[9]],
        [PEAK_DORMER, PEAK_DORMER_INSET, DORMER_NW, DORMER_NE],
        [PEAK_DORMER_INSET, PEAK_DORMER, DORMER_SE, DORMER_SW]
        ]

CHIMNEY_HEIGHT = 16
CHIMNEY_XYZ = nudge(PEAK_BACK, dx=-1.5, dy=3, dz=-PEAK_BACK[Z])
CHIMNEY = [CHIMNEY_XYZ,
           nudge(CHIMNEY_XYZ, dx=0.0, dy=2.95),
           nudge(CHIMNEY_XYZ, dx=2.1, dy=2.95),
           nudge(CHIMNEY_XYZ, dx=2.1, dy=0.00)]

CRAWL_SPACE_HEIGHT = 4
GROUND_FLOOR_HEIGHT = 11.5
ADDON_HEIGHT = 8


class Cottage:
    """Cottage objects know how to describe a Queen Anne cottage."""

    def __init__(self, plato: Plato):
        self._plato = plato

    def add_street(self, count: int=5):
        """Tell plato about the street the cottages are on."""
        self._plato.hurry(count > 1)

        STREET_DX = 15
        STREET_DY = count * PARCEL_DY

        SIDEWALK_WIDTH = 6
        SIDEWALK = [(0, 0, 0),
                    (SIDEWALK_WIDTH, 0, 0),
                    (SIDEWALK_WIDTH, STREET_DY, 0),
                    (0, STREET_DY, 0)]

        CURB_HEIGHT = 0.4
        STREET = [(SIDEWALK_WIDTH, 0, -CURB_HEIGHT),
                  (SIDEWALK_WIDTH, STREET_DY, -CURB_HEIGHT),
                  (SIDEWALK_WIDTH + STREET_DX, STREET_DY, -CURB_HEIGHT),
                  (SIDEWALK_WIDTH + STREET_DX, 0, -CURB_HEIGHT)]

        self._plato.add_place(Place.WALKWAY, shape=SIDEWALK)
        CURB = [(SIDEWALK_WIDTH, 0, -CURB_HEIGHT),
                (SIDEWALK_WIDTH, STREET_DY, -CURB_HEIGHT)]
        self._plato.add_wall(shape=CURB, height=CURB_HEIGHT, cap=False)
        self._plato.add_place(Place.STREET, shape=STREET)
        self._plato.goto(x=STREET_DX+SIDEWALK_WIDTH)

        xNorth = 0  # TODO: ???
        xSouth = 0  # TODO: ???

        for i in range(count):
            y = i * PARCEL_DY

            self.add_parcel(x=xNorth, y=y, facing=Facing.NORTH)
            self.add_cottage(x=xNorth, y=y, facing=Facing.NORTH)
            self.add_garage_and_adu(x=xNorth, y=y, facing=Facing.NORTH)

            # self.add_parcel(x=xSouth, y=y, facing=Facing.SOUTH)
            # self.add_cottage(x=xSouth, y=y, facing=Facing.SOUTH)
            # self.add_garage_and_adu(x=xSouth, y=y, facing=Facing.SOUTH)

    def add_stairs(self, x: int=0, y: int=0, facing: Facing=Facing.NORTH):
        for i in range(NUM_STAIR_STEPS):
            z = CRAWL_SPACE_HEIGHT / NUM_STAIR_STEPS * i
            x -= 1
            self._plato.goto(x=x, y=y, z=z, facing=facing)
            self._plato.add(Place.WALKWAY, shape=STAIR, nuance=True)

    def add_parcel(self, x: int=0, y: int=0, facing: Facing=Facing.NORTH):
        """Tell plato about the yard, fence, sidewalk, etc."""
        self._plato.goto(x=x, y=y, z=0, facing=facing)
        self._plato.add_place(Place.PARCEL, shape=PARCEL)
        self._plato.add_wall(shape=FENCE_LINE, height=FENCE_HEIGHT, cap=False)
        self._plato.add_place(Place.WALKWAY, shape=DOORPATH, nuance=True)
        self._plato.add_place(Place.STREET, shape=DRIVEWAY, nuance=True)
        self.add_stairs(x=x, y=y, facing=facing)
        return self

    def add_garage_and_adu(self, x: int=0, y: int=0, facing: Facing=Facing.NORTH):
        self._plato.goto(x=x, y=y, z=0, facing=facing)
        self._plato.add_place(Place.BARE, shape=GARAGE, wall=GARAGE_HEIGHT, nuance=True)
        self._plato.add_place(Place.ROOM, shape=ADU, wall=GARAGE_HEIGHT, nuance=True)
        self._plato.add_place(Place.WALKWAY, shape=ADU_DOORPATH, nuance=True)
        return self

    def add_cottage(self, x: int=0, y: int=0, facing: Facing=Facing.NORTH):
        """Tell plato about the floors, walls, roof, etc."""
        plato = self._plato

        # Crawl space
        plato.goto(x=x, y=y, z=0, facing=facing)
        plato.add_place(Place.BARE, shape=HOUSE, wall=CRAWL_SPACE_HEIGHT)
        plato.add_place(Place.BARE, shape=ADDON, wall=CRAWL_SPACE_HEIGHT)
        plato.add_place(Place.BARE, shape=PORCH, wall=CRAWL_SPACE_HEIGHT)

        # Main floor
        plato.goto(x=x, y=y, z=CRAWL_SPACE_HEIGHT, facing=facing)
        plato.add_place(Place.ROOM, shape=HOUSE, wall=GROUND_FLOOR_HEIGHT, openings=HOUSE_WINDOWS)
        plato.add_place(Place.BARE, shape=PORCH)
        plato.add_place(Place.ROOM, shape=ADDON, wall=ADDON_HEIGHT, openings=ADDON_WINDOWS)

        # Attic
        ATTIC_ELEVATION = GROUND_FLOOR_HEIGHT + CRAWL_SPACE_HEIGHT
        plato.goto(x=x, y=y, z=ATTIC_ELEVATION, facing=facing)
        plato.add_place(Place.BARE, shape=ATTIC)
        for roof in ROOF:
            plato.add(Place.ROOF, shape=roof)
        plato.add_wall(shape=CHIMNEY, height=CHIMNEY_HEIGHT, nuance=True)

        # Porch roofs
        PORCH_TOP_ELEVATION = ADDON_HEIGHT + CRAWL_SPACE_HEIGHT
        plato.goto(x=x, y=y, z=PORCH_TOP_ELEVATION, facing=facing)
        for roof in PORCH_ROOF:
            plato.add(Place.ROOF, shape=roof)

        return self
