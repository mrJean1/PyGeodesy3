
# -*- coding: utf-8 -*-

u'''(INTERNAL) Private base classes for elliposiodal, spherical and N-/vectorial
C{Cartesian}s.

After I{(C) Chris Veness 2011-2015} published under the same MIT Licence**,
see U{https://www.Movable-Type.co.UK/scripts/latlong.html},
U{https://www.Movable-Type.co.UK/scripts/latlong-vectors.html} and
U{https://www.Movable-Type.co.UK/scripts/geodesy/docs/latlon-ellipsoidal.js.html}.
'''

# from pygeodesy3.Base.nvector import _N_vector_  # _MODS
from pygeodesy3.basics import _xinstanceof, _xkwds
from pygeodesy3.constants import EPS, EPS0, isnear0, _1_0, _N_1_0, \
                                _2_0, _4_0, _6_0
from pygeodesy3.earth.datums import Datum, _earth_ellipsoid, _spherical_datum, \
                                   _WGS84
# from pygeodesy3.earth.ecef import EcefKarney  # MODS
# from pygeodesy3.earth.triaxials import Triaxial_ _MODS
from pygeodesy3.miscs.errors import _IsnotError, _ValueError, _xdatum
from pygeodesy3.interns import NN, _COMMASPACE_, _height_, _not_
from pygeodesy3.interns import _ellipsoidal_, _spherical_  # PYCHOK used!
from pygeodesy3.lazily import _ALL_LAZY, _ALL_MODS as _MODS
from pygeodesy3.maths.fmath import cbrt, hypot_, hypot2, sqrt  # hypot
from pygeodesy3.maths.fsums import Fmt, fsumf_
from pygeodesy3.maths.vector3d import Vector3d, _xyzhdn3
from pygeodesy3.miscs.namedTuples import LatLon4Tuple, Vector4Tuple, \
                                         Bearing2Tuple  # PYCHOK .base.spherical
from pygeodesy3.miscs.props import Property, Property_RO, property_doc_, \
                                   property_RO, _update_all
# from pygeodesy3.distances.resections import cassini, collins5, pierlot, tienstra7
# from pygeodesy3.miscs.streprs import Fmt  # from .maths.fsums
from pygeodesy3.miscs.units import Height, _heigHt
# from pygeodesy3.projections.ltp import Ltp, _xLtp  # MODS

# from math import sqrt  # from .fmath

