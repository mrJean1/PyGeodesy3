
# -*- coding: utf-8 -*-

u'''(INTERNAL) Private C{CartesianBase} class for elliposiodal, spherical and N-/vectorial
C{Cartesian}s and public functions L{rtp2xyz}, L{rtp2xyz_}, L{xyz2rtp} and L{xyz2rtp_}.

After I{(C) Chris Veness 2011-2015} published under the same MIT Licence**, see
U{https://www.Movable-Type.co.UK/scripts/latlong.html},
U{https://www.Movable-Type.co.UK/scripts/latlong-vectors.html} and
U{https://www.Movable-Type.co.UK/scripts/geodesy/docs/latlon-ellipsoidal.js.html}.
'''

# from pygeodesy3.Base.nvector import _N_vector_  # _MODS
# from pygeodesy3.Base.vector3d import _xyz3  # _MODS
from pygeodesy3.basics import _xinstanceof,  _ALL_LAZY, _MODS
from pygeodesy3.constants import EPS, EPS0, INT0, PI2, _isfinite, isnear0, \
                                _0_0, _1_0, _N_1_0, _2_0, _4_0, _6_0
# from pygeodesy3.distances.resections import cassini, collins5, pierlot, tienstra7
from pygeodesy3.earth.datums import Datum, _earth_ellipsoid, _spherical_datum, \
                                    Transform, _WGS84
# from pygeodesy3.earth.ecef import EcefKarney  # MODS
# from pygeodesy3.earth.triaxials import Triaxial_ _MODS
from pygeodesy3.interns import NN, _COMMASPACE_, _phi_  # _not_
from pygeodesy3.interns import _ellipsoidal_, _spherical_  # PYCHOK used!
# from pygeodesy3.lazily import _ALL_LAZY, _ALL_MODS as _MODS  # from .basics
from pygeodesy3.maths.fmath import cbrt, hypot, hypot_, hypot2,  fabs, sqrt  # hypot
from pygeodesy3.maths.fsums import fsumf_,  Fmt
from pygeodesy3.maths.umath import acos1, sincos2d, sincos2_,  atan2, degrees, radians
from pygeodesy3.maths.vector3d import Vector3d, _xyzhdn3
from pygeodesy3.miscs.errors import _IsnotError, _TypeError, _ValueError, _xdatum, \
                                    _xkwds
from pygeodesy3.miscs.named import _NamedTuple, _Pass
from pygeodesy3.miscs.namedTuples import LatLon4Tuple, Vector3Tuple, Vector4Tuple, \
                                         Bearing2Tuple  # PYCHOK .Base.spherical
from pygeodesy3.miscs.props import Property, Property_RO, property_doc_, \
                                   property_RO, _update_all
# from pygeodesy3.miscs.streprs import Fmt  # from .maths.fsums
from pygeodesy3.miscs.units import Degrees, Height, _heigHt, _isMeter, Meter, \
                                   Radians, _toDegrees, _toRadians
# from pygeodesy3.projections.ltp import Ltp, _xLtp  # MODS

# from math import atan2, degrees, fabs, radians, sqrt  # from .fmath, .umath

__all__ = _ALL_LAZY.Base_cartesian
__version__ = '24.02.20'

_r_     = 'r'
_theta_ = 'theta'


class CartesianBase(Vector3d):
    '''(INTERNAL) Base class for ellipsoidal and spherical C{Cartesian}.
    '''
    _datum  = None  # L{Datum}, to be overriden
    _height = None  # height (L{Height}), set or approximated

    def __init__(self, x_xyz, y=None, z=None, datum=None, ll=None, name=NN):
        '''New C{Cartesian...}.

           @arg x_xyz: Cartesian X coordinate (C{scalar}) or a C{Cartesian},
                       L{Ecef9Tuple}, L{Vector3Tuple} or L{Vector4Tuple}.
           @kwarg y: Cartesian Y coordinate (C{scalar}), ignored if B{C{x_xyz}}
                     is not C{scalar}, otherwise same units as B{C{x_xyz}}.
           @kwarg z: Cartesian Z coordinate (C{scalar}), ignored if B{C{x_xyz}}
                     is not C{scalar}, otherwise same units as B{C{x_xyz}}.
           @kwarg datum: Optional datum (L{Datum}, L{Ellipsoid}, L{Ellipsoid2}
                         or L{a_f2Tuple}).
           @kwarg ll: Optional, original latlon (C{LatLon}).
           @kwarg name: Optional name (C{str}).

           @raise TypeError: Non-scalar B{C{x_xyz}}, B{C{y}} or B{C{z}} coordinate
                             or B{C{x_xyz}} not a C{Cartesian}, L{Ecef9Tuple},
                             L{Vector3Tuple} or L{Vector4Tuple} or B{C{datum}} is
                             not a L{Datum}.
        '''
        h, d, n = _xyzhdn3(x_xyz, None, datum, ll)
        Vector3d.__init__(self, x_xyz, y=y, z=z, ll=ll, name=name or n)
        if h is not None:
            self._height = Height(h)
        if d is not None:
            self.datum = d

