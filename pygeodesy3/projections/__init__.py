
# -*- coding: utf-8 -*-

u'''Various earth projections.
'''
from pygeodesy3.lazily import _ALL_LAZY, _init__star__, _lazy_import_as, _unLazy0

__version__ = '23.12.18'

if _unLazy0:
    if _init__star__:  # PYCHOK no cover
        from pygeodesy3.projections.albers import *  # PYCHOK expected
        from pygeodesy3.projections.azimuthal import *  # PYCHOK expected
        from pygeodesy3.projections.css import *  # PYCHOK expected
        from pygeodesy3.projections.etm import *  # PYCHOK expected
        from pygeodesy3.projections.ktm import *  # PYCHOK expected
        from pygeodesy3.projections.lcc import *  # PYCHOK expected
        from pygeodesy3.projections.ltp import *  # PYCHOK expected
        from pygeodesy3.projections.ltpTuples import *  # PYCHOK expected
        from pygeodesy3.projections.ups import *  # PYCHOK expected
        from pygeodesy3.projections.utm import *  # PYCHOK expected
        from pygeodesy3.projections.utmups import *  # PYCHOK expected
        from pygeodesy3.projections.webmercator import *  # PYCHOK expected

    __all__ = (_ALL_LAZY.projections +
               _ALL_LAZY.projections_albers +
               _ALL_LAZY.projections_azimuthal +
               _ALL_LAZY.projections_css +
               _ALL_LAZY.projections_etm +
               _ALL_LAZY.projections_ktm +
               _ALL_LAZY.projections_lcc +
               _ALL_LAZY.projections_ltp +
               _ALL_LAZY.projections_ltpTuples +
               _ALL_LAZY.projections_ups +
               _ALL_LAZY.projections_utm +
               _ALL_LAZY.projections_utmups +
               _ALL_LAZY.projections_webmercator)

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
