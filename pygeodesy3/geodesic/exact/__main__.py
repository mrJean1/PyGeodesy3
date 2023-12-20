
# -*- coding: utf-8 -*-

u'''Print L{geodesic.exact} version, etc. using C{python -m pygeodesy3.geodesic.exact}.
'''

__all__ = ()
__version__ = '23.12.18'


def _C4stats(gx, nC4=None):  # PYCHOK no cover
    '''(INTERNAL) Get the C{C4} stats.
    '''
    gX = gx.GeodesicExact(C4order=nC4)
    cs = gx._C4coeffs(gX.C4order)
    ss = set(cs)  # without duplicates
    pc = '%.1f%%' % (len(ss) * 100.0 / len(cs))
    cx = gX._C4x
    return dict(C4order=gX.C4order, C4len=len(cs), C4set=len(ss), C4set_len=pc, C4x=len(cx))


def _main():  # PYCHOK no cover

    import os.path as os_path

    try:
        from pygeodesy3.interns import _COMMASPACE_, _DOT_, _pythonarchine, \
                                       _SPACE_, _usage, _version_
        from pygeodesy3 import pygeodesy3_abspath
        from pygeodesy3.geodesic import exact
        from pygeodesy3.geodesic.solve import GeodesicSolve
        from pygeodesy3.lazily import printf
        from pygeodesy3.miscs.errors import GeodesicError
        from pygeodesy3.miscs.streprs import Fmt

        def _dot_attr(name, value):
            return Fmt.DOT(Fmt.EQUAL(name, value))

        s = tuple(sorted(_C4stats(exact.gx).items()))
        p = [_dot_attr(*t) for t in (((_version_, exact.__version__),) + s)]

        def _name_version(pkg):
            return _SPACE_(pkg.__name__, pkg.__version__)

        v = _pythonarchine()
        try:
            import geographiclib
            v.append(_name_version(geographiclib))
        except ImportError:
            pass
        try:
            g = GeodesicSolve()
            v.append(g.version)
        except GeodesicError:
            pass

        g = exact.__name__
        x = os_path.basename(pygeodesy3_abspath)
        if not g.startswith(x):
            g = _DOT_(x, g)
        printf('%s%s (%s)', g, _COMMASPACE_.join(p), _COMMASPACE_.join(v))

    except ImportError:
        print(_usage(__file__))


_main()

# **) MIT License
#
# Copyright (C) 2016-2024 -- mrJean1 at Gmail -- All Rights Reserved.
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

# % python3 -m pygeodesy3.geodesic.exact
# pygeodesy3.geodesic.exact.version=23.12.05, .C4Order=None, .C4len=5425, .C4set=5107, .C4set100=94, .C4x=465 (Python 3.9.5, 64bit, geographiclib 1.52)
