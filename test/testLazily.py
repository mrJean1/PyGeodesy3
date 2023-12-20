
# -*- coding: utf-8 -*-

# Test the lazy import module L{lazily}.

__all__ = ('Tests',)
__version__ = '23.12.18'

from bases import TestsBase, ismacOS, isNix, isPython37, isWindows, \
                  PythonX, type2str
import pygeodesy3

lazily = pygeodesy3.lazily
_all_  = pygeodesy3.__all__

import os
# import sys

_cmd = PythonX + " -c 'import pygeodesy3, sys; " \
                      "sys.exit(0 if pygeodesy3.isLazy == %s else 1)'"
if ismacOS or isNix:
    _env_cmd = 'env %s ' + _cmd + ' >>/dev/null'
elif isWindows:  # XXX UNTESTED
    _env_cmd = 'set %s;' + _cmd
else:
    _env_cmd = None

_HOME = os.getenv('HOME', '')
if _HOME and _cmd.startswith(_HOME):
    _cmd = '~' + _cmd[len(_HOME):]
del _HOME


class Tests(TestsBase):

    def testLazily(self):

        for a in sorted(_all_, key=str.lower):
            t = type2str(pygeodesy3, a).replace('()', '').strip()
            self.test(a, t, t)

        z = pygeodesy3.isLazy
        self.test('isLazy', z, z)
        if not z:
            for a, m in lazily._all_missing2(_all_):
                t = all(_.startswith('rhumb') for _ in m) if m else False
                m = ', '.join(m) if m else None
                self.test('missing in %s' % (a,), m, None, known=t)

        # simple lazy_import enable tests
        self.test('cmd', _cmd, _cmd)
        if _env_cmd:
            for z in range(1, 5):
                e = 'PYGEODESY3_LAZY_IMPORT=%s' % (z,)
                c = _env_cmd % (e, z if isPython37 else None)
                x = os.system(c) >> 8  # exit status in high byte
                self.test(e, x, 0)
        else:
            self.skip('no _env_cmd')

        for n, m in lazily._ALL_MODS.items():  # coverage
            self.test(n, m, m)

#       p = pygeodesy3.printf
#       t = p('to %(std)s, flushed', nl=1, std='stdout', file=sys.stdout, flush=True)
#       self.test('%s to stdout, flushed' % (p.__name__,), t, t)


if __name__ == '__main__':

    t = Tests(__file__, __version__)
    t.testLazily()
    t.results()
    t.exit()