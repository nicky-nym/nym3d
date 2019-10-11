# merlon.py
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

# Distances, in feet
STORY_HEIGHT = 10
ROOFLINE = STORY_HEIGHT * 5
RAMP_WIDTH = 6
RAMP_LENGTH = 30
RAMP_HEIGHT = 2.5
TOWER_WIDTH = RAMP_LENGTH + 12
LANDING_WIDTH = RAMP_WIDTH + TOWER_WIDTH - RAMP_LENGTH
TOWER_SPACING = TOWER_WIDTH + RAMP_WIDTH

D1 = LANDING_WIDTH/2.0
D2 = RAMP_WIDTH/2.0
RAMP = [(+D2, D1, 0),
        (+D2, D1 + RAMP_LENGTH, RAMP_HEIGHT),
        (-D2, D1 + RAMP_LENGTH, RAMP_HEIGHT),
        (-D2, D1, 0)]
OCTAGONAL_LANDING = [(-D1, -D2, 0),
                     (-D2, -D1, 0),
                     (+D2, -D1, 0),
                     (+D1, -D2, 0),
                     (+D1, +D2, 0),
                     (+D2, +D1, 0),
                     (-D2, +D1, 0),
                     (-D1, +D2, 0)]
BASEMENT = [(D1, 0, 0),
            (D1, D2, 0),
            (D2, D1, 0),
            (0, D1, 0),
            (0, 2 * D1 + RAMP_LENGTH, 0),
            (2 * D1 + RAMP_LENGTH, 2 * D1 + RAMP_LENGTH, 0),
            (2 * D1 + RAMP_LENGTH, 0, 0)]
APARTMENT_WIDTH = D1 + RAMP_LENGTH + (D1+D2)/2

DOOR_HEIGHT = 6 + 8/12
DOORS = [yzwh2rect(1.2, 0.01, 3, DOOR_HEIGHT),
         yzwh2rect(4.285, 0.01, 3, DOOR_HEIGHT)]
WINDOWS = [yzwh2rect(1.75, 3, 2.5, 5),
           yzwh2rect(4.75, 3, 2.5, 5),

           yzwh2rect(8.75, 3, 2.5, 5),
           yzwh2rect(11.75, 3, 2.5, 5),

           yzwh2rect(15.75, 3, 2.5, 5),
           yzwh2rect(18.75, 3, 2.5, 5),

           yzwh2rect(22.75, 3, 2.5, 5),
           yzwh2rect(25.75, 3, 2.5, 5)]
APARTMENT_SPEC = [((D1, D2, 0), DOORS),
                  ((D2, D1, 0), WINDOWS),
                  ((D2, D1 + RAMP_LENGTH, 0), []),
                  ((D1, D1 + RAMP_LENGTH + (D1+D2)/2, 0), WINDOWS),
                  ((D1 + RAMP_LENGTH, D1 + RAMP_LENGTH + (D1+D2)/2, 0), []),
                  ((D1 + RAMP_LENGTH + (D1+D2)/2, D1 + RAMP_LENGTH, 0), WINDOWS),
                  ((D1 + RAMP_LENGTH + (D1+D2)/2, D1, 0), []),
                  ((D1 + RAMP_LENGTH, D2, 0), WINDOWS)]
APARTMENT = [entry[0] for entry in APARTMENT_SPEC]
APARTMENT_WINDOWS = [(i, entry[1]) for i, entry in enumerate(APARTMENT_SPEC)]
ATTIC = [nudge(APARTMENT[0], dx=-1.2, dy=-2),
         nudge(APARTMENT[1], dx=-2, dy=-1.2),
         nudge(APARTMENT[2], dx=-2, dy=1.2),
         nudge(APARTMENT[3], dx=-1.2, dy=2),
         nudge(APARTMENT[4], dx=1.2, dy=2),
         nudge(APARTMENT[5], dx=2, dy=1.2),
         nudge(APARTMENT[6], dx=2, dy=-1.2),
         nudge(APARTMENT[7], dx=1.2, dy=-2)]

def _get_cloverleaf_landing_pattern():
    # Make an empty 3-by-3 spatial grid for planning landings and ramps
    landings = [
        [[], [], []],
        [[], [], []],
        [[], [], []]
    ]

    # Initialize the landings altitudes and ramps directions
    landings[1][1].append((00.0, [Facing.NORTH]))
    landings[1][2].append((02.5, [Facing.EAST]))
    landings[2][2].append((05.0, [Facing.SOUTH]))
    landings[2][1].append((07.5, [Facing.WEST]))

    landings[1][1].append((10.0, [Facing.WEST]))
    landings[0][1].append((12.5, [Facing.NORTH]))
    landings[0][2].append((15.0, [Facing.EAST]))
    landings[1][2].append((17.5, [Facing.SOUTH]))

    landings[1][1].append((20.0, [Facing.SOUTH]))
    landings[1][0].append((22.5, [Facing.WEST]))
    landings[0][0].append((25.0, [Facing.NORTH]))
    landings[0][1].append((27.5, [Facing.EAST]))

    landings[1][1].append((30.0, [Facing.EAST]))
    landings[2][1].append((32.5, [Facing.SOUTH]))
    landings[2][0].append((35.0, [Facing.WEST]))
    landings[1][0].append((37.5, [Facing.NORTH]))

    landings[1][1].append((40.0, []))
    return landings


