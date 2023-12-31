
# -*- coding: utf-8 -*-

u'''Some, basic definitions, functions and dependencies.

Use env variable C{PYGEODESY3_XPACKAGES} to avoid import of dependencies
C{geographiclib}, C{numpy} and/or C{scipy}.  Set C{PYGEODESY3_XPACKAGES}
to a comma-separated list of package names to be excluded from import.
'''
# make sure int/int division yields float quotient
from __future__ import division
division = 1 / 2  # .albers, .azimuthal, .constants, .maths.umath, etc.
if not division:
    raise ImportError('%s 1/2 == %s' % ('division', division))
del division

# from pygeodesy3.Base.latlon import LatLonBase  # _MODS
# from pygeodesy3.Base.nvector import NvectorBase  # _MODS
from pygeodesy3.interns import MISSING, NN, _1_, _by_, _COMMA_, _DEPRECATED_, \
                              _DOT_, _ELLIPSIS4_, _enquote, _EQUAL_, _in_, _invalid_, \
                              _N_A_, _SPACE_, _UNDER_, _version_  # _utf_8_
from pygeodesy3.lazily import _ALL_LAZY, _ALL_MODS as _MODS, _FOR_DOCS, _getenv, \
                               LazyImportError, _sys, _sys_version_info2
# from pygeodesy3.miscs.errors import _AssertionError, _AttributeError, _ImportError, \
#                _NotImplementedError, _TypeError, _TypesError, _ValueError  # _MODS
# from pygeodesy3.miscs.named import classname, modulename  # _MODS

from copy import copy as _copy, deepcopy as _deepcopy
from math import copysign as _copysign
import inspect as _inspect

__all__ = _ALL_LAZY.basics
__version__ = '24.01.05'

_0_0                   =  0.0  # in .constants
_below_                = 'below'
_can_t_                = "can't"
_list_tuple_types      = (list, tuple)
_list_tuple_set_types  = (list, tuple, set)
_odd_                  = 'odd'
_required_             = 'required'
_PYGEODESY3_XPACKAGES_ = 'PYGEODESY3_XPACKAGES'

try:  # Luciano Ramalho, "Fluent Python", O'Reilly, 2016 p. 395, 2022 p. 577+
    from numbers import Integral as _Ints, Real as _Scalars  # .units
except ImportError:
    try:
        _Ints = int, long  # int objects (C{tuple})
    except NameError:  # Python 3+
        _Ints = int,  # int objects (C{tuple})
    _Scalars = _Ints + (float,)

try:
    try:  # use C{from collections.abc import ...} in Python 3.9+
        from collections.abc import Sequence as _Sequence  # in .points
    except ImportError:  # no .abc in Python 3.8- and 2.7-
        from collections import Sequence as _Sequence  # in .points
    if isinstance([], _Sequence) and isinstance((), _Sequence):
        #                        and isinstance(range(1), _Sequence):
        _Seqs = _Sequence
    else:
        raise ImportError()
except ImportError:
    _Sequence = tuple  # immutable for .points._Basequence
    _Seqs     = list, _Sequence  # range for function len2 below


def _passarg(arg):  # in .maths.auxilats.auxLat
    '''(INTERNAL) Helper, no-op.
    '''
    return arg


def _passargs(*args):  # in .maths.umath
    '''(INTERNAL) Helper, no-op.
    '''
    return args


try:
    _Bytes = unicode, bytearray  # PYCHOK expected
    _Strs  = basestring, str  # XXX , bytes
    str2ub = ub2str = _passarg  # avoids UnicodeDecodeError

    def _Xstr(exc):  # PYCHOK no cover
        '''I{Invoke only with caught ImportError} B{C{exc}}.

           C{... "can't import name _distributor_init" ...}

           only for C{numpy}, C{scipy} import errors occurring
           on arm64 Apple Silicon running macOS' Python 2.7.16?
        '''
        t = str(exc)
        if '_distributor_init' in t:
            from sys import exc_info
            from traceback import extract_tb
            tb = exc_info()[2]  # 3-tuple (type, value, traceback)
            t4 = extract_tb(tb, 1)[0]  # 4-tuple (file, line, name, 'import ...')
            t = _SPACE_(_can_t_, t4[3] or _N_A_)
            del tb, t4
        return t