#   def __matmul__(self, other):  # PYCHOK Python 3.5+
#       '''Return C{NotImplemented} for C{c_ = c @ datum} and C{c_ = c @ transform}.
#       '''
#       return NotImplemented if isinstance(other, (Datum, Transform)) else \
#             _NotImplemented(self, other)

    def cassini(self, pointB, pointC, alpha, beta, useZ=False):
        '''3-Point resection between this and 2 other points using U{Cassini
           <https://NL.WikiPedia.org/wiki/Achterwaartse_insnijding>}'s method.

           @arg pointB: Second point (C{Cartesian}, L{Vector3d}, C{Vector3Tuple},
                        C{Vector4Tuple} or C{Vector2Tuple} if C{B{useZ}=False}).
           @arg pointC: Center point (C{Cartesian}, L{Vector3d}, C{Vector3Tuple},
                        C{Vector4Tuple} or C{Vector2Tuple} if C{B{useZ}=False}).
           @arg alpha: Angle subtended by triangle side C{b} from B{C{pointA}} to
                       B{C{pointC}} (C{degrees}, non-negative).
           @arg beta: Angle subtended by triangle side C{a} from B{C{pointB}} to
                      B{C{pointC}} (C{degrees}, non-negative).
           @kwarg useZ: If C{True}, use and interpolate the Z component, otherwise
                        force C{z=INT0} (C{bool}).

           @note: Typically, B{C{pointC}} is between this and B{C{pointB}}.

           @return: The survey point, an instance of this (sub-)class.

           @raise ResectionError: Near-coincident, -colinear or -concyclic points
                                  or negative or invalid B{C{alpha}} or B{C{beta}}.

           @raise TypeError: Invalid B{C{pointA}}, B{C{pointB}} or B{C{pointM}}.

           @see: Function L{pygeodesy3.cassini} for references and more details.
        '''
        return self._resections.cassini(self, pointB, pointC, alpha, beta,
                                              useZ=useZ, datum=self.datum)

    def collins5(self, pointB, pointC, alpha, beta, useZ=False):
        '''3-Point resection between this and 2 other points using U{Collins<https://Dokumen.tips/
           documents/three-point-resection-problem-introduction-kaestner-burkhardt-method.html>}' method.

           @arg pointB: Second point (C{Cartesian}, L{Vector3d}, C{Vector3Tuple},
                        C{Vector4Tuple} or C{Vector2Tuple} if C{B{useZ}=False}).
           @arg pointC: Center point (C{Cartesian}, L{Vector3d}, C{Vector3Tuple},
                        C{Vector4Tuple} or C{Vector2Tuple} if C{B{useZ}=False}).
           @arg alpha: Angle subtended by triangle side C{b} from B{C{pointA}} to
                       B{C{pointC}} (C{degrees}, non-negative).
           @arg beta: Angle subtended by triangle side C{a} from B{C{pointB}} to
                      B{C{pointC}} (C{degrees}, non-negative).
           @kwarg useZ: If C{True}, use and interpolate the Z component, otherwise
                        force C{z=INT0} (C{bool}).

           @note: Typically, B{C{pointC}} is between this and B{C{pointB}}.

           @return: L{Collins5Tuple}C{(pointP, pointH, a, b, c)} with survey C{pointP},
                    auxiliary C{pointH}, each an instance of this (sub-)class and
                    triangle sides C{a}, C{b} and C{c}.

           @raise ResectionError: Near-coincident, -colinear or -concyclic points
                                  or negative or invalid B{C{alpha}} or B{C{beta}}.

           @raise TypeError: Invalid B{C{pointB}} or B{C{pointM}}.

           @see: Function L{pygeodesy3.collins5} for references and more details.
        '''
        return self._resections.collins5(self, pointB, pointC, alpha, beta,
                                               useZ=useZ, datum=self.datum)

    @property_doc_(''' this cartesian's datum (L{Datum}).''')
    def datum(self):
        '''Get this cartesian's datum (L{Datum}).
        '''
        return self._datum

    @datum.setter  # PYCHOK setter!
    def datum(self, datum):
        '''Set this cartesian's C{datum} I{without conversion}
           (L{Datum}), ellipsoidal or spherical.

           @raise TypeError: The B{C{datum}} is not a L{Datum}.
        '''
        d = _spherical_datum(datum, name=self.name)
        if self._datum:  # is not None
            if d.isEllipsoidal and not self._datum.isEllipsoidal:
                raise _IsnotError(_ellipsoidal_, datum=datum)
            elif d.isSpherical and not self._datum.isSpherical:
                raise _IsnotError(_spherical_, datum=datum)
        if self._datum != d:
            _update_all(self)
            self._datum = d

    def destinationXyz(self, delta, Cartesian=None, **Cartesian_kwds):
        '''Calculate the destination using a I{local} delta from this cartesian.

           @arg delta: Local delta to the destination (L{XyzLocal}, L{Enu},
                       L{Ned} or L{Local9Tuple}).
           @kwarg Cartesian: Optional (geocentric) class to return the
                             destination or C{None}.
           @kwarg Cartesian_kwds: Optional, additional B{C{Cartesian}} keyword
                                  arguments, ignored if C{B{Cartesian} is None}.

           @return: Destination as a C{B{Cartesian}(x, y, z, **B{Cartesian_kwds})}
                    instance or if C{B{Cartesian} is None}, an L{Ecef9Tuple}C{(x, y,
                    z, lat, lon, height, C, M, datum)} with C{M=None} always.

           @raise TypeError: Invalid B{C{delta}}, B{C{Cartesian}} or
                             B{C{Cartesian_kwds}}.
        '''
        if Cartesian is None:
            r = self._Ltp._local2ecef(delta, nine=True)
        else:
            r = self._Ltp._local2ecef(delta, nine=False)
            r = Cartesian(*r, **_xkwds(Cartesian_kwds, datum=self.datum))
        return r._xnamed(r) if self.name else r

    @property_RO
    def Ecef(self):
        '''Get the ECEF I{class} (L{EcefKarney}), I{once}.
        '''
        CartesianBase.Ecef = E = _MODS.earth.ecef.EcefKarney  # overwrite property_RO
        return E

    @Property_RO
    def _ecef9(self):
        '''(INTERNAL) Helper for L{toEcef}, L{toLocal} and L{toLtp} (L{Ecef9Tuple}).
        '''
        return self.Ecef(self.datum, name=self.name).reverse(self, M=True)

    @property_RO
    def ellipsoidalCartesian(self):
        '''Get the C{Cartesian type} iff ellipsoidal, overloaded in L{CartesianEllipsoidalBase}.
        '''
        return False

    def hartzell(self, los=True, earth=None):
        '''Compute the intersection of a Line-Of-Sight from this cartesian Point-Of-View
           (pov) and this cartesian's ellipsoid surface.

           @kwarg los: Line-Of-Sight, I{direction} to the ellipsoid (L{Los}, L{Vector3d}),
                       C{True} for the I{normal, plumb} onto the surface or I{False} or
                       C{None} to point to the center of the ellipsoid.
           @kwarg earth: The earth model (L{Datum}, L{Ellipsoid}, L{Ellipsoid2}, L{a_f2Tuple}
                         or C{scalar} radius in C{meter}), overriding this cartesian's
                         C{datum} ellipsoid.

           @return: The intersection (C{Cartesian}) with C{.height} set to the distance to
                    this C{pov}.

           @raise IntersectionError: Null or bad C{pov} or B{C{los}}, this C{pov} is inside
                                     the ellipsoid or B{C{los}} points outside or away from
                                     the ellipsoid.

           @raise TypeError: Invalid B{C{los}} or invalid or undefined B{C{earth}} or C{datum}.

           @see: Function L{hartzell<pygeodesy3.hartzell>} for further details.
        '''
        return _MODS.distances.formy._hartzell(self, los, earth)

    @Property
    def height(self):
        '''Get the height (C{meter}).
        '''
        return self._height4.h if self._height is None else self._height

    @height.setter  # PYCHOK setter!
    def height(self, height):
        '''Set the height (C{meter}).

           @raise TypeError: Invalid B{C{height}} C{type}.

           @raise ValueError: Invalid B{C{height}}.
        '''
        h = Height(height)
        if self._height != h:
            _update_all(self)
            self._height = h

    def _height2C(self, r, Cartesian=None, datum=None, height=INT0, **kwds):
        '''(INTERNAL) Helper for methods C{.height3} and C{.height4}.
        '''
        if Cartesian is not None:
            r = Cartesian(r, **kwds)
            if datum is not None:
                r.datum = datum
            if height is not None:
                r.height = height  # Height(height)
        return r

    def height3(self, earth=None, height=None, **Cartesian_and_kwds):
        '''Compute the cartesian at a height above or below this certesian's ellipsoid.

           @kwarg earth: A datum, ellipsoid, triaxial ellipsoid or earth radius,
                         I{overriding} this cartesian's datum (L{Datum}, L{Ellipsoid},
                         L{Ellipsoid2}, L{a_f2Tuple} or C{meter}, conventionally).
           @kwarg height: The height (C{meter}, conventionally), overriding this
                          cartesian's height.
           @kwarg Cartesian_and_kwds: Optional C{B{Cartesian}=None} class to return
                            the cartesian I{at height} and additional B{C{Cartesian}}
                            keyword arguments.

           @return: An instance of B{C{Cartesian}} or if C{B{Cartesian} is None},
                    a L{Vector3Tuple}C{(x, y, z)} with the C{x}, C{y} and C{z}
                    coordinates I{at height} in C{meter}, conventionally.

           @note: This cartesian's coordinates are returned if B{C{earth}} and this
                  datum or B{C{heigth}} and/or this height are C{None} or undefined.

           @note: Include keyword argument C{B{datum}=None} if class B{C{Cartesian}}
                  does not accept a B{C{datum}} keyword agument.

           @raise TriaxialError: No convergence in triaxial root finding.

           @raise TypeError: Invalid or undefined B{C{earth}} or C{datum}.
        '''
        n = self.height3.__name__
        d = self.datum if earth is None else _spherical_datum(earth, name=n)
        c, h = self, _heigHt(self, height)
        if h and d:
            R, r = self.Roc2(earth=d)
            if R > EPS0:
                R =  (R + h) / R
                r = ((r + h) / r) if r > EPS0 else _1_0
                c = c.times_(R, R, r)

        r = Vector3Tuple(c.x, c.y, c.z, name=n)
        if Cartesian_and_kwds:
            r = self._height2C(r, **_xkwds(Cartesian_and_kwds, datum=d))
        return r

    @Property_RO
    def _height4(self):
        '''(INTERNAL) Get this C{height4}-tuple.
        '''
        try:
            r = self.datum.ellipsoid.height4(self, normal=True)
        except (AttributeError, ValueError):  # no datum, null cartesian,
            r = Vector4Tuple(self.x, self.y, self.z, 0, name=self.height4.__name__)
        return r

    def height4(self, earth=None, normal=True, **Cartesian_and_kwds):
        '''Compute the projection of this point on and the height above or below
           this datum's ellipsoid surface.

           @kwarg earth: A datum, ellipsoid, triaxial ellipsoid or earth radius,
                         I{overriding} this datum (L{Datum}, L{Ellipsoid},
                         L{Ellipsoid2}, L{a_f2Tuple}, L{Triaxial}, L{Triaxial_},
                         L{JacobiConformal} or C{meter}, conventionally).
           @kwarg normal: If C{True} the projection is the nearest point on the
                          ellipsoid's surface, otherwise the intersection of the
                          radial line to the ellipsoid's center and the surface.
           @kwarg Cartesian_and_kwds: Optional C{B{Cartesian}=None} class to return
                            the I{projection} and additional B{C{Cartesian}} keyword
                            arguments.

           @return: An instance of B{C{Cartesian}} or if C{B{Cartesian} is None}, a
                    L{Vector4Tuple}C{(x, y, z, h)} with the I{projection} C{x}, C{y}
                    and C{z} coordinates and height C{h} in C{meter}, conventionally.

           @note: Include keyword argument C{B{datum}=None} if class B{C{Cartesian}}
                  does not accept a B{C{datum}} keyword agument.

           @raise TriaxialError: No convergence in triaxial root finding.

           @raise TypeError: Invalid or undefined B{C{earth}} or C{datum}.

           @see: Methods L{Ellipsoid.height4} and L{Triaxial_.height4} for more information.
        '''
        n = self.height4.__name__
        d = self.datum if earth is None else earth
        if normal and d is self.datum:
            r = self._height4
        elif isinstance(d, _MODS.earth.triaxials.Triaxial_):
            r = d.height4(self, normal=normal)
            try:
                d = d.toEllipsoid(name=n)
            except (TypeError, ValueError):  # TriaxialError
                d = None
        else:
            r = _earth_ellipsoid(d).height4(self, normal=normal)

        if Cartesian_and_kwds:
            if d and not isinstance(d, Datum):
                d = _spherical_datum(d, name=n)
            r = self._height2C(r, **_xkwds(Cartesian_and_kwds, datum=d))
        return r

    @Property_RO
    def isEllipsoidal(self):
        '''Check whether this cartesian is ellipsoidal (C{bool} or C{None} if unknown).
        '''
        return self.datum.isEllipsoidal if self._datum else None

    @Property_RO
    def isSpherical(self):
        '''Check whether this cartesian is spherical (C{bool} or C{None} if unknown).
        '''
        return self.datum.isSpherical if self._datum else None

    @Property_RO
    def latlon(self):
        '''Get this cartesian's (geodetic) lat- and longitude in C{degrees} (L{LatLon2Tuple}C{(lat, lon)}).
        '''
        return self.toEcef().latlon

    @Property_RO
    def latlonheight(self):
        '''Get this cartesian's (geodetic) lat-, longitude in C{degrees} with height (L{LatLon3Tuple}C{(lat, lon, height)}).
        '''
        return self.toEcef().latlonheight

    @Property_RO
    def latlonheightdatum(self):
        '''Get this cartesian's (geodetic) lat-, longitude in C{degrees} with height and datum (L{LatLon4Tuple}C{(lat, lon, height, datum)}).
        '''
        return self.toEcef().latlonheightdatum

    @property_RO
    def _ltp(self):
        '''(INTERNAL) Get module C{.projections.ltp}, I{once}.
        '''
        CartesianBase._ltp = m = _MODS.projections.ltp  # overwrite property_RO
        return m

    @Property_RO
    def _Ltp(self):
        '''(INTERNAL) Cache for L{toLtp}.
        '''
        return self._ltp.Ltp(self._ecef9, ecef=self.Ecef(self.datum), name=self.name)

    @Property_RO
    def _N_vector(self):
        '''(INTERNAL) Get the (C{Base.nvector._N_vector_}).
        '''
        m = _MODS.Base.nvector
        x, y, z, h = self._n_xyzh4(self.datum)
        return m._N_vector_(x, y, z, h=h, name=self.name)

    def _n_xyzh4(self, datum):
        '''(INTERNAL) Get the n-vector components as L{Vector4Tuple}.
        '''
        def _ErrorEPS0(x):
            return _ValueError(origin=self, txt=Fmt.PARENSPACED(EPS0=x))

        _xinstanceof(Datum, datum=datum)
        # <https://www.Movable-Type.co.UK/scripts/geodesy/docs/
        #        latlon-nvector-ellipsoidal.js.html#line309>,
        # <https://GitHub.com/pbrod/nvector>/src/nvector/core.py>
        # _equation23 and <https://www.NavLab.net/nvector>
        E = datum.ellipsoid
        x, y, z = self.xyz

        # Kenneth Gade eqn 23
        p = hypot2(x, y) * E.a2_
        q = z**2 * E.e21 * E.a2_
        r = fsumf_(p, q, -E.e4) / _6_0
        s = (p * q * E.e4) / (_4_0 * r**3)
        t = cbrt(fsumf_(_1_0, s, sqrt(s * (_2_0 + s))))
        if isnear0(t):
            raise _ErrorEPS0(t)
        u = fsumf_(_1_0, t, _1_0 / t) * r
        v = sqrt(u**2 + E.e4 * q)
        t = v * _2_0
        if t < EPS0:  # isnear0
            raise _ErrorEPS0(t)
        w = fsumf_(u, v, -q) * E.e2 / t
        k = sqrt(fsumf_(u, v, w**2)) - w
        if isnear0(k):
            raise _ErrorEPS0(k)
        t = k + E.e2
        if isnear0(t):
            raise _ErrorEPS0(t)
        e = k / t