def _get_landing_pattern_for_four_cloverleafs():
    # Make an empty 5-by-5 spatial grid for planning landings and ramps
    landings = [
        [[], [], [], [], []],
        [[], [], [], [], []],
        [[], [], [], [], []],
        [[], [], [], [], []],
        [[], [], [], [], []]
    ]

    def _flip_ramp(ramp, northSouth: bool, eastWest: bool):
        if northSouth and ramp == Facing.NORTH:
            return Facing.SOUTH
        if northSouth and ramp == Facing.SOUTH:
            return Facing.NORTH
        if eastWest and ramp == Facing.EAST:
            return Facing.WEST
        if eastWest and ramp == Facing.WEST:
            return Facing.EAST
        return ramp

    def _flip_ramps(entries, northSouth: bool, eastWest: bool):
        out = []
        for entry in entries:
            (z, ramps) = entry
            flipped_ramps = [_flip_ramp(ramp, northSouth=northSouth, eastWest=eastWest) for ramp in ramps]
            out.append((z, flipped_ramps))
        return out

    pattern = _get_cloverleaf_landing_pattern()
    for i in range(3):
        for j in range(3):
            landings[i][j] = pattern[i][j]
        landings[i][3] = _flip_ramps(pattern[i][1], northSouth=True, eastWest=False)
        landings[i][4] = _flip_ramps(pattern[i][0], northSouth=True, eastWest=False)
    landings[3] = [_flip_ramps(entry, northSouth=False, eastWest=True) for entry in landings[1]]
    landings[4] = [_flip_ramps(entry, northSouth=False, eastWest=True) for entry in landings[0]]
    return landings


def _get_landing_pattern(num_rows: int, num_cols: int):
    pattern = _get_landing_pattern_for_four_cloverleafs()
    grid = []
    for i in range(num_rows+1):
        row = []
        for j in range(num_cols+1):
            row.append(pattern[i % 4][j % 4])
        grid.append(row)
    return grid


def _add_roof_around_floor(plato: Plato,
                           shape: Sequence[Xyz],
                           peak_xyz: Xyz):
    if peak_xyz[Z] == 0:
        plato.add_place(Place.ROOF, shape=shape)
    else:
        plato.add_place(Place.BARE, shape=shape)
        for i, xyz in enumerate(shape):
            next = i+1 if i+1 < len(shape) else 0
            triangle = [xyz, shape[next], peak_xyz]
            plato.add_place(Place.ROOF, shape=triangle)


def _add_features_at_landing(plato: Plato, ramp_bearings: Sequence, at: Xyz):
    """Make plato envision the floorspace for a landing and its ramps."""
    (x, y, z) = at

    # Landing
    plato.goto(x=x, y=y, z=z, facing=Facing.NORTH)
    plato.add_place(Place.WALKWAY, shape=OCTAGONAL_LANDING)

    # Ramps
    for bearing in ramp_bearings:
        plato.goto(x=x, y=y, z=z, facing=bearing)
        plato.add_place(Place.WALKWAY, shape=RAMP)

    # Floors, Walls, and Roof
    if z % STORY_HEIGHT == 0:
        for bearing in ramp_bearings:
            # parcel
            plato.goto(x=x, y=y, z=0, facing=bearing)
            plato.add_place(Place.PARCEL, shape=BASEMENT)
            # lower floors
            for altitude in range(0, int(z), STORY_HEIGHT):
                plato.goto(x=x, y=y, z=altitude, facing=bearing)
                plato.add_place(Place.ROOM, shape=BASEMENT)
            # upper floors
            for altitude in range(int(z), ROOFLINE, STORY_HEIGHT):
                plato.goto(x=x, y=y, z=altitude, facing=bearing)
                plato.add_place(Place.ROOM, shape=APARTMENT, wall=STORY_HEIGHT, openings=APARTMENT_WINDOWS)
            # Roof
            midpoint = (APARTMENT_WIDTH + D2)/2
            peak = (midpoint, midpoint, randint(0, 4)*7)
            plato.goto(x=x, y=y, z=ROOFLINE, facing=bearing)
            _add_roof_around_floor(plato, shape=ATTIC, peak_xyz=peak)
    return


class Merlon:
    """Merlon knows how build the merlon-style towers in the Pinq city design.
    """

    def __init__(self, plato: Plato):
        self._plato = plato

    def add_buildings(self, num_rows: int=2, num_cols: int=2):
        """Tell plato about all of our landings, ramps, rooms, and roofs."""
        for i, row in enumerate(_get_landing_pattern(num_rows, num_cols)):
            for j, grid_cell in enumerate(row):
                x = i * TOWER_SPACING
                y = j * TOWER_SPACING
                for landing_spec in grid_cell:
                    z = landing_spec[0]
                    ramp_bearings = landing_spec[1]
                    _add_features_at_landing(self._plato,
                                             ramp_bearings,
                                             at=(x, y, z))
        return self