except NameError:  # Python 3+
    from pygeodesy3.interns import _utf_8_

    _Bytes = bytes, bytearray
    _Strs  = str,  # tuple
    _Xstr  = str

    def str2ub(sb):
        '''Convert C{str} to C{unicode bytes}.
        '''
        if isinstance(sb, _Strs):
            sb = sb.encode(_utf_8_)
        return sb

    def ub2str(ub):
        '''Convert C{unicode bytes} to C{str}.
        '''
        if isinstance(ub, _Bytes):
            ub = str(ub.decode(_utf_8_))
        return ub


def clips(sb, limit=50, white=NN):
    '''Clip a string to the given length limit.

       @arg sb: String (C{str} or C{bytes}).
       @kwarg limit: Length limit (C{int}).
       @kwarg white: Optionally, replace all whitespace (C{str}).

       @return: The clipped or unclipped B{C{sb}}.
    '''
    T = type(sb)
    if len(sb) > limit > 8:
        h  = limit // 2
        sb = T(_ELLIPSIS4_).join((sb[:h], sb[-h:]))
    if white:  # replace whitespace
        sb = T(white).join(sb.split())
    return sb


def copysign0(x, y):
    '''Like C{math.copysign(x, y)} except C{zero}, I{unsigned}.

       @return: C{math.copysign(B{x}, B{y})} if B{C{x}} else
                C{type(B{x})(0)}.
    '''
    return _copysign(x, (y if y else 0)) if x else copytype(0, x)


def copytype(x, y):
    '''Return the value of B{x} as C{type} of C{y}.

       @return: C{type(B{y})(B{x})}.
    '''
    return type(y)(x if x else _0_0)


def halfs2(str2):
    '''Split a string in 2 halfs.

       @arg str2: String to split (C{str}).

       @return: 2-Tuple C{(_1st, _2nd)} half (C{str}).

       @raise ValueError: Zero or odd C{len(B{str2})}.
    '''
    h, r = divmod(len(str2), 2)
    if r or not h:
        E = _MODS.miscs.errors._ValueError
        raise E(str2=str2, txt=_odd_)
    return str2[:h], str2[h:]


def int1s(x):
    '''Count the number of 1-bits in an C{int}, I{unsigned}.

       @note: C{int1s(-B{x}) == int1s(abs(B{x}))}.
    '''
    try:
        return x.bit_count()  # Python 3.10+
    except AttributeError:
        # bin(-x) = '-' + bin(abs(x))
        return bin(x).count(_1_)


def isbool(obj):
    '''Check whether an object is C{bool}ean.

       @arg obj: The object (any C{type}).

       @return: C{True} if B{C{obj}} is C{bool}ean,
                C{False} otherwise.
    '''
    return isinstance(obj, bool)  # and (obj is False
#                                     or obj is True)

assert not (isbool(1) or isbool(0))  # PYCHOK 2

if _FOR_DOCS:  # XXX avoid epidoc Python 2.7 error

    def isclass(obj):
        '''Return C{True} if B{C{obj}} is a C{class} or C{type}.

           @see: Python's C{inspect.isclass}.
        '''
        return _inspect.isclass(obj)
else:
    isclass = _inspect.isclass


def isCartesian(obj, ellipsoidal=None):
    '''Is B{C{obj}} some C{Cartesian}?

       @arg obj: The object (any C{type}).
       @kwarg ellipsoidal: If C{None}, return the type of any C{Cartesian},
                           if C{True}, only an ellipsoidal C{Cartesian type}
                           or if C{False}, only a spherical C{Cartesian type}.

       @return: C{type(B{obj}} if B{C{obj}} is a C{Cartesian} instance of
                the required type, C{False} if a C{Cartesian} of an other
                type or C{None} otherwise.
    '''
    if ellipsoidal is not None:
        try:
            return obj.ellipsoidalCartesian if ellipsoidal else \
                   obj.sphericalCartesian
        except AttributeError:
            return None
    return isinstanceof(obj, _MODS.Base.cartesian.CartesianBase)