#       d = e * hypot(x, y)
#       tmp = 1 / hypot(d, z) == 1 / hypot(e * hypot(x, y), z)
        t = hypot_(x * e, y * e, z)  # == 1 / tmp
        if t < EPS0:  # isnear0
            raise _ErrorEPS0(t)
        h = fsumf_(k, E.e2, _N_1_0) / k * t
        s = e / t  # == e * tmp
        return Vector4Tuple(x * s, y * s, z / t, h, name=self.name)

    @Property_RO
    def philam(self):
        '''Get this cartesian's (geodetic) lat- and longitude in C{radians} (L{PhiLam2Tuple}C{(phi, lam)}).
        '''
        return self.toEcef().philam

    @Property_RO
    def philamheight(self):
        '''Get this cartesian's (geodetic) lat-, longitude in C{radians} with height (L{PhiLam3Tuple}C{(phi, lam, height)}).
        '''
        return self.toEcef().philamheight

    @Property_RO
    def philamheightdatum(self):
        '''Get this cartesian's (geodetic) lat-, longitude in C{radians} with height and datum (L{PhiLam4Tuple}C{(phi, lam, height, datum)}).
        '''
        return self.toEcef().philamheightdatum

    def pierlot(self, point2, point3, alpha12, alpha23, useZ=False, eps=EPS):
        '''3-Point resection between this and two other points using U{Pierlot
           <http://www.Telecom.ULg.ac.Be/triangulation>}'s method C{ToTal} with
           I{approximate} limits for the (pseudo-)singularities.

           @arg point2: Second point (C{Cartesian}, L{Vector3d}, C{Vector3Tuple},
                        C{Vector4Tuple} or C{Vector2Tuple} if C{B{useZ}=False}).
           @arg point3: Third point (C{Cartesian}, L{Vector3d}, C{Vector3Tuple},
                        C{Vector4Tuple} or C{Vector2Tuple} if C{B{useZ}=False}).
           @arg alpha12: Angle subtended from this point to B{C{point2}} or
                         B{C{alpha2 - alpha}} (C{degrees}).
           @arg alpha23: Angle subtended from B{C{point2}} to B{C{point3}} or
                         B{C{alpha3 - alpha2}} (C{degrees}).
           @kwarg useZ: If C{True}, interpolate the Z component, otherwise use C{z=INT0}
                        (C{bool}).
           @kwarg eps: Tolerance for C{cot} (pseudo-)singularities (C{float}).

           @note: This point, B{C{point2}} and B{C{point3}} are ordered counter-clockwise.

           @return: The survey (or robot) point, an instance of this (sub-)class.

           @raise ResectionError: Near-coincident, -colinear or -concyclic points
                                  or invalid B{C{alpha12}} or B{C{alpha23}}.

           @raise TypeError: Invalid B{C{point2}} or B{C{point3}}.

           @see: Function L{pygeodesy3.pierlot} for references and more details.
        '''
        return self._resections.pierlot(self, point2, point3, alpha12, alpha23,
                                              useZ=useZ, eps=eps, datum=self.datum)

    def pierlotx(self, point2, point3, alpha1, alpha2, alpha3, useZ=False):
        '''3-Point resection between this and two other points using U{Pierlot
           <http://www.Telecom.ULg.ac.Be/publi/publications/pierlot/Pierlot2014ANewThree>}'s
           method C{ToTal} with I{exact} limits for the (pseudo-)singularities.

           @arg point2: Second point (C{Cartesian}, L{Vector3d}, C{Vector3Tuple},
                        C{Vector4Tuple} or C{Vector2Tuple} if C{B{useZ}=False}).
           @arg point3: Third point (C{Cartesian}, L{Vector3d}, C{Vector3Tuple},
                        C{Vector4Tuple} or C{Vector2Tuple} if C{B{useZ}=False}).
           @arg alpha1: Angle at B{C{point1}} (C{degrees}).
           @arg alpha2: Angle at B{C{point2}} (C{degrees}).
           @arg alpha3: Angle at B{C{point3}} (C{degrees}).
           @kwarg useZ: If C{True}, interpolate the survey point's Z component,
                        otherwise use C{z=INT0} (C{bool}).

           @return: The survey (or robot) point, an instance of this (sub-)class.

           @raise ResectionError: Near-coincident, -colinear or -concyclic points or
                                  invalid B{C{alpha1}}, B{C{alpha2}} or B{C{alpha3}}.

           @raise TypeError: Invalid B{C{point2}} or B{C{point3}}.

           @see: Function L{pygeodesy3.pierlotx} for references and more details.
        '''
        return self._resections.pierlotx(self, point2, point3, alpha1, alpha2, alpha3,
                                               useZ=useZ, datum=self.datum)

    @property_RO
    def _resections(self):
        '''(INTERNAL) Import the C{.distances.resections} module, I{once}.
        '''
        CartesianBase._resections = r = _MODS.distances.resections  # overwrite property_RO
        return r

    def Roc2(self, earth=None):
        '''Compute this cartesian's I{normal} and I{pseudo, z-based} radius of curvature.

           @kwarg earth: A datum, ellipsoid, triaxial ellipsoid or earth radius,
                         I{overriding} this cartesian's datum (L{Datum}, L{Ellipsoid},
                         L{Ellipsoid2}, L{a_f2Tuple} or C{meter}, conventionally).

           @return: 2-Tuple C{(R, r)} with the I{normal} and I{pseudo, z-based} radius of
                    curvature C{R} respectively C{r}, both in C{meter} conventionally.

           @raise TypeError: Invalid or undefined B{C{earth}} or C{datum}.
        '''
        r = z = fabs( self.z)
        R, _0 = hypot(self.x, self.y), EPS0
        if R < _0:  # polar
            R = z
        elif z > _0:  # non-equatorial
            d = self.datum if earth is None else _spherical_datum(earth)
            e = self.toLatLon(datum=d, height=0, LatLon=None)  # Ecef9Tuple
            M = e.M  # EcefMatrix
            sa, ca = map(fabs, (M._2_2_, M._2_1_) if M else sincos2d(e.lat))
            if ca < _0:  # polar
                R = z
            else:  # prime-vertical, normal roc R
                R = R / ca  # /= chokes PyChecker
                r = R if sa < _0 else (r / sa)  # non-/equatorial
        return R, r

    @property_RO
    def sphericalCartesian(self):
        '''Get the C{Cartesian type} iff spherical, overloaded in L{CartesianSphericalBase}.
        '''
        return False

    def tienstra7(self, pointB, pointC, alpha, beta=None, gamma=None, useZ=False):
        '''3-Point resection between this and two other points using U{Tienstra
           <https://WikiPedia.org/wiki/Tienstra_formula>}'s formula.

           @arg pointB: Second point (C{Cartesian}, L{Vector3d}, C{Vector3Tuple}, C{Vector4Tuple} or
                        C{Vector2Tuple} if C{B{useZ}=False}).
           @arg pointC: Third point (C{Cartesian}, L{Vector3d}, C{Vector3Tuple}, C{Vector4Tuple} or
                        C{Vector2Tuple} if C{B{useZ}=False}).
           @arg alpha: Angle subtended by triangle side C{a} from B{C{pointB}} to B{C{pointC}} (C{degrees},
                       non-negative).
           @kwarg beta: Angle subtended by triangle side C{b} from this to B{C{pointC}} (C{degrees},
                        non-negative) or C{None} if C{B{gamma} is not None}.
           @kwarg gamma: Angle subtended by triangle side C{c} from this to B{C{pointB}} (C{degrees},
                         non-negative) or C{None} if C{B{beta} is not None}.
           @kwarg useZ: If C{True}, use and interpolate the Z component, otherwise force C{z=INT0}
                        (C{bool}).

           @note: This point, B{C{pointB}} and B{C{pointC}} are ordered clockwise.

           @return: L{Tienstra7Tuple}C{(pointP, A, B, C, a, b, c)} with survey C{pointP},
                    an instance of this (sub-)class and triangle angle C{A} at this point,
                    C{B} at B{C{pointB}} and C{C} at B{C{pointC}} in C{degrees} and
                    triangle sides C{a}, C{b} and C{c}.

           @raise ResectionError: Near-coincident, -colinear or -concyclic points or sum of
                                  B{C{alpha}}, B{C{beta}} and B{C{gamma}} not C{360} or
                                  negative B{C{alpha}}, B{C{beta}} or B{C{gamma}}.

           @raise TypeError: Invalid B{C{pointB}} or B{C{pointC}}.

           @see: Function L{pygeodesy3.tienstra7} for references and more details.
        '''
        return self._resections.tienstra7(self, pointB, pointC, alpha, beta, gamma,
                                                useZ=useZ, datum=self.datum)