__all__ = _ALL_LAZY.Base_cartesian
__version__ = '24.01.05'


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

           @raise TypeError: Non-scalar B{C{x_xyz}}, B{C{y}} or B{C{z}}
                             coordinate or B{C{x_xyz}} not an L{Ecef9Tuple},
                             L{Vector3Tuple} or L{Vector4Tuple}.
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

    def hartzell(self, los=None, earth=None):
        '''Compute the intersection of a Line-Of-Sight (los) from this cartesian
           Point-Of-View (pov) with this cartesian's ellipsoid surface.

           @kwarg los: Line-Of-Sight, I{direction} to earth (L{Los}, L{Vector3d})
                       or C{None} to point to the ellipsoid's center.
           @kwarg earth: The earth model (L{Datum}, L{Ellipsoid}, L{Ellipsoid2},
                         L{a_f2Tuple} or C{scalar} radius in C{meter}) overriding
                         this cartesian's C{datum} ellipsoid.

           @return: The ellipsoid intersection (C{Cartesian}) with C{.height} set
                    to the distance to this C{pov}.

           @raise IntersectionError: Null or bad C{pov} or B{C{los}}, this C{pov}
                                     is inside the ellipsoid or B{C{los}} points
                                     outside or away from the ellipsoid.

           @raise TypeError: Invalid B{C{los}} or no B{C{datum}}.

           @see: Function C{hartzell} for further details.
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

    @Property_RO
    def _height4(self):
        '''(INTERNAL) Get this C{height4}-tuple.
        '''
        try:
            r = self.datum.ellipsoid.height4(self, normal=True)
        except (AttributeError, ValueError):  # no datum, null cartesian,
            r = Vector4Tuple(self.x, self.y, self.z, 0, name=self.height4.__name__)
        return r

    def height4(self, earth=None, normal=True, Cartesian=None, **Cartesian_kwds):
        '''Compute the height of this cartesian above or below and the projection
           on this datum's ellipsoid surface.

           @kwarg earth: A datum, ellipsoid, triaxial ellipsoid or earth radius
                         I{overriding} this datum (L{Datum}, L{Ellipsoid},
                         L{Ellipsoid2}, L{a_f2Tuple}, L{Triaxial}, L{Triaxial_},
                         L{JacobiConformal} or C{meter}, conventionally).
           @kwarg normal: If C{True} the projection is the nearest point on the
                          ellipsoid's surface, otherwise the intersection of the
                          radial line to the center and the ellipsoid's surface.
           @kwarg Cartesian: Optional class to return the height and projection
                             (C{Cartesian}) or C{None}.
           @kwarg Cartesian_kwds: Optional, additional B{C{Cartesian}} keyword
                                  arguments, ignored if C{B{Cartesian} is None}.

           @note: Use keyword argument C{height=0} to override C{B{Cartesian}.height}
                  to {0} or any other C{scalar}, conventionally in C{meter}.

           @return: An instance of B{C{Cartesian}} or if C{B{Cartesian} is None}, a
                    L{Vector4Tuple}C{(x, y, z, h)} with the I{projection} C{x}, C{y}
                    and C{z} coordinates and height C{h} in C{meter}, conventionally.

           @raise TriaxialError: No convergence in triaxial root finding.

           @raise TypeError: Invalid B{C{earth}}.

           @see: L{Ellipsoid.height4} and L{Triaxial_.height4} for more information.
        '''
        d = self.datum if earth is None else earth
        if normal and d is self.datum:
            r =  self._height4
        elif isinstance(d, _MODS.earth.triaxials.Triaxial_):
            r =  d.height4(self, normal=normal)
        else:
            r = _earth_ellipsoid(d).height4(self, normal=normal)
        if Cartesian is not None:
            kwds = Cartesian_kwds.copy()
            h = kwds.pop(_height_, None)
            r = Cartesian(r, **kwds)
            if h is not None:
                r.height = Height(height=h)
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
        '''(INTERNAL) Get the (C{base.nvector._N_vector_}).
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

    def toStr(self, prec=3, fmt=Fmt.SQUARE, sep=_COMMASPACE_):  # PYCHOK expected
        '''Return the string representation of this cartesian.

           @kwarg prec: Number of (decimal) digits, unstripped (C{int}).
           @kwarg fmt: Enclosing backets format (C{str}).
           @kwarg sep: Separator to join (C{str}).

           @return: Cartesian represented as "[x, y, z]" (C{str}).
        '''
        return Vector3d.toStr(self, prec=prec, fmt=fmt, sep=sep)

    def toTransform(self, transform, inverse=False, datum=None):
        '''Return a new cartesian by applying a Helmert transform
           to this cartesian.

           @arg transform: Transform to apply (L{Transform}).
           @kwarg inverse: Apply the inverse of the Helmert
                           transform (C{bool}).
           @kwarg datum: Datum for the transformed cartesian (L{Datum}),
                         overriding this cartesian's datum.

           @return: The transformed cartesian (C{Cartesian}).

           @raise Valuerror: If C{B{inverse}=True} and B{C{datum}}
                             is not L{Datums}C{.WGS84}.
        '''
        d = datum or self.datum
        if inverse and d != _WGS84:
            raise _ValueError(inverse=inverse, datum=d,
                              txt=_not_(_WGS84.name))

        xyz = transform.transform(*self.xyz, inverse=inverse)
        return self.classof(xyz, datum=d)

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