def iscomplex(obj):
    '''Check whether an object is a C{complex} or complex C{str}.

       @arg obj: The object (any C{type}).

       @return: C{True} if B{C{obj}} is C{complex}, otherwise
                C{False}.
    '''
    try:  # hasattr('conjugate'), hasattr('real') and hasattr('imag')
        return isinstance(obj,          complex) or (isstr(obj)
           and isinstance(complex(obj), complex))  # numbers.Complex?
    except (TypeError, ValueError):
        return False


def isDEPRECATED(obj):
    '''Return C{True} if C{B{obj}} is a C{DEPRECATED} class, method
       or function, C{False} if not or C{None} if undetermined.
    '''
    try:  # XXX inspect.getdoc(obj)
        return bool(obj.__doc__.lstrip().startswith(_DEPRECATED_))
    except AttributeError:
        return None


def isfloat(obj):
    '''Check whether an object is a C{float} or float C{str}.

       @arg obj: The object (any C{type}).

       @return: C{True} if B{C{obj}} is a C{float}, otherwise
                C{False}.
    '''
    try:
        return isinstance(      obj,  float) or (isstr(obj)
           and isinstance(float(obj), float))
    except (TypeError, ValueError):
        return False


try:
    isidentifier = str.isidentifier  # Python 3, must be str
except AttributeError:  # Python 2-

    def isidentifier(obj):
        '''Return C{True} if B{C{obj}} is a Python identifier.
        '''
        return bool(obj and isstr(obj)
                        and obj.replace(_UNDER_, NN).isalnum()
                        and not obj[:1].isdigit())


def isinstanceof(obj, *classes):
    '''Is B{C{ob}} an intance of one of the C{classes}?

       @arg obj: The instance (any C{type}).
       @arg classes: One or more classes (C{class}).

       @return: C{type(B{obj}} if B{C{obj}} is an instance
                of the B{C{classes}}, C{None} otherwise.
    '''
    return type(obj) if isinstance(obj, classes) else None


def isint(obj, both=False):
    '''Check for C{int} type or an integer C{float} value.

       @arg obj: The object (any C{type}).
       @kwarg both: If C{true}, check C{float} and L{Fsum}
                    type and value (C{bool}).

       @return: C{True} if B{C{obj}} is C{int} or I{integer}
                C{float} or L{Fsum}, C{False} otherwise.

       @note: Both C{isint(True)} and C{isint(False)} return
              C{False} (and no longer C{True}).
    '''
    if isinstance(obj, _Ints) and not isbool(obj):
        return True
    elif both:  # and isinstance(obj, (float, Fsum))
        try:  # NOT , _Scalars) to include Fsum!
            return obj.is_integer()
        except AttributeError:
            pass  # XXX float(int(obj)) == obj?
    return False


try:
    from keyword import iskeyword  # Python 2.7+
except ImportError:

    def iskeyword(unused):
        '''Not Implemented, C{False} always.
        '''
        return False


def isLatLon(obj, ellipsoidal=None):
    '''Is B{C{obj}} some C{LatLon}?

       @arg obj: The object (any C{type}).
       @kwarg ellipsoidal: If C{None}, return the type of any C{LatLon},
                           if C{True}, only an ellipsoidal C{LatLon type}
                           or if C{False}, only a spherical C{LatLon type}.

       @return: C{type(B{obj}} if B{C{obj}} is a C{LatLon} instance of
                the required type, C{False} if a C{LatLon} of an other
                type or {None} otherwise.
    '''
    if ellipsoidal is not None:
        try:
            return obj.ellipsoidalLatLon if ellipsoidal else \
                   obj.sphericalLatLon
        except AttributeError:
            return None
    return isinstanceof(obj, _MODS.Base.latlon.LatLonBase)