#   def _to3LLh(self, datum, LL, **pairs):  # OBSOLETE
#       '''(INTERNAL) Helper for C{subclass.toLatLon} and C{.to3llh}.
#       '''
#       r = self.to3llh(datum)  # LatLon3Tuple
#       if LL is not None:
#           r = LL(r.lat, r.lon, height=r.height, datum=datum, name=self.name)
#           for n, v in pairs.items():
#               setattr(r, n, v)
#       return r

    def toDatum(self, datum2, datum=None):
        '''Convert this cartesian from one datum to an other.

           @arg datum2: Datum to convert I{to} (L{Datum}).
           @kwarg datum: Datum to convert I{from} (L{Datum}).

           @return: The converted point (C{Cartesian}).

           @raise TypeError: B{C{datum2}} or B{C{datum}}
                             invalid.
        '''
        _xinstanceof(Datum, datum2=datum2)

        c = self if datum in (None, self.datum) else \
            self.toDatum(datum)

        i, d = False, c.datum
        if d == datum2:
            return c.copy() if c is self else c

        elif datum2.transform.isunity and \
                  d.transform.isunity:
            return c.dup(datum=datum2)

        elif d == _WGS84:
            d = datum2  # convert from WGS84 to datum2

        elif datum2 == _WGS84:
            i = True  # convert to WGS84 by inverse transformation

        else:  # neither datum2 nor c.datum is WGS84, invert to WGS84 first
            c = c.toTransform(d.transform, inverse=True, datum=_WGS84)
            d = datum2

        return c.toTransform(d.transform, inverse=i, datum=datum2)

    convertDatum = toDatum  # for backward compatibility

    def toEcef(self):
        '''Convert this cartesian to I{geodetic} (lat-/longitude) coordinates.

           @return: An L{Ecef9Tuple}C{(x, y, z, lat, lon, height,
                    C, M, datum)} with C{C} and C{M} if available.

           @raise EcefError: A C{.datum} or an ECEF issue.
        '''
        return self._ecef9

    def toLatLon(self, datum=None, height=None, LatLon=None, **LatLon_kwds):  # see .ecef.Ecef9Tuple.toDatum
        '''Convert this cartesian to a I{geodetic} (lat-/longitude) point.

           @kwarg datum: Optional datum (L{Datum}, L{Ellipsoid}, L{Ellipsoid2}
                         or L{a_f2Tuple}).
           @kwarg height: Optional height, overriding the converted height
                          (C{meter}), iff B{C{LatLon}} is not C{None}.
           @kwarg LatLon: Optional class to return the geodetic point
                          (C{LatLon}) or C{None}.
           @kwarg LatLon_kwds: Optional, additional B{C{LatLon}} keyword
                               arguments, ignored if C{B{LatLon} is None}.

           @return: The geodetic point (B{C{LatLon}}) or if B{C{LatLon}}
                    is C{None}, an L{Ecef9Tuple}C{(x, y, z, lat, lon,
                    height, C, M, datum)} with C{C} and C{M} if available.

           @raise TypeError: Invalid B{C{datum}} or B{C{LatLon_kwds}}.
        '''
        d = _spherical_datum(datum or self.datum, name=self.name)
        if d == self.datum:
            r = self.toEcef()
        else:
            c = self.toDatum(d)
            r = c.Ecef(d, name=self.name).reverse(c, M=LatLon is None)

        if LatLon:  # class or .classof
            h = _heigHt(r, height)
            r =  LatLon(r.lat, r.lon, datum=r.datum, height=h,
                                   **_xkwds(LatLon_kwds, name=r.name))
        _xdatum(r.datum, d)
        return r

    def toLocal(self, Xyz=None, ltp=None, **Xyz_kwds):
        '''Convert this I{geocentric} cartesian to I{local} C{X}, C{Y} and C{Z}.

           @kwarg Xyz: Optional class to return C{X}, C{Y} and C{Z}
                       (L{XyzLocal}, L{Enu}, L{Ned}) or C{None}.
           @kwarg ltp: The I{local tangent plane} (LTP) to use,
                       overriding this cartesian's LTP (L{Ltp}).
           @kwarg Xyz_kwds: Optional, additional B{C{Xyz}} keyword
                            arguments, ignored if C{B{Xyz} is None}.

           @return: An B{C{Xyz}} instance or if C{B{Xyz} is None},
                    a L{Local9Tuple}C{(x, y, z, lat, lon, height,
                    ltp, ecef, M)} with C{M=None} always.

           @raise TypeError: Invalid B{C{ltp}}.
        '''
        p = self._ltp._xLtp(ltp, self._Ltp)
        return p._ecef2local(self._ecef9, Xyz, Xyz_kwds)

    def toLtp(self, Ecef=None):
        '''Return the I{local tangent plane} (LTP) for this cartesian.

           @kwarg Ecef: Optional ECEF I{class} (L{EcefKarney}, ...
                        L{EcefYou}), overriding this cartesian's C{Ecef}.
        '''
        return self._Ltp if Ecef in (None, self.Ecef) else self._ltp.Ltp(
               self._ecef9, ecef=Ecef(self.datum), name=self.name)

    def toNvector(self, Nvector=None, datum=None, **Nvector_kwds):
        '''Convert this cartesian to C{n-vector} components, I{including height}.

           @kwarg Nvector: Optional class to return the C{n-vector} components
                           (C{Nvector}) or C{None}.
           @kwarg datum: Optional datum (L{Datum}, L{Ellipsoid}, L{Ellipsoid2}
                         or L{a_f2Tuple}) overriding this cartesian's datum.
           @kwarg Nvector_kwds: Optional, additional B{C{Nvector}} keyword
                                arguments, ignored if C{B{Nvector} is None}.

           @return: An B{C{Nvector}} or a L{Vector4Tuple}C{(x, y, z, h)} if
                    B{C{Nvector}} is C{None}.

           @raise TypeError: Invalid B{C{Nvector}}, B{C{Nvector_kwds}} or
                             B{C{datum}}.

           @raise ValueError: B{C{Cartesian}} at origin.
        '''
        r, d = self._N_vector.xyzh, self.datum
        if datum is not None:
            d = _spherical_datum(datum, name=self.name)
            if d != self.datum:
                r = self._n_xyzh4(d)

        if Nvector is not None:
            kwds = _xkwds(Nvector_kwds, h=r.h, datum=d)
            r = self._xnamed(Nvector(r.x, r.y, r.z, **kwds))
        return r

    def toRtp(self):
        '''Convert this cartesian to I{spherical, polar} coordinates.

           @return: L{RadiusThetaPhi3Tuple}C{(r, theta, phi)} with C{theta}
                    and C{phi}, both in L{Degrees}.

           @see: Function L{xyz2rtp_} and class L{RadiusThetaPhi3Tuple}.
        '''
        return _rtp3(self.toRtp, Degrees, self, name=self.name)

    def toStr(self, prec=3, fmt=Fmt.SQUARE, sep=_COMMASPACE_):  # PYCHOK expected
        '''Return the string representation of this cartesian.

           @kwarg prec: Number of (decimal) digits, unstripped (C{int}).
           @kwarg fmt: Enclosing backets format (C{letter}).
           @kwarg sep: Separator to join (C{str}).

           @return: Cartesian represented as "[x, y, z]" (C{str}).
        '''
        return Vector3d.toStr(self, prec=prec, fmt=fmt, sep=sep)

    def toTransform(self, transform, inverse=False, datum=None):
        '''Apply a Helmert transform to this cartesian.

           @arg transform: Transform to apply (L{Transform} or L{TransformXform}).
           @kwarg inverse: Apply the inverse of the C{B{transform}} (C{bool}).
           @kwarg datum: Datum for the transformed cartesian (L{Datum}), overriding
                         this cartesian's datum but I{not} taking it into account.

           @return: A transformed cartesian (C{Cartesian}) or a copy of this
                    cartesian if C{B{transform}.isunity}.

           @raise TypeError: Invalid B{C{transform}}.
        '''
        _xinstanceof(Transform, transform=transform)
        if transform.isunity:
            c = self.dup(datum=datum or self.datum)
        else:
            # if inverse and d != _WGS84:
            #     raise _ValueError(inverse=inverse, datum=d,
            #                       txt=_not_(_WGS84.name))
            xyz = transform.transform(*self.xyz, inverse=inverse)
            c = self.dup(xyz=xyz, datum=datum or self.datum)
        return c

    def toVector(self, Vector=None, **Vector_kwds):
        '''Return this cartesian's I{geocentric} components as vector.

           @kwarg Vector: Optional class to return the I{geocentric}
                          components (L{Vector3d}) or C{None}.
           @kwarg Vector_kwds: Optional, additional B{C{Vector}} keyword
                               arguments, ignored if C{B{Vector} is None}.

           @return: A B{C{Vector}} or a L{Vector3Tuple}C{(x, y, z)} if
                    B{C{Vector}} is C{None}.

           @raise TypeError: Invalid B{C{Vector}} or B{C{Vector_kwds}}.
        '''
        return self.xyz if Vector is None else self._xnamed(
               Vector(self.x, self.y, self.z, **Vector_kwds))


