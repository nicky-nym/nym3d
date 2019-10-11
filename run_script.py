# run_script.py
#
# <pep8-80 compliant>

# UNLICENSE
# This is free and unencumbered software released into the public domain.
# For more information, please refer to <http://unlicense.org>
#
# Authored in 2019 by Nicky Nym <https://github.com/nicky-nym>

import bpy  # Blender API
import os
import sys

# NOTE: you must open "nym.blend" in Blender before doing run_script

nym_dir = os.path.dirname(bpy.data.filepath)
if nym_dir not in sys.path:
    sys.path.append(nym_dir)

filename = os.path.join(nym_dir, "nym.py")
exec(compile(open(filename).read(), filename, 'exec'))