def islistuple(obj, minum=0):
    '''Check for list or tuple C{type} with a minumal length.

       @arg obj: The object (any C{type}).
       @kwarg minum: Minimal C{len} required C({int}).

       @return: C{True} if B{C{obj}} is C{list} or C{tuple} with
                C{len} at least B{C{minum}}, C{False} otherwise.
    '''
    return isinstance(obj, _list_tuple_types) and len(obj) >= minum


def isNvector(obj, ellipsoidal=None):
    '''Is B{C{obj}} some C{Nvector}?

       @arg obj: The object (any C{type}).
       @kwarg ellipsoidal: If C{None}, return the type of any C{Nvector},
                           if C{True}, only an ellipsoidal C{Nvector type}
                           or if C{False}, only a spherical C{Nvector type}.

       @return: C{type(B{obj}} if B{C{obj}} is an C{Nvector} instance of
                the required type, C{False} if an C{Nvector} of an other
                type or {None} otherwise.
    '''
    if ellipsoidal is not None:
        try:
            return obj.ellipsoidalNvector if ellipsoidal else \
                   obj.sphericalNvector
        except AttributeError:
            return None
    return isinstanceof(obj, _MODS.Base.nvector.NvectorBase)


def isodd(x):
    '''Is B{C{x}} odd?

       @arg x: Value (C{scalar}).

       @return: C{True} if B{C{x}} is odd,
                C{False} otherwise.
    '''
    return bool(int(x) & 1)  # == bool(int(x) % 2)


def isscalar(obj):
    '''Check for scalar types.

       @arg obj: The object (any C{type}).

       @return: C{True} if B{C{obj}} is C{scalar}, C{False} otherwise.
    '''
    return isinstance(obj, _Scalars) and not isbool(obj)


def issequence(obj, *excls):
    '''Check for sequence types.

       @arg obj: The object (any C{type}).
       @arg excls: Classes to exclude (C{type}), all positional.

       @note: Excluding C{tuple} implies excluding C{namedtuple}.

       @return: C{True} if B{C{obj}} is a sequence, C{False} otherwise.
    '''
    return isinstance(obj, _Seqs) and not (excls and isinstance(obj, excls))


def isstr(obj):
    '''Check for string types.

       @arg obj: The object (any C{type}).

       @return: C{True} if B{C{obj}} is C{str}, C{False} otherwise.
    '''
    return isinstance(obj, _Strs)


def issubclassof(Sub, *Supers):
    '''Check whether a class is a sub-class of some other class(es).

       @arg Sub: The sub-class (C{class}).
       @arg Supers: One or more C(super) classes (C{class}).

       @return: C{True} if B{C{Sub}} is a sub-class of any B{C{Supers}},
                C{False} if not (C{bool}) or C{None} if B{C{Sub}} is not
                a class or if no B{C{Supers}} are given or none of those
                are a class.
    '''
    if isclass(Sub):
        t = tuple(S for S in Supers if isclass(S))
        if t:
            return bool(issubclass(Sub, t))
    return None


def itemsorted(adict, *items_args, **asorted_reverse):
    '''Return the items of C{B{adict}} sorted I{alphabetically,
       case-insensitively} and in I{ascending} order.

       @arg items_args: Optional positional argument(s) for method
                        C{B{adict}.items(B*{items_args})}.
       @kwarg asorted_reverse: Use keyword argument C{B{asorted}=False} for
                      I{case-sensitive} sorting and C{B{reverse}=True} for
                      results in C{descending} order.
    '''
    def _ins(item):
        return item[0].lower()

    a = _xkwds_get(asorted_reverse, asorted=True)
    r = _xkwds_get(asorted_reverse, reverse=False)
    items = adict.items(*items_args) if items_args else adict.items()
    return sorted(items, reverse=r, key=_ins if a else None)


