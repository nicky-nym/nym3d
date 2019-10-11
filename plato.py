# plato.py
#
# <pep8-80 compliant>

# UNLICENSE
# This is free and unencumbered software released into the public domain.
# For more information, please refer to <http://unlicense.org>
#
# Authored in 2019 by Nicky Nym <https://github.com/nicky-nym>

import bpy
import bmesh  # for creating Blender mesh objects

from typing import Tuple, Sequence, Iterable, Any, List, Optional, Union
import math

from xyz import Num, Xyz, X, Y, Z, xy2xyz, nudge
from compass_facing import CompassFacing as Facing
from place import Place

WHITE = (1, 1, 1, 1)  # opaque white
RED = (0.8, 0, 0, 1)  # opaque red
GREEN = (0, 1, 0, 1)  # opaque green
BLUE = (0, 0, 1, 1)  # opaque blue
YELLOW = (1, 1, 0, 1)  # opaque yellow

GREEN_GRASS = (0, 0.3, 0, 1)  # opaque dark green
BROWN = (0.5, 0.4, 0.2, 1)
DARK_GRAY = (0.25, 0.25, 0.25, 1)  # opaque dark gray
LIGHT_GRAY = (0.8745, 0.8745, 0.8745, 1)  # opaque light gray
BLUE_GLASS = (0.6, 0.6, 1, 0.8)  # transparent light blue
MARTIAN_ORANGE = (0.8745, 0.2863, 0.0667, 1)  # opaque Martian orange

COLORS_OF_PLACES = {
    Place.STREET: RED,
    Place.BIKEPATH: MARTIAN_ORANGE,
    Place.WALKWAY: YELLOW,
    Place.ROOM: BROWN,
    Place.BARE: LIGHT_GRAY,
    Place.PARCEL: GREEN_GRASS,
    Place.CANAL: BLUE,

    Place.WALL: WHITE,
    Place.ROOF: DARK_GRAY,
    Place.DOOR: YELLOW
}


def _rotate(xyz, facing: Facing):
    (x, y, z) = xyz
    if facing == Facing.NORTH:
        return (x, y, z)
    elif facing == Facing.SOUTH:
        return (-x, -y, z)
    elif facing == Facing.EAST:
        return (y, -x, z)
    elif facing == Facing.WEST:
        return (-y, x, z)

    # TODO: not implemented yet
    SIN45 = COS45 = 0.707
    if facing == Facing.NORTHEAST:
        return (x*COS45 - y*SIN45, x*COS45 + y*SIN45, z)
    elif facing == Facing.SOUTHEAST:
        return (-x, -y, z)
    elif facing == Facing.SOUTHWEST:
        return (y, -x, z)
    elif facing == Facing.NORTHWEST:
        return (-y, x, z)

    else:
        raise Exception("bad compass facing in plato._rotate(): " + str(facing.value))


def _material_by_place(place: Place):
    material = bpy.data.materials.get(place.name)
    if material is None:
        material = bpy.data.materials.new(name=place.name)
        material.diffuse_color = COLORS_OF_PLACES[place]
    return material


def _printXyz(xyz: Xyz):
    (x, y, z) = xyz
    print("   xyz: ({:,.2f}, {:,.2f}, {:,.2f})".format(x, y, z))


def _xyzFromDotOnEdge(length: Num, height: Num, edge: Tuple[Xyz]):
    (x0, y0, z0) = edge[0]
    (x1, y1, z1) = edge[1]
    x_span = x1 - x0
    y_span = y1 - y0
    edge_length = math.sqrt(x_span**2 + y_span**2)

    # (d_edge, dz) = dot
    dx = length * x_span / edge_length
    dy = length * y_span / edge_length
    return (x0+dx, y0+dy, z0+height)


