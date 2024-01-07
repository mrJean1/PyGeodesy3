
# -*- coding: utf-8 -*-

u'''Precision mathematical classes and functions.
'''
from pygeodesy3.lazily import _ALL_LAZY, _init__star__, _lazy_import_as, _unLazy0

__version__ = '23.12.18'

if _unLazy0:
    if _init__star__:  # PYCHOK no cover
        from pygeodesy3.maths.auxilats import *  # PYCHOK expected
        from pygeodesy3.maths.elliptic import *  # PYCHOK expected
        from pygeodesy3.maths.fmath import *  # PYCHOK expected
        from pygeodesy3.maths.fstats import *  # PYCHOK expected
        from pygeodesy3.maths.fsums import *  # PYCHOK expected
        from pygeodesy3.maths.umath import *  # PYCHOK expected
        from pygeodesy3.maths.vector2d import *  # PYCHOK expected
        from pygeodesy3.maths.vector3d import *  # PYCHOK expected

    __all__ = (_ALL_LAZY.maths +
               _ALL_LAZY.maths_auxilats +
               _ALL_LAZY.maths_elliptic +
               _ALL_LAZY.maths_fmath +
               _ALL_LAZY.maths_fstats +
               _ALL_LAZY.maths_fsums +
               _ALL_LAZY.maths_umath +
               _ALL_LAZY.maths_vector2d +
               _ALL_LAZY.maths_vector3d)

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