class RadiusThetaPhi3Tuple(_NamedTuple):
    '''3-Tuple C{(r, theta, phi)} with radial distance C{r} in C{meter}, inclination
       C{theta} (with respect to the positive z-axis) and azimuthal angle C{phi} in
       L{Degrees} I{or} L{Radians} representing a U{spherical, polar position
       <https://WikiPedia.org/wiki/Spherical_coordinate_system>}.
    '''
    _Names_ = (_r_,    _theta_, _phi_)
    _Units_ = ( Meter, _Pass,   _Pass)

    def toCartesian(self, name=NN, **Cartesian_and_kwds):
        '''Convert this L{RadiusThetaPhi3Tuple} to a cartesian C{(x, y, z)} vector.

           @kwarg name: Optional name (C{str}), overriding this name.
           @kwarg Cartesian_and_kwds: Optional C{B{Cartesian}=None} class and additional
                            C{B{Cartesian}} keyword arguments.

           @return: A C{B{Cartesian}(x, y, z)} instance or if no C{B{Cartesian}} keyword
                    argument is given, a L{Vector3Tuple}C{(x, y, z)} with C{x}, C{y}
                    and C{z} in the same units as radius C{r}, C{meter} conventionally.

           @see: Function L{rtp2xyz_}.
        '''
        r, t, p =  self
        t, p, _ = _toRadians(self, t, p)
        return rtp2xyz_(r, t, p, name=name or self.name, **Cartesian_and_kwds)

    def toDegrees(self, name=NN):
        '''Convert this L{RadiusThetaPhi3Tuple}'s angles to L{Degrees}.

           @kwarg name: Optional name (C{str}), overriding this name.

           @return: L{RadiusThetaPhi3Tuple}C{(r, theta, phi)} with C{theta}
                    and C{phi} both in L{Degrees}.
        '''
        r, t, p =  self
        t, p, _ = _toDegrees(self, t, p)
        return _ or self.classof(r, Degrees(theta=t), Degrees(phi=p),
                                    name=name or self.name)

    def toRadians(self, name=NN):
        '''Convert this L{RadiusThetaPhi3Tuple}'s angles to L{Radians}.

           @kwarg name: Optional name (C{str}), overriding this name.

           @return: L{RadiusThetaPhi3Tuple}C{(r, theta, phi)} with C{theta}
                    and C{phi} both in L{Radians}.
        '''
        r, t, p =  self
        t, p, _ = _toRadians(self, t, p)
        return _ or self.classof(r, Radians(theta=t), Radians(phi=p),
                                    name=name or self.name)


