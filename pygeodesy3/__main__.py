
# -*- coding: utf-8 -*-

u'''Print L{pygeodesy3} version, etc. using C{python -m pygeodesy3}.
'''

__all__ = ()
__version__ = '23.12.31'

from os.path import basename


def _main():  # PYCHOK no cover

    from pygeodesy3 import _isfrozen, pygeodesy3_abspath, version
    from pygeodesy3.basics import _xgeographiclib, _xnumpy, _xscipy
    from pygeodesy3.constants import _floats
    from pygeodesy3.interns import _COMMASPACE_, _DEPRECATED_, _pygeodesy3_abspath_, \
                                   _pythonarchine, _SPACE_, _version_
    from pygeodesy3.lazily import _a_l_l_, _all_deprecates, _all_imports, \
                                  isLazy, printf
    from pygeodesy3.miscs.streprs import Fmt

    def _p(name_value):
        return Fmt.DOT(Fmt.EQUAL(*name_value))

    p = [_p(t) for t in ((_version_,                       version),
                         (_pygeodesy3_abspath_, pygeodesy3_abspath),
                         ('isLazy',                         isLazy),
                         ('_isfrozen',                   _isfrozen),
                         ('_floats',                  len(_floats)),
                         (_a_l_l_,             len(_all_imports())),
                         (_DEPRECATED_,     len(_all_deprecates())))]

    def _nv(_xpkg, v):
        try:
            pkg = _xpkg(_main)
        except ImportError:
            pkg = None
        if pkg is not None:
            v.append(_SPACE_(pkg.__name__, pkg.__version__))

    v = _pythonarchine()
    _nv(_xgeographiclib, v)
    _nv(_xnumpy, v)
    _nv(_xscipy, v)

    x = basename(pygeodesy3_abspath)
    printf('%s%s (%s)', x, _COMMASPACE_.join(p), _COMMASPACE_.join(v))


try:
    _main()
except ImportError:
    from pygeodesy3.interns import _usage
    print(_usage(__file__))

# % python3 -m pygeodesy3

# pygeodesy3.version=24.01.05, .pygeodesy3_abspath=.../PyGeodesy3/pygeodesy3, .isLazy=1, ._isfrozen=False, ._floats=82, .__all__=938, .DEPRECATED=73 (Python 3.12.0, 64bit, arm64, geographiclib 2.0)

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

# % python3.12 -m pygeodesy3
# pygeodesy3.version=23.11.11, .pygeodesy3_abspath=.../PyGeodesy3/pygeodesy3, .isLazy=1, ._isfrozen=False, ._floats=82, .__all__=964 (Python 3.12.0, 64bit, arm64, geographiclib 2.0)

# % python3.11 -m pygeodesy3
# pygeodesy3.version=23.11.11, .pygeodesy3_abspath=.../PyGeodesy3/pygeodesy3, .isLazy=1, ._isfrozen=False, ._floats=82, .__all__=964 (Python 3.11.5, 64bit, arm64, geographiclib 2.0, numpy 1.24.2, scipy 1.10.1)

# % python3.10 -m pygeodesy3
# pygeodesy3.version=23.11.11, .pygeodesy3_abspath=.../PyGeodesy3/pygeodesy3, .isLazy=1, ._isfrozen=False, ._floats=82, .__all__=964 (Python 3.10.8, 64bit, arm64, geographiclib 2.0, numpy 1.23.3, scipy 1.9.1)

# % python3.9 -m pygeodesy3
# pygeodesy3.version=23.11.11, .pygeodesy3_abspath=.../PyGeodesy3/pygeodesy3, .isLazy=1, ._isfrozen=False, ._floats=82, .__all__=964 (Python 3.9.6, 64bit, arm64)

# % python3.8 -m pygeodesy3
# pygeodesy3.version=23.1.6, .pygeodesy3_abspath=.../PyGeodesy3/pygeodesy3, .isLazy=1, ._isfrozen=False, ._floats=81, .__all__=908 (Python 3.8.10, 64bit, arm64_x86_64, geographiclib 1.52, numpy 1.19.2, scipy 1.5.2)

# % python2 -m pygeodesy3
# pygeodesy3.version=23.1.6, .pygeodesy3_abspath=.../PyGeodesy3/pygeodesy3, .isLazy=None, ._isfrozen=False, ._floats=560, .__all__=908 (Python 2.7.18, 64bit, arm64_x86_64, geographiclib 1.50, numpy 1.16.6, scipy 1.2.2)
