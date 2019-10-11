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

import plato as _plato
from plato import Plato

import merlon as _merlon
from merlon import Merlon

import cottage as _cottage
from cottage import Cottage

reload(_plato)
reload(_merlon)
reload(_cottage)


if True:
    print("")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    plato = Plato()
    plato.delete_all_objects()

    plato.study("Cottage")
    cottage = Cottage(plato)
    cottage.add_street(1)
    plato.pontificate()

    plato.study("Merlon")
    merlon = Merlon(plato)
    merlon.add_buildings(2, 2)
    plato.pontificate()
