
# -*- coding: utf-8 -*-

from pygeodesy3.lazily import _ALL_LAZY, _init__star__, _lazy_import_as, _unLazy0

__version__ = '23.12.18'

if _unLazy0:
    if _init__star__:
        from pygeodesy3.base.cartesian import *  # PYCHOK expected
        from pygeodesy3.base.karney import *  # PYCHOK expected
        from pygeodesy3.base.latlon import *  # PYCHOK expected
        from pygeodesy3.base.nvector import *  # PYCHOK expected
#       from pygeodesy3.base.solve import *  # PYCHOK expected
        from pygeodesy3.base.units import *  # PYCHOK expected
        from pygeodesy3.base.utmups import *  # PYCHOK expected
        from pygeodesy3.base.vector3d import *  # PYCHOK expected
        from pygeodesy3.base.units import *  # PYCHOK expected

    __all__ = (_ALL_LAZY.base +
               _ALL_LAZY.base_cartesian +
               _ALL_LAZY.base_karney +
               _ALL_LAZY.base_latlon +
               _ALL_LAZY.base_nvector +
            #  _ALL_LAZY.base_solve +
               _ALL_LAZY.base_units +
               _ALL_LAZY.base_utmups +
               _ALL_LAZY.base_vector3d)

else:  # lazily import modules only
    __getattr__ = _lazy_import_as(__name__)

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
