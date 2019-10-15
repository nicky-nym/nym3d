# nym.py
#
# <pep8-80 compliant>

# UNLICENSE
# This is free and unencumbered software released into the public domain.
# For more information, please refer to <http://unlicense.org>
#
# Authored in 2019 by Nicky Nym <https://github.com/nicky-nym>

from importlib import reload

# from place import Place

import bikeway as _bikeway
from bikeway import Bikeway

import cottage as _cottage
from cottage import Cottage

import manhattan as _manhattan
from manhattan import Manhattan

import merlon as _merlon
from merlon import Merlon

import wurster as _wurster
from wurster import Wurster

import plato as _plato
from plato import Plato

reload(_bikeway)
reload(_cottage)
reload(_manhattan)
reload(_merlon)
reload(_wurster)
reload(_plato)

if True:
    print("")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    plato = Plato()
    plato.delete_all_objects()

    plato.study("Cottage(s)", x0=-100, y0=100)
    cottage = Cottage(plato)
    cottage.add_street(12)
    plato.pontificate()

    CITY_SIZE = 4
    plato.study("Manhattan New York", x0=-800*CITY_SIZE, y0=-600*CITY_SIZE)
    nyc = Manhattan(plato)
    nyc.add_blocks(CITY_SIZE, CITY_SIZE*2)
    plato.pontificate()

    plato.study("Merlon Buildings", x0=238, y0=238)
    merlon = Merlon(plato)
    merlon.add_buildings(8, 8, buildings=True)
    plato.pontificate()

    plato.study("Bikeways", x0=100, y0=100)
    bikeway = Bikeway(plato)
    bikeway.add_bikeways(3, 3, buildings=True)
    plato.pontificate()

    plato.study("Wurster Hall(s)", x0=100, y0=-600)
    wurster = Wurster(plato)
    wurster.add_buildings(1)
    plato.pontificate()