def rtp2xyz(r_rtp, *theta_phi, **name_Cartesian_and_kwds):
    '''Convert I{spherical, polar} C{(r, theta, phi)} to cartesian C{(x, y, z)} coordinates.

       @arg r_rtp: Radial distance (C{scalar}, conventially C{meter}) or a previous
                   L{RadiusThetaPhi3Tuple} instance.
       @arg theta_phi: Inclination B{C{theta}} (C{degrees} with respect to the positive z-axis)
                       and azimuthal angle B{C{phi}} (C{degrees}), ignored if C{B{r_rtp}} is a
                       L{RadiusThetaPhi3Tuple}.
       @kwarg name_Cartesian_and_kwds: Optional C{B{name}=NN} (C{str}), a C{B{Cartesian}=None}
                             class to return the coordinates and additional C{B{Cartesian}}
                             keyword arguments.

       @return: A C{B{Cartesian}(x, y, z)} instance or if no C{B{Cartesian}} keyword argument
                is given a L{Vector3Tuple}C{(x, y, z)}, with C{x}, C{y} and C{z} in the same
                units as radius C{r}, C{meter} conventionally.

       @raise TypeError: Invalid B{C{r_rtp}}.

       @see: Functions L{rtp2xyz_} and L{xyz2rtp}.
    '''
    if isinstance(r_rtp, RadiusThetaPhi3Tuple):
        c = r_rtp.toCartesian(**name_Cartesian_and_kwds)
    else:
        c = rtp2xyz_(r_rtp, *map(radians, theta_phi), **name_Cartesian_and_kwds)
    return c