def len2(items):
    '''Make built-in function L{len} work for generators, iterators,
       etc. since those can only be started exactly once.

       @arg items: Generator, iterator, list, range, tuple, etc.

       @return: 2-Tuple C{(n, items)} of the number of items (C{int})
                and the items (C{list} or C{tuple}).
    '''
    if not isinstance(items, _Seqs):  # NOT hasattr(items, '__len__'):
        items = list(items)
    return len(items), items


def map1(fun1, *xs):  # XXX map_
    '''Apply a single-argument function to each B{C{xs}} and
       return a C{tuple} of results.

       @arg fun1: 1-Arg function (C{callable}).
       @arg xs: Arguments (C{any positional}).

       @return: Function results (C{tuple}).
    '''
    return tuple(map(fun1, xs))


def map2(fun, *xs):
    '''Apply a function to arguments and return a C{tuple} of results.

       Unlike Python 2's built-in L{map}, Python 3+ L{map} returns a
       L{map} object, an iterator-like object which generates the
       results only once.  Converting the L{map} object to a tuple
       maintains the Python 2 behavior.

       @arg fun: Function (C{callable}).
       @arg xs: Arguments (C{list, tuple, ...}).

       @return: Function results (C{tuple}).
    '''
    return tuple(map(fun, *xs))


def neg(x, neg0=None):
    '''Negate C{x} and optionally, negate C{0.0} and C{-0.0}.

       @kwarg neg0: Defines the return value for zero C{B{x}}: if C{None}
                    return C{0.0}, if C{True} return C{NEG0 if B{x}=0.0}
                    and C{0.0 if B{x}=NEG0} or if C{False} return C{B{x}}
                    I{as-is} (C{bool} or C{None}).

       @return: C{-B{x} if B{x} else 0.0, NEG0 or B{x}}.
    '''
    return (-x) if x else (_0_0 if neg0 is None else (x if not neg0 else
                          (_0_0 if signBit(x) else _MODS.constants.NEG0)))


def neg_(*xs):
    '''Negate all C{xs} with L{neg}.

       @return: A C{map(neg, B{xs})}.
    '''
    return map(neg, xs)


def _reverange(n, stop=-1, step=-1):
    '''(INTERNAL) Reversed range yielding C{n-1, n-1-step, ..., stop+1}.
    '''
    return range(n - 1, stop, step)


def signBit(x):
    '''Return C{signbit(B{x})}, like C++.

       @return: C{True} if C{B{x} < 0} or C{NEG0} (C{bool}).
    '''
    return x < 0 or _MODS.constants.isneg0(x)


def _signOf(x, ref):  # in .maths.fsums
    '''(INTERNAL) Return the sign of B{C{x}} versus B{C{ref}}.
    '''
    return +1 if x > ref else (-1 if x < ref else 0)


def signOf(x):
    '''Return sign of C{x} as C{int}.

       @return: -1, 0 or +1 (C{int}).
    '''
    try:
        s = x.signOf()  # Fsum instance?
    except AttributeError:
        s = _signOf(x, 0)
    return s


def _sizeof(inst):
    '''(INTERNAL) Recursively size an C{inst}ance.

       @return: Instance' size in bytes (C{int}),
                ignoring class attributes and
                counting duplicates only once or
                C{None}.

       @note: With C{PyPy}, the size is always C{None}.
    '''
    try:
        _zB = _sys.getsizeof
        _zD = _zB(None)  # get some default
    except TypeError:  # PyPy3.10
        return None

    def _zR(s, iterable):
        z, _s = 0, s.add
        for o in iterable:
            i = id(o)
            if i not in s:
                _s(i)
                z += _zB(o, _zD)
                if isinstance(o, dict):
                    z += _zR(s, o.keys())
                    z += _zR(s, o.values())
                elif isinstance(o, _list_tuple_set_types):
                    z += _zR(s, o)
                else:
                    try:  # size instance' attr values only
                        z += _zR(s, o.__dict__.values())
                    except AttributeError:  # None, int, etc.
                        pass
        return z

    return _zR(set(), (inst,))