class Plato:
    """Plato can envision 3D architectural spaces, with walls, floors, etc."""

    def __init__(self, hurry: bool=False):
        """Sets plato's initial mental state."""
        self._x = 0
        self._y = 0
        self._z = 0
        self._facing = Facing.NORTH
        self.hurry(hurry)
        self.study()

    def hurry(self, hurry: bool=False):
        self._hurry = hurry
        return self

    def study(self, topic: str=""):
        self._topic = topic
        self._square_feet = {}

    def goto(self, *, x: Num=0, y: Num=0, z: Num=0, facing: Facing=Facing.NORTH):
        self._x = x
        self._y = y
        self._z = z
        self._facing = facing
        # print("  goto: ({:,.0f},{:,.0f},{:,.0f})".format(x, y, z))
        return self

    def delete_all_objects(self):
        """Try to delete everything in the Blender scene."""

        if bpy.context.active_object:
            mode = bpy.context.active_object.mode
            # print("mode: " + mode)
            if (mode == 'EDIT'):
                bpy.ops.object.mode_set(mode='OBJECT')
                mode = bpy.context.active_object.mode
                print("new mode: " + mode)
                # print("SELECT and delete FACE")
                # bpy.ops.mesh.select_all(action='SELECT')
                # bpy.ops.mesh.delete(type='FACE')
            if (mode == 'OBJECT'):
                bpy.ops.object.select_all(action='SELECT')
                bpy.ops.object.delete(use_global=False)
        else:
            print("mode: There is no active_object")
        return self

    def _begin_face(self):
        self._bmesh = bmesh.new()

    def _end_face(self):
        return self._bmesh.faces.new(self._bmesh.verts)

    def _new_bpy_object_for_face(self):
        self._bmesh.normal_update()
        my_mesh = bpy.data.meshes.new("")
        self._bmesh.to_mesh(my_mesh)
        self._bmesh.free()
        obj = bpy.data.objects.new("", my_mesh)
        return obj

    def _new_vert(self, xyz: Xyz):
        xyz = _rotate(xyz, self._facing)
        dxyz = (self._x, self._y, self._z)
        xyz = nudge(xyz, dxyz=dxyz)
        self._bmesh.verts.new(xyz)

    def add(self,
            place: Place,
            *,
            shape: Sequence[Xyz],
            openings: Sequence[Sequence[Xyz]]=[],
            nuance: bool=False,
            flip: bool=False):
        """Add a new mesh to the blender scene."""

        if nuance and self._hurry:
            return self
        at = (self._x, self._y, self._z)
        self._begin_face()
        if self._hurry or len(openings) == 0:
            for xyz in shape:
                self._new_vert(xyz)
            face = self._end_face()
        else:
            edge = (shape[0], shape[1])
            self._new_vert(shape[0])
            for i, opening in enumerate(openings):
                opening = opening.copy()
                opening.reverse()
                opening = opening[-1:] + opening[:-1]  # rotate: last to first
                (length, height) = opening[0]
                base_point = _xyzFromDotOnEdge(length, shape[0][Z], edge)
                self._new_vert(base_point)
                for qz in opening:
                    (length, height) = qz
                    xyz = _xyzFromDotOnEdge(length, height, edge)
                    self._new_vert(xyz)
                (length, height) = opening[0]
                xyz = _xyzFromDotOnEdge(length, height, edge)
                self._new_vert(xyz)
                self._new_vert(base_point)
            for xyz in shape:
                self._new_vert(xyz)
            face = self._end_face()

        area = face.calc_area()
        self._square_feet[place] = area + self._square_feet.get(place, 0)

        obj = self._new_bpy_object_for_face()
        obj.data.materials.append(_material_by_place(place))
        scene = bpy.context.scene
        scene.collection.objects.link(obj)
        return self

    def add_place(self,
                  place: Place,
                  *,
                  shape: Sequence[Xyz],
                  nuance: bool=False,
                  flip: bool=False,
                  wall: Num=0,
                  openings: Sequence[Tuple]=[]):
        self.add(place=place, shape=shape, nuance=nuance, flip=flip)
        if wall != 0:
            self.add_wall(shape=shape, height=wall, openings=openings, nuance=nuance)
        return self

    def add_wall(self,
                 *,
                 shape: Sequence[Xyz],
                 height: Num=10,
                 openings: Sequence[Tuple]=[],
                 nuance: bool=False,
                 cap: bool=True):
        for i, xyz in enumerate(shape):
            windows = []
            for opening in openings:
                if opening[0] == i:
                    windows = opening[1]
            if cap or i+1 < len(shape):
                next = i+1 if i+1 < len(shape) else 0
                wall = [xyz,
                        shape[next],
                        nudge(shape[next], dz=height),
                        nudge(xyz, dz=height)]
                self.add(Place.WALL, shape=wall, nuance=nuance, openings=windows)
        return self

    def pontificate(self):
        """Print a report of square footage of rooms, walkways, etc."""

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("")
        print(str(self._topic) + " floor area")
        print("")
        for role_name in self._square_feet.keys():
            area = self._square_feet[role_name]
            print("  {}: {:,.0f} square feet".format(role_name.name, area))

        floor = self._square_feet.get(Place.ROOM, 0)
        parcel = self._square_feet.get(Place.PARCEL, 10)
        street = self._square_feet.get(Place.STREET, 0)
        if parcel:
            parcel_far = floor / parcel
            urban_far = floor / (parcel + street)
            print("")
            print("  Parcel FAR: {:,.2f} floor area ratio".format(parcel_far))
            print("  Urban  FAR: {:,.2f} floor area ratio".format(urban_far))

        proximity = 0
        propinquity = 0
        print("  Proximity: {:,.2f} ???".format(proximity))
        print("  Propinquity: {:,.2f} ???".format(propinquity))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        return self

    def add_cubes(self, number_of_cubes: int=1):
        """Create N new cubes at random locations, with different orientations.
        """
        for i in range(number_of_cubes):
            x = randint(-10, 20)
            y = randint(-10, 20)
            z = randint(-10, 20)
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z), size=4)
            radians = i*(3.14/(4*number_of_cubes))
            bpy.ops.transform.rotate(orient_axis='Z', value=radians)
        return self