def rtp2xyz_(r_rtp, *theta_phi, **name_Cartesian_and_kwds):
    '''Convert I{spherical, polar} C{(r, theta, phi)} to cartesian C{(x, y, z)} coordinates.

       @arg r_rtp: Radial distance (C{scalar}, conventially C{meter}) or a previous
                   L{RadiusThetaPhi3Tuple} instance.
       @arg theta_phi: Inclination B{C{theta}} (C{radians} with respect to the positive z-axis)
                       and azimuthal angle B{C{phi}} (C{degrees}), ignored is C{B{r_rtp}} is a
                       L{RadiusThetaPhi3Tuple}.
       @kwarg name_Cartesian_and_kwds: Optional C{B{name}=NN} (C{str}), a C{B{Cartesian}=None}
                             class to return the coordinates and additional C{B{Cartesian}}
                             keyword arguments.

       @return: A C{B{Cartesian}(x, y, z)} instance or if no C{B{Cartesian}} keyword argument
                is given a L{Vector3Tuple}C{(x, y, z)}, with C{x}, C{y} and C{z} in the same
                units as radius C{r}, C{meter} conventionally.

       @raise TypeError: Invalid B{C{r_rtp}} or B{C{theta_phi}}.

       @see: U{Physics convention<https://WikiPedia.org/wiki/Spherical_coordinate_system>}
             (ISO 80000-2:2019).
    '''
    if _isMeter(r_rtp) and len(theta_phi) == 2:
        r = r_rtp
        if r and _isfinite(r):
            s, z, y, x = sincos2_(*theta_phi)
            s *= r
            z *= r
            y *= s
            x *= s
        else:
            x = y = z = r

        def _n_C_kwds3(name=NN, Cartesian=None, **kwds):
            return name, Cartesian, kwds

        n, C, kwds = _n_C_kwds3(**name_Cartesian_and_kwds)
        c = Vector3Tuple(x, y, z, name=n) if C is None else \
                       C(x, y, z, name=n, **kwds)

    elif isinstance(r_rtp, RadiusThetaPhi3Tuple):
        c = r_rtp.toCartesian(**name_Cartesian_and_kwds)
    else:
        raise _TypeError(r_rtp=r_rtp, theta_phi=theta_phi)
    return c


