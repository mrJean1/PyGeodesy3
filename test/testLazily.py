
# -*- coding: utf-8 -*-

# Test the lazy import module L{lazily}.

__all__ = ('Tests',)
__version__ = '24.03.03'

from bases import TestsBase, coverage, _env_c2, isLazy, \
                  isPython37, lazily, type2str
import pygeodesy3


class Tests(TestsBase):

    def testLazily(self):

        if coverage:
            a = lazily._import_all()
            self.test('_all', len(a), 932)
            b = lazily._import_all_backward(True)
            self.test('_all_backward', len(b), 78, nt=1)
            _all = a + b
        else:
            _all = pygeodesy3.__all__

        for a in sorted(_all, key=str.lower):
            t = type2str(pygeodesy3, a).replace('()', '').strip()
            self.test(a, t, t)

        self.test('isLazy', isLazy, isLazy, nl=1)
        if len(_all) > 2:
            for a, m in lazily._all_missing2(_all):
                t = len(m) > 2  # XXX
                m = ', '.join(m) if m else None
                self.test('missing in %s' % (a,), m, None, known=t)

        # simple lazy_import enable tests
        env_cmd, cmd = _env_c2("-c 'import sys; import pygeodesy3; "
                                   "sys.exit(0 if pygeodesy3.isLazy == %s else 1)'")
        self.test('cmd', cmd, cmd, nl=1)
        if env_cmd:
            from os import system
            for z in range(1, 5):
                e = 'PYGEODESY3_LAZY_IMPORT=%s' % (z,)
                c =  env_cmd % (e, z if isPython37 else None)
                x =  system(c) >> 8  # exit status in high byte
                self.test(e, x, 0)
        else:
            self.skip('no env_cmd')

        M = lazily._ALL_MODS
        self.test('items', M._name, M._name, nl=1)
        for n, m in sorted(M.items()):  # coverage
            self.test(n, m, m)

#       p = pygeodesy3.printf
#       t = p('to %(std)s, flushed', nl=1, std='stdout', file=sys.stdout, flush=True)
#       self.test('%s to stdout, flushed' % (p.__name__,), t, t)


if __name__ == '__main__':

    t = Tests(__file__, __version__)
    t.testLazily()
    t.results()
    t.exit()