def splice(iterable, n=2, **fill):
    '''Split an iterable into C{n} slices.

       @arg iterable: Items to be spliced (C{list}, C{tuple}, ...).
       @kwarg n: Number of slices to generate (C{int}).
       @kwarg fill: Optional fill value for missing items.

       @return: A generator for each of B{C{n}} slices,
                M{iterable[i::n] for i=0..n}.

       @raise TypeError: Invalid B{C{n}}.

       @note: Each generated slice is a C{tuple} or a C{list},
              the latter only if the B{C{iterable}} is a C{list}.

       @example:

        >>> from pygeodesy3 import splice

        >>> a, b = splice(range(10))
        >>> a, b
        ((0, 2, 4, 6, 8), (1, 3, 5, 7, 9))

        >>> a, b, c = splice(range(10), n=3)
        >>> a, b, c
        ((0, 3, 6, 9), (1, 4, 7), (2, 5, 8))

        >>> a, b, c = splice(range(10), n=3, fill=-1)
        >>> a, b, c
        ((0, 3, 6, 9), (1, 4, 7, -1), (2, 5, 8, -1))

        >>> tuple(splice(list(range(9)), n=5))
        ([0, 5], [1, 6], [2, 7], [3, 8], [4])

        >>> splice(range(9), n=1)
        <generator object splice at 0x0...>
    '''
    if not isint(n):
        E = _MODS.miscs.errors._TypeError
        raise E(n=n)

    t = iterable
    if not isinstance(t, _list_tuple_types):
        t = tuple(t)  # force tuple, also for PyPy3

    if n > 1:
        if fill:
            fill = _xkwds_get(fill, fill=MISSING)
            if fill is not MISSING:
                m = len(t) % n
                if m > 0:  # same type fill
                    t += type(t)((fill,) * (n - m))
        for i in range(n):
            # XXX t[i::n] chokes PyChecker
            yield t[slice(i, None, n)]
    else:
        yield t


def _splituple(strs, *sep_splits):  # in .mgrs, .osgr, .webmercator
    '''(INTERNAL) Split a C{comma}- or C{whitespace}-separated
       string into a C{tuple} of stripped strings.
    '''
    t = (strs.split(*sep_splits) if sep_splits else
         strs.replace(_COMMA_, _SPACE_).split()) if strs else ()
    return tuple(s.strip() for s in t if s)


def unsigned0(x):
    '''Unsign if C{0.0}.

       @return: C{B{x}} if B{C{x}} else C{0.0}.
    '''
    return x if x else _0_0


def _xargs_kwds_names(func):
    '''(INTERNAL) Get a C{func}'s args and kwds names, including
       C{self} for methods.

       @note: Python 2 does I{not} include the C{*args} nor the
              C{**kwds} names.
    '''
    try:
        args_kwds = _inspect.signature(func).parameters.keys()
    except AttributeError:  # .signature new Python 3+
        args_kwds = _inspect.getargspec(func).args
    return tuple(args_kwds)


def _xAssertionError(where, *args, **kwds):
    '''(INTERNAL) Embellish an C{AssertionError}.
    '''
    t = _MODS.miscs.streprs.unstr(where, *args, **kwds)
    return _MODS.miscs.errors._AssertionError(t)


def _xattr(obj, **name_default):  # see .strerprs._xattrs
    '''(INTERNAL) Get an C{obj}'s attribute by C{name}.
    '''
    if len(name_default) == 1:
        for n, d in name_default.items():
            return getattr(obj, n, d)
    raise _xAssertionError(_xattr, obj, **name_default)


def _xcopy(inst, deep=False):
    '''(INTERNAL) Copy an object, shallow or deep.

       @arg inst: The object to copy (any C{type}).
       @kwarg deep: If C{True} make a deep, otherwise
                    a shallow copy (C{bool}).

       @return: The copy of B{C{inst}}.
    '''
    return _deepcopy(inst) if deep else _copy(inst)