def _rtp3(where, Unit, *x_y_z, **name):
    '''(INTERNAL) Helper for C{.toRtp}, C{xyz2rtp} and C{xyz2rtp_}.
    '''
    x, y, z = _MODS.Base.vector3d._xyz3(where, *x_y_z)
    r = hypot_(x, y, z)
    if r > 0:
        t = acos1(z / r)
        p = atan2(y, x)
        while p < 0:
            p += PI2
        if Unit is Degrees:
            t = degrees(t)
            p = degrees(p)
    else:
        t = p = _0_0
    return RadiusThetaPhi3Tuple(r, Unit(theta=t), Unit(phi=p), **name)


def xyz2rtp(x_xyz, *y_z, **name):
    '''Convert cartesian C{(x, y, z)} to I{spherical, polar} C{(r, theta, phi)} coordinates.

       @return: L{RadiusThetaPhi3Tuple}C{(r, theta, phi)} with C{theta} and C{phi},
                both in L{Degrees}.

       @see: Function L{xyz2rtp_} and class L{RadiusThetaPhi3Tuple}.
    '''
    return _rtp3(xyz2rtp, Degrees, x_xyz, *y_z, **name)


def xyz2rtp_(x_xyz, *y_z, **name):
    '''Convert cartesian C{(x, y, z)} to I{spherical, polar} C{(r, theta, phi)} coordinates.

       @arg x_xyz: X component (C{scalar}) or a cartesian (C{Cartesian}, L{Ecef9Tuple},
                   C{Nvector}, L{Vector3d}, L{Vector3Tuple}, L{Vector4Tuple} or a
                   C{tuple} or C{list} of 3+ C{scalar} items) if no C{y_z} specified.
       @arg y_z: Y and Z component (C{scalar}s), ignored if C{x_xyz} is not a C{scalar}.
       @kwarg name: Optional C{B{name}=NN} (C{str}).

       @return: L{RadiusThetaPhi3Tuple}C{(r, theta, phi)} with radial distance C{r}
                (C{meter}, same units as C{x}, C{y} and C{z}), inclination C{theta}
                (with respect to the positive z-axis) and azimuthal angle C{phi},
                both in L{Radians}.

       @see: U{Physics convention<https://WikiPedia.org/wiki/Spherical_coordinate_system>}
             (ISO 80000-2:2019).
    '''
    return _rtp3(xyz2rtp_, Radians, x_xyz, *y_z, **name)


# __all__ += _ALL_DOCS(CartesianBase)

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
