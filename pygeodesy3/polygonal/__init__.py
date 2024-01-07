
# -*- coding: utf-8 -*-

u'''Classes and functions for operations on polygons or polylines, open or
closed lists of points.
'''
from pygeodesy3.lazily import _ALL_LAZY, _init__star__, _lazy_import_as, _unLazy0

__version__ = '23.12.21'

if _unLazy0:
    if _init__star__:  # PYCHOK no cover
        from pygeodesy3.polygonal.booleans import *  # PYCHOK expected
        from pygeodesy3.polygonal.clipy import *  # PYCHOK expected
        from pygeodesy3.polygonal.points import *  # PYCHOK expected
        from pygeodesy3.polygonal.simplify import *  # PYCHOK expected

    __all__ = (_ALL_LAZY.polygonal +
               _ALL_LAZY.polygonal_booleans +
               _ALL_LAZY.polygonal_clipy +
               _ALL_LAZY.polygonal_points +
               _ALL_LAZY.polygonal_simplify)

else:  # lazily import modules and deprecated attr
    __getattr__ = _lazy_import_as(__name__)
#   __star__    = _lazy_import_star(__name__)

# **) MIT License
#
# Copyright (C) 2023-2024 -- mrJean1 at Gmail -- All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