def _xdup(inst, deep=False, **items):
    '''(INTERNAL) Duplicate an object, replacing some attributes.

       @arg inst: The object to copy (any C{type}).
       @kwarg deep: If C{True} copy deep, otherwise shallow.
       @kwarg items: Attributes to be changed (C{any}).

       @return: A duplicate of B{C{inst}} with modified
                attributes, if any B{C{items}}.

       @raise AttributeError: Some B{C{items}} invalid.
    '''
    d = _xcopy(inst, deep=deep)
    for n, v in items.items():
        if getattr(d, n, v) != v:
            setattr(d, n, v)
        elif not hasattr(d, n):
            t = _MODS.miscs.named.classname(inst)
            t = _SPACE_(_DOT_(t, n), _invalid_)
            E = _MODS.miscs.errors._AttributeError
            raise E(txt=t, this=inst, **items)
    return d


def _xgeographiclib(where, *required):
    '''(INTERNAL) Import C{geographiclib} and check required version.
    '''
    try:
        _xpackage(_xgeographiclib)
        import geographiclib
    except ImportError as x:
        raise _xImportError(x, where, Error=LazyImportError)
    return _xversion(geographiclib, where, *required)


def _xImportError(x, where, **Error_name):
    '''(INTERNAL) Embellish an C{Lazy/ImportError}.
    '''
    E = _MODS.miscs.errors._ImportError
    if Error_name:
        E = _xkwds_pop(Error_name, Error=E)
    t = _SPACE_(_required_, _by_, _xwhere(where, **Error_name))
    return E(_Xstr(x), txt=t, cause=x)


def _xinstanceof(*Types, **names_values):
    '''(INTERNAL) Check C{Types} of all C{name=value} pairs.

       @arg Types: One or more classes or types (C{class}), all
                   positional.
       @kwarg names_values: One or more C{B{name}=value} pairs
                            with the C{value} to be checked.

       @raise TypeError: One B{C{names_values}} pairs is not an
                         instance of any of the B{C{Types}}.
    '''
    if not (Types and names_values):
        raise _xAssertionError(_xinstanceof, *Types, **names_values)

    for n, v in names_values.items():
        if not isinstance(v, Types):
            E = _MODS.miscs.errors._TypesError
            raise E(n, v, *Types)


try:
    _ = {} | {}  # PYCHOK {}.__or__ Python 3.9+

    def _xkwds(kwds, **dflts):
        '''(INTERNAL) Override C{dflts} with specified C{kwds}.
        '''
        return (dflts | kwds) if kwds else dflts

except TypeError:

    def _xkwds(kwds, **dflts):  # PYCHOK expected
        '''(INTERNAL) Override C{dflts} with specified C{kwds}.
        '''
        d = dflts
        if kwds:
            d = _copy(d)
            d.update(kwds)
        return d


def _xkwds_get(kwds, **name_default):
    '''(INTERNAL) Get a C{kwds} value by C{name}, or the C{default}.
    '''
    if len(name_default) == 1:
        for n, d in name_default.items():
            return kwds.get(n, d)
    raise _xAssertionError(_xkwds_get, kwds, **name_default)


def _xkwds_get_(kwds, **names_defaults):
    '''(INTERNAL) Yield each C{kwds} value or its C{default}
       in I{case-insensitive, alphabetical} order.
    '''
    for n, d in itemsorted(names_defaults):
        yield kwds.get(n, d)


def _xkwds_not(*args, **kwds):
    '''(INTERNAL) Return C{kwds} with a value not in C{args}.
    '''
    return dict((n, v) for n, v in kwds.items() if v not in args)


def _xkwds_pop(kwds, **name_default):
    '''(INTERNAL) Pop a C{kwds} value by C{name}, or the C{default}.
    '''
    if len(name_default) == 1:
        for n, d in name_default.items():
            return kwds.pop(n, d)
    raise _xAssertionError(_xkwds_pop, kwds, **name_default)


def _xkwds_pop_(kwds, **names_defaults):
    '''(INTERNAL) Pop and yield each C{kwds} value or its C{default}
       in I{case-insensitive, alphabetical} order.
    '''
    for n, d in itemsorted(names_defaults):
        yield kwds.pop(n, d)


