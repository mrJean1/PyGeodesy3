
# -*- coding: utf-8 -*-

# Test L{deprecated} classes, functions and methods.

__all__ = ('Tests',)
__version__ = '23.12.17'

from bases import TestsBase

from pygeodesy3 import deprecated, isDEPRECATED, unstr
# try:
#     from pygeodesy3.deprecated import __star__
#     __star__(__name__)
# except ImportError:
#     from pygeodesy3.deprecated import *  # PYCHOK expected
# from pygeodesy3.interns import _DOT_, _UNDER_  # from .lazily
from pygeodesy3.lazily import _ALL_MODS as _MODS, _ALL_DEPRECATED,  \
                             _attrof, _DOT_, _headof, _UNDER_


class Tests(TestsBase):

    def testDEPRECATED(self, *known):
        for m, t in _ALL_DEPRECATED.items():
            if _headof(m) == 'deprecated':
                self.test(m, len(t), len(t), nl=1)
                m = _MODS.getmodule(m.replace(_UNDER_, _DOT_))
                for a in t:
                    a = _attrof(a)  # a_ or a
                    v =  getattr(m, a)
                    n =  unstr(isDEPRECATED, a)
                    self.test(n, isDEPRECATED(v), True, known=v in known)


if __name__ == '__main__':

    t = Tests(__file__, __version__, deprecated)
    try:
        t.testDEPRECATED(isDEPRECATED)
    except DeprecationWarning:
        t.skip(DeprecationWarning.__name__, n=1)
    t.results()
    t.exit()