def _xkwds_popitem(name_value):
    '''(INTERNAL) Return exactly one C{(name, value)} item.
    '''
    if len(name_value) == 1:  # XXX TypeError
        return name_value.popitem()  # XXX AttributeError
    raise _xAssertionError(_xkwds_popitem, name_value)


def _xnumpy(where, *required):
    '''(INTERNAL) Import C{numpy} and check required version.
    '''
    try:
        _xpackage(_xnumpy)
        import numpy
    except ImportError as x:
        raise _xImportError(x, where)
    return _xversion(numpy, where, *required)


def _xpackage(_xpkg):
    '''(INTERNAL) Check dependency to be excluded.
    '''
    n = _xpkg.__name__[2:]  # remove _x
    if n in _XPACKAGES:
        x = _SPACE_(n, _in_, _PYGEODESY3_XPACKAGES_)
        e = _enquote(_getenv(_PYGEODESY3_XPACKAGES_, NN))
        raise ImportError(_EQUAL_(x, e))


_XPACKAGES = _splituple(_getenv(_PYGEODESY3_XPACKAGES_, NN).lower())


def _xor(x, *xs):
    '''(INTERNAL) Exclusive-or C{x} and C{xs}.
    '''
    for x_ in xs:
        x ^= x_
    return x


def _xscipy(where, *required):
    '''(INTERNAL) Import C{scipy} and check required version.
    '''
    try:
        _xpackage(_xscipy)
        import scipy
    except ImportError as x:
        raise _xImportError(x, where)
    return _xversion(scipy, where, *required)


def _xsubclassof(*Classes, **names_values):
    '''(INTERNAL) Check (super) class of all C{name=value} pairs.

       @arg Classes: One or more classes or types (C{class}), all
                     positional.
       @kwarg names_values: One or more C{B{name}=value} pairs
                            with the C{value} to be checked.

       @raise TypeError: One B{C{names_values}} pair is not a
                         (sub-)class of any of the B{C{Classes}}.
    '''
    if not (Classes and names_values):
        raise _xAssertionError(_xsubclassof, *Classes, **names_values)

    for n, v in names_values.items():
        if not issubclassof(v, *Classes):
            E = _MODS.miscs.errors._TypesError
            raise E(n, v, *Classes)


def _xversion(package, where, *required, **name):
    '''(INTERNAL) Check the C{package} version vs B{C{required}}.
    '''
    n = len(required)
    if n:
        t = _xversion_info(package)
        if t[:n] < required:
            t = _SPACE_(package.__name__, _version_, _DOT_(*t),
                       _below_, _DOT_(*required),
                       _required_, _by_, _xwhere(where, **name))
            raise ImportError(t)
    return package


def _xversion_info(package):  # in .Base.karney
    '''(INTERNAL) Get the C{package.__version_info__} as a 2- or
       3-tuple C{(major, minor, revision)} if C{int}s.
    '''
    try:
        t = package.__version_info__
    except AttributeError:
        t = package.__version__.strip()
        t = t.replace(_DOT_, _SPACE_).split()[:3]
    return map2(int, t)


def _xwhere(where, **name):
    '''(INTERNAL) Get the fully qualified name.
    '''
    m = _MODS.miscs.named.modulename(where, prefixed=True)
    if name:
        n = _xkwds_get(name, name=NN)
        if n:
            m = _DOT_(m, n)
    return m


def _xzip(*args, **strict):  # PYCHOK no cover
    '''(INTERNAL) Standard C{zip(..., strict=True)}.
    '''
    s = _xkwds_get(strict, strict=True)
    if s:
        if _zip is zip:  # < (3, 10)
            m = _MODS.miscs
            t =  m.streprs.unstr(_xzip, *args, strict=s)
            E =  m.errors._NotImplementedError
            raise E(t, txt=None)
        return _zip(*args)
    return zip(*args)


if _sys_version_info2 < (3, 10):  # see .errors
    _zip = zip  # PYCHOK exported
else:  # Python 3.10+

    def _zip(*args):
        return zip(*args, strict=True)

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
