
# -*- coding: utf-8 -*-

u'''Ellipsoidal, C{N-vector}-based geodesy.

Ellipsoidal classes geodetic L{LatLon}, geocentric (ECEF) L{Cartesian}
and C{Nvector} and functions L{meanOf}, L{sumOf} and DEPRECATED L{toNed}.

Pure Python implementation of n-vector-based geodetic (lat-/longitude)
methods by I{(C) Chris Veness 2011-2016} published under the same MIT
Licence**, see U{Vector-based geodesy
<https://www.Movable-Type.co.UK/scripts/latlong-vectors.html>}.

These classes and functions work with: (a) geodetic lat-/longitude points on
the earth's surface and (b) 3-D vectors used as n-vectors representing points
on the earth's surface or vectors normal to the plane of a great circle.

See also I{Kenneth Gade} U{'A Non-singular Horizontal Position Representation'
<https://www.NavLab.net/Publications/A_Nonsingular_Horizontal_Position_Representation.pdf>},
The Journal of Navigation (2010), vol 63, nr 3, pp 395-417.
'''
# make sure int/int division yields float quotient, see .basics
from __future__ import division as _; del _  # PYCHOK semicolon

from pygeodesy3.base.nvector import fabs, fdot, NorthPole, LatLonNvectorBase, \
                                    NvectorBase, sumOf as _sumOf
# from pygeodesy3.distances.formy import _isequalTo  # _MODS
from pygeodesy3.earth.datums import _earth_ellipsoid, _ellipsoidal_datum, _WGS84
from pygeodesy3.ellipsoidal.base import CartesianEllipsoidalBase, _nearestOn, \
                                        LatLonEllipsoidalBase, _TOL_M,  _Wrap
from pygeodesy3.interns import NN, _Nv00_
from pygeodesy3.interns import _down_, _east_, _north_, _pole_  # PYCHOK used!
from pygeodesy3.lazily import _ALL_LAZY, _ALL_MODS as _MODS, _ALL_OTHER
# from pygeodesy3.maths.fmath import fdot  # from .base.nvector
# from pygeodesy3.maths.umath import _Wrap  # from .base.ellipsoidal
from pygeodesy3.miscs.basics import issubclassof, map2, _xinstanceof
# from pygeodesy3.miscs.dms import toDMS  # _MODS
from pygeodesy3.miscs.errors import _IsnotError, _xkwds, _xkwds_pop
from pygeodesy3.miscs.props import deprecated_function, Property_RO, property_RO
from pygeodesy3.miscs.streprs import Fmt  # XXX fstr, _xzipairs
from pygeodesy3.miscs.units import Scalar  # XXX Bearing, Distance, Height, Scalar
# from pygeodesy3.projections.ltp import Ltp  # _MODS
from pygeodesy3.projections.ltpTuples import Aer, Ned, Ned4Tuple  # XXX sincos2d_

# from math import fabs  # from .base.nvector

__all__ = _ALL_LAZY.ellipsoidal_nvector
__version__ = '23.12.24'


class Cartesian(CartesianEllipsoidalBase):
    '''Extended to convert geocentric, L{Cartesian} points to
       C{Nvector} and n-vector-based, geodetic L{LatLon}.
    '''
    @property_RO
    def Ecef(self):
        '''Get the ECEF I{class} (L{EcefVeness}), I{once}.
        '''
        return _Ecef()

    def toLatLon(self, **LatLon_and_kwds):  # PYCHOK LatLon=LatLon, datum=None
        '''Convert this cartesian to an C{Nvector}-based geodetic point.

           @kwarg LatLon_and_kwds: Optional L{LatLon}, B{C{datum}} and other
                                   keyword arguments.  Use C{B{LatLon}=...} to
                                   override this L{LatLon} class or specify
                                   C{B{LatLon} is None}.

           @return: The geodetic point (L{LatLon}) or if B{C{LatLon}} is set
                    to C{None}, an L{Ecef9Tuple}C{(x, y, z, lat, lon, height,
                    C, M, datum)} with C{C} and C{M} if available.

           @raise TypeError: Invalid B{C{LatLon_and_kwds}}.
        '''
        kwds = _xkwds(LatLon_and_kwds, LatLon=LatLon, datum=self.datum)
        return CartesianEllipsoidalBase.toLatLon(self, **kwds)

    def toNvector(self, **Nvector_and_kwds):  # PYCHOK Datums.WGS84
        '''Convert this cartesian to C{Nvector} components, I{including height}.

           @kwarg Nvector_and_kwds: Optional C{Nvector}, B{C{datum}} and other
                                    keyword arguments.  Use C{B{Nvector}=...} to
                                    override this C{Nvector} class or specify
                                    C{B{Nvector} is None}.

           @return: The C{n-vector} components (C{Nvector}) or if B{C{Nvector}}
                    is set to C{None}, a L{Vector4Tuple}C{(x, y, z, h)}

           @raise TypeError: Invalid B{C{Nvector_and_kwds}}.
        '''
        kwds = _xkwds(Nvector_and_kwds, Nvector=Nvector, datum=self.datum)
        return CartesianEllipsoidalBase.toNvector(self, **kwds)


class LatLon(LatLonNvectorBase, LatLonEllipsoidalBase):
    '''An n-vector-based, ellipsoidal L{LatLon} point.
    '''
    _Nv = None  # cached toNvector (C{Nvector})

    def _update(self, updated, *attrs, **setters):  # PYCHOK args
        '''(INTERNAL) Zap cached attributes if updated.
        '''
        if updated:
            LatLonNvectorBase._update(self, updated, _Nv=self._Nv)  # special case
            LatLonEllipsoidalBase._update(self, updated, *attrs, **setters)

#     def crossTrackDistanceTo(self, start, end, radius=R_M):
#         '''Return the (signed) distance from this point to the great
#            circle defined by a start point and an end point or bearing.
#
#            @arg start: Start point of great circle line (L{LatLon}).
#            @arg end: End point of great circle line (L{LatLon}) or
#                      initial bearing (compass C{degrees360}) at the
#                      start point.
#            @kwarg radius: Mean earth radius (C{meter}).
#
#            @return: Distance to great circle, negative if to left or
#                     positive if to right of line (C{meter}, same units
#                     as B{C{radius}}).
#
#            @raise TypeError: If B{C{start}} or B{C{end}} point is not L{LatLon}.
#         '''
#         self.others(start=start)
#
#         if _isDegrees(end):  # gc from point and bearing
#             gc = start.greatCircle(end)
#         else:  # gc by two points
#             gc = start.toNvector().cross(end.toNvector())
#
#         # (signed) angle between point and gc normal vector
#         v =  self.toNvector()
#         a =  gc.angleTo(v, vSign=v.cross(gc))
#         a = _copysign(PI_2, a) - a
#         return a * float(radius)

    def deltaTo(self, other, wrap=False, **Ned_and_kwds):
        '''Calculate the local delta from this to an other point.

           @note: This is a linear delta, I{unrelated} to a geodesic on the
                  ellipsoid.

           @arg other: The other point (L{LatLon}).
           @kwarg wrap: If C{True}, wrap or I{normalize} the B{C{other}}
                        point (C{bool}).
           @kwarg Ned_and_kwds: Optional keyword arguments C{B{Ned}=L{Ned},
                          B{name}=NN} with the class to return delta, name
                          and and possibly other B{C{Ned}} keyword arguments.

           @return: Delta from this to the other point (B{C{Ned}}).

           @raise TypeError: The B{C{other}} point is not L{LatLon} or
                             B{C{Ned}} is invalid.

           @raise ValueError: If ellipsoids are incompatible.
        '''
        self.ellipsoids(other)  # throws TypeError and ValueError

        p = self.others(other)
        if wrap:
            p = _Wrap.point(p)
        # get delta in cartesian frame
        dc = p.toCartesian().minus(self.toCartesian())
        # rotate dc to get delta in n-vector reference
        # frame using the rotation matrix row vectors
        ned_ = map2(dc.dot, self._rotation3)

        C = _xkwds_pop(Ned_and_kwds, Ned=Ned)
        if issubclassof(C, Ned4Tuple):
            ltp = _MODS.projections.ltp
            ned_ += (ltp.Ltp(self, ecef=self.Ecef(self.datum)),)
        elif not issubclassof(C, Ned):
            raise _IsnotError(Fmt.sub_class(Ned, Ned4Tuple), Ned=C)
        return C(*ned_, **_xkwds(Ned_and_kwds, name=NN))

#     def destination(self, distance, bearing, radius=R_M, height=None):
#         '''Return the destination point after traveling from this
#            point the given distance on the given initial bearing.
#
#            @arg distance: Distance traveled (C{meter}, same units as
#                           given earth B{C{radius}}).
#            @arg bearing: Initial bearing (compass C{degrees360}).
#            @kwarg radius: Mean earth radius (C{meter}).
#            @kwarg height: Optional height at destination point,
#                           overriding default (C{meter}, same units
#                           as B{C{radius}}).
#
#            @return: Destination point (L{LatLon}).
#         '''
#         r = _m2radians(distance, radius)  # angular distance in radians
#         # great circle by starting from this point on given bearing
#         gc = self.greatCircle(bearing)
#
#         v1 = self.toNvector()
#         x = v1.times(cos(r))  # component of v2 parallel to v1
#         y = gc.cross(v1).times(sin(r))  # component of v2 perpendicular to v1
#
#         v2 = x.plus(y).unit()
#         return v2.toLatLon(height=self.height if height is C{None} else height)

    def destinationNed(self, delta):
        '''Calculate the destination point using the supplied NED delta
           from this point.

           @arg delta: Delta from this to the other point in the local
                       tangent plane (LTP) of this point (L{Ned}).

           @return: Destination point (L{LatLon}).

           @raise TypeError: If B{C{delta}} is not L{pygeodesy3.Ned}.
        '''
        _xinstanceof(Ned, delta=delta)

        nv, ev, dv = self._rotation3
        # convert NED delta to standard coordinate frame of n-vector
        dn = delta.ned4[:3]  # XXX Ned4Tuple.to3Tuple
        # rotate dn to get delta in cartesian (ECEF) coordinate
        # reference frame using the rotation matrix column vectors
        dc = Cartesian(fdot(dn, nv.x, ev.x, dv.x),
                       fdot(dn, nv.y, ev.y, dv.y),
                       fdot(dn, nv.z, ev.z, dv.z))

        # apply (cartesian) delta to this Cartesian to obtain destination as cartesian
        v = self.toCartesian().plus(dc)
        return v.toLatLon(datum=self.datum, LatLon=self.classof)  # Cartesian(v.x, v.y, v.z).toLatLon(...)

    def distanceTo(self, other, radius=None, wrap=False):
        '''I{Approximate} the distance from this to an other point.

           @arg other: The other point (L{LatLon}).
           @kwarg radius: Mean earth radius, ellipsoid or datum (C{meter},
                          L{Ellipsoid}, L{Ellipsoid2}, L{Datum} or
                          L{a_f2Tuple}), overriding the mean radius C{R1}
                          of this point's datum..
           @kwarg wrap: If C{True}, wrap or I{normalize} and unroll the
                        B{C{other}} and angular distance (C{bool}).

           @return: Distance (C{meter}, same units as B{C{radius}}).

           @raise TypeError: The B{C{other}} point is not L{LatLon}.

           @raise ValueError: Invalid B{C{radius}}.
        '''
        p = self.others(other)
        if wrap:
            p = _Wrap.point(p)
        a = self._N_vector.angleTo(p._N_vector, wrap=wrap)
        E = self.datum.ellipsoid if radius is None else _earth_ellipsoid(radius)
        return fabs(a) * E.R1  # see .maths.umath.radians2m

    @property_RO
    def Ecef(self):
        '''Get the ECEF I{class} (L{EcefVeness}), I{once}.
        '''
        return _Ecef()

    def isequalTo(self, other, eps=None):
        '''Compare this point with an other point.

           @arg other: The other point (L{LatLon}).
           @kwarg eps: Optional margin (C{float}).

           @return: C{True} if points are identical, including
                    datum, I{ignoring height}, C{False} otherwise.

           @raise TypeError: The B{C{other}} point is not L{LatLon}.

           @raise ValueError: Invalid B{C{eps}}.

           @see: Method C{isequalTo3} to include I{height}.
        '''
        return self.datum == self.others(other).datum and \
              _MODS.distances.formy._isequalTo(self, other, eps=eps)

#     def greatCircle(self, bearing):
#         '''Return the great circle heading on the given bearing
#            from this point.
#
#            Direction of vector is such that initial bearing vector
#            b = c × p, where p is representing this point.
#
#            @arg bearing: Bearing from this point (compass C{degrees360}).
#
#            @return: N-vector representing great circle (C{Nvector}).
#         '''
#         a, b, _ = self.philamheight
#         t = radians(bearing)
#
#         sa, ca, sb, cb, st, ct = sincos2_(a, b, t)
#         return self._xnamed(Nvector(sb * ct - sa * cb * st,
#                                    -cb * ct - sa * sb * st,
#                                     ca * st)

#     def initialBearingTo(self, other, wrap=False):
#         '''Return the initial bearing (forward azimuth) from
#            this to an other point.
#
#            @arg other: The other point (L{LatLon}).
#            @kwarg wrap: If C{True}, wrap or I{normalize}
#                         and unroll the B{C{other}} (C{bool}).
#
#            @return: Initial bearing (compass C{degrees360}).
#
#            @raise TypeError: The B{C{other}} point is not L{LatLon}.
#         '''
#         p = self.others(other)
#         if wrap:
#             p = _Wrap.point(p)
#         v1 = self.toNvector()
#
#         gc1 = v1.cross(p.toNvector())  # gc through v1 & v2
#         gc2 = v1.cross(_NP3)  # gc through v1 & North pole
#
#         # bearing is (signed) angle between gc1 & gc2
#         return degrees360(gc1.angleTo(gc2, vSign=v1))

    def intermediateTo(self, other, fraction, height=None, wrap=False):
        '''Return the point at given fraction between this and
           an other point.

           @arg other: The other point (L{LatLon}).
           @arg fraction: Fraction between both points (C{scalar},
                          0.0 at this to 1.0 at the other point.
           @kwarg height: Optional height, overriding the fractional
                          height (C{meter}).
           @kwarg wrap: If C{True}, wrap or I{normalize} the
                        B{C{other}} point (C{bool}).

           @return: Intermediate point (L{LatLon}).

           @raise TypeError: The B{C{other}} point is not L{LatLon}.
        '''
        p = self.others(other)
        if wrap:
            p = _Wrap.point(p)
        f = Scalar(fraction=fraction)
        h = self._havg(other, f=f, h=height)
        i = self.toNvector().intermediateTo(p.toNvector(), f)
        return i.toLatLon(height=h, LatLon=self.classof)  # Nvector(i.x, i.y, i.z).toLatLon(...)

    @Property_RO
    def _rotation3(self):
        '''(INTERNAL) Get the rotation matrix from n-vector coordinate frame axes.
        '''
        nv = self.toNvector()  # local (n-vector) coordinate frame

        dv = nv.negate()  # down, opposite to n-vector
        ev = NorthPole.cross(nv, raiser=_pole_).unit()  # east, pointing perpendicular to the plane
        nv = ev.cross(dv)  # north, by right hand rule
        return nv, ev, dv  # matrix rows

    def toCartesian(self, **Cartesian_and_kwds):  # PYCHOK Cartesian=Cartesian, datum=None
        '''Convert this point to an C{Nvector}-based geodetic point.

           @kwarg Cartesian_and_kwds: Optional L{Cartesian}, B{C{datum}} and other
                                      keyword arguments.  Use C{B{Cartesian}=...}
                                      to override this L{Cartesian} class or specify
                                      C{B{Cartesian}=None}.

           @return: The geodetic point (L{Cartesian}) or if B{C{Cartesian}} is set
                    to C{None}, an L{Ecef9Tuple}C{(x, y, z, lat, lon, height, C, M,
                    datum)} with C{C} and C{M} if available.

           @raise TypeError: Invalid B{C{Cartesian}} or other B{C{Cartesian_and_kwds}}.
        '''
        kwds = _xkwds(Cartesian_and_kwds, Cartesian=Cartesian, datum=self.datum)
        return LatLonEllipsoidalBase.toCartesian(self, **kwds)

    def toNvector(self, **Nvector_and_kwds):  # PYCHOK signature
        '''Convert this point to C{Nvector} components, I{including height}.

           @kwarg Nvector_and_kwds: Optional C{Nvector}, B{C{datum}} and other
                                    keyword arguments.  Use C{B{Nvector}=...}
                                    to override this C{Nvector} class or specify
                                    C{B{Nvector}=None}.

           @return: The C{n-vector} components (C{Nvector}) or if B{C{Nvector}}
                    is set to C{None}, a L{Vector4Tuple}C{(x, y, z, h)}.

           @raise TypeError: Invalid B{C{Nvector}} or other B{C{Nvector_and_kwds}}.
        '''
        kwds = _xkwds(Nvector_and_kwds, Nvector=Nvector, datum=self.datum)
        return LatLonNvectorBase.toNvector(self, **kwds)


_Nvll = LatLon(0, 0, name=_Nv00_)  # reference instance (L{LatLon})


class Nvector(NvectorBase):
    '''An n-vector is a position representation using a (unit) vector
       normal to the earth ellipsoid.  Unlike lat-/longitude points,
       n-vectors have no singularities or discontinuities.

       For many applications, n-vectors are more convenient to work
       with than other position representations like lat-/longitude,
       earth-centred earth-fixed (ECEF) vectors, UTM coordinates, etc.

       Note commonality with spherical L{Nvector<spherical.nvector.Nvector>}.
    '''
    _datum = _WGS84  # default datum (L{Datum})

    def __init__(self, x_xyz, y=None, z=None, h=0, datum=None, ll=None, name=NN):
        '''New n-vector normal to the earth's surface.

           @arg x_xyz: X component of vector (C{scalar}) or (3-D) vector
                       (C{Nvector}, L{Vector3d}, L{Vector3Tuple} or
                       L{Vector4Tuple}).
           @kwarg y: Y component of vector (C{scalar}), ignored if B{C{x_xyz}}
                     is not C{scalar}, otherwise same units as B{C{x_xyz}}.
           @kwarg z: Z component of vector (C{scalar}), ignored if B{C{x_xyz}}
                     is not C{scalar}, otherwise same units as B{C{x_xyz}}.
           @kwarg h: Optional height above model surface (C{meter}).
           @kwarg datum: Optional datum this n-vector is defined in
                         (L{Datum}, L{Ellipsoid}, L{Ellipsoid2} or
                         L{a_f2Tuple}).
           @kwarg ll: Optional, original latlon (C{LatLon}).
           @kwarg name: Optional name (C{str}).

           @raise TypeError: If B{C{datum}} is not a L{Datum}.
        '''
        NvectorBase.__init__(self, x_xyz, y=y, z=z, h=h, ll=ll, name=name)
        if datum not in (None, self._datum):
            self._datum = _ellipsoidal_datum(datum, name=name)

    @Property_RO
    def datum(self):
        '''Get this n-vector's datum (L{Datum}).
        '''
        return self._datum

    @property_RO
    def ellipsoidalNvector(self):
        '''Get this C{Nvector}'s ellipsoidal class.
        '''
        return type(self)

    def toCartesian(self, **Cartesian_and_kwds):  # PYCHOK Cartesian=Cartesian
        '''Convert this n-vector to C{Nvector}-based cartesian (ECEF) coordinates.

           @kwarg Cartesian_and_kwds: Optional L{Cartesian}, B{C{h}}, B{C{datum}} and
                                      other keyword arguments.  Use C{B{Cartesian}=...}
                                      to override this L{Cartesian} class or specify
                                      C{B{Cartesian} is None}.

           @return: The cartesian point (L{Cartesian}) or if B{C{Cartesian}} is set
                    to C{None}, an L{Ecef9Tuple}C{(x, y, z, lat, lon, height, C, M,
                    datum)} with C{C} and C{M} if available.

           @raise TypeError: Invalid B{C{Cartesian_and_kwds}}.
        '''
        kwds = _xkwds(Cartesian_and_kwds, h=self.h, Cartesian=Cartesian,
                                                        datum=self.datum)
        return NvectorBase.toCartesian(self, **kwds)  # class or .classof

    def toLatLon(self, **LatLon_and_kwds):  # PYCHOK height=None, LatLon=LatLon
        '''Convert this n-vector to an C{Nvector}-based geodetic point.

           @kwarg LatLon_and_kwds: Optional L{LatLon}, B{C{height}}, B{C{datum}}
                                   and other keyword arguments.  Use C{B{LatLon}=...}
                                   to override this L{LatLon} class or specify
                                   C{B{LatLon} is None}.

           @return: The geodetic point (L{LatLon}) or if B{C{LatLon}} is set
                    to C{None}, an L{Ecef9Tuple}C{(x, y, z, lat, lon, height,
                    C, M, datum)} with C{C} and C{M} if available.

           @raise TypeError: Invalid B{C{LatLon_and_kwds}}.
        '''
        kwds = _xkwds(LatLon_and_kwds, height=self.h, datum=self.datum, LatLon=LatLon)
        return NvectorBase.toLatLon(self, **kwds)  # class or .classof

    def unit(self, ll=None):
        '''Normalize this vector to unit length.

           @kwarg ll: Optional, original latlon (C{LatLon}).

           @return: Normalised vector (C{Nvector}).
        '''
        u = NvectorBase.unit(self, ll=ll)
        if u.datum != self.datum:
            u._update(False, datum=self.datum)
        return u


def _Ecef():
    # return the Ecef class and overwrite property_RO
    Cartesian.Ecef = LatLon.Ecef = E = _MODS.earth.ecef.EcefVeness
    return E


def meanOf(points, datum=_WGS84, height=None, wrap=False,
                                            **LatLon_and_kwds):
    '''Compute the geographic mean of several points.

       @arg points: Points to be averaged (L{LatLon}[]).
       @kwarg datum: Optional datum to use (L{Datum}).
       @kwarg height: Optional height at mean point, overriding
                      the mean height (C{meter}).
       @kwarg wrap: If C{True}, wrap or I{normalize} B{C{points}}
                    (C{bool}).
       @kwarg LatLon_and_kwds: Optional B{C{LatLon}} class to return
                     the mean points and overriding this L{LatLon}
                     (or C{None}) and additional B{C{LatLon}}
                     keyword arguments, ignored if C{B{LatLon}
                     is None}.

       @return: Geographic mean point and mean height (B{C{LatLon}})
                or if B{C{LatLon}} is C{None}, an L{Ecef9Tuple}C{(x,
                y, z, lat, lon, height, C, M, datum)} with C{C} and
                C{M} if available.

       @raise ValueError: Insufficient number of B{C{points}}.
    '''
    Ps = _Nvll.PointsIter(points, wrap=wrap)
    # geographic mean
    m = sumOf(p._N_vector for p in Ps.iterate(closed=False))
    kwds = _xkwds(LatLon_and_kwds, height=height, datum=datum,
                                   LatLon=LatLon, name=meanOf.__name__)
    return m.toLatLon(**kwds)


def nearestOn(point, point1, point2, within=True, height=None, wrap=False,
              equidistant=None, tol=_TOL_M, LatLon=LatLon, **LatLon_kwds):
    '''I{Iteratively} locate the closest point on the geodesic between
       two other (ellipsoidal) points.

       @arg point: Reference point (C{LatLon}).
       @arg point1: Start point of the geodesic (C{LatLon}).
       @arg point2: End point of the geodesic (C{LatLon}).
       @kwarg within: If C{True} return the closest point I{between}
                      B{C{point1}} and B{C{point2}}, otherwise the
                      closest point elsewhere on the geodesic (C{bool}).
       @kwarg height: Optional height for the closest point (C{meter},
                      conventionally) or C{None} or C{False} for the
                      interpolated height.  If C{False}, the closest
                      takes the heights of the points into account.
       @kwarg wrap: If C{True}, wrap or I{normalize} and unroll I{only}
                    B{C{point1}} and B{C{point2}} (C{bool}).
       @kwarg equidistant: An azimuthal equidistant projection (I{class}
                           or function L{pygeodesy3.equidistant}) or C{None}
                           for the preferred C{B{point}.Equidistant}.
       @kwarg tol: Convergence tolerance (C{meter}).
       @kwarg LatLon: Optional class to return the closest point
                      (L{LatLon}) or C{None}.
       @kwarg LatLon_kwds: Optional, additional B{C{LatLon}} keyword
                           arguments, ignored if C{B{LatLon} is None}.

       @return: Closest point, a B{C{LatLon}} instance or if C{B{LatLon}
                is None}, a L{LatLon4Tuple}C{(lat, lon, height, datum)}.

       @raise ImportError: Package U{geographiclib
                           <https://PyPI.org/project/geographiclib>}
                           not installed or not found.

       @raise TypeError: Invalid or non-ellipsoidal B{C{point}}, B{C{point1}}
                         or B{C{point2}} or invalid B{C{equidistant}}.

       @raise ValueError: No convergence for the B{C{tol}}.

       @see: U{The B{ellipsoidal} case<https://GIS.StackExchange.com/questions/48937/
             calculating-intersection-of-two-circles>} and U{Karney's paper
             <https://ArXiv.org/pdf/1102.1215.pdf>}, pp 20-21, section B{14. MARITIME
             BOUNDARIES} for more details about the iteration algorithm.
    '''
    return _nearestOn(point, point1, point2, within=within, height=height, wrap=wrap,
                      equidistant=equidistant, tol=tol, LatLon=LatLon, **LatLon_kwds)


def sumOf(nvectors, Vector=Nvector, h=None, **Vector_kwds):
    '''Return the vectorial sum of two or more n-vectors.

       @arg nvectors: Vectors to be added (C{Nvector}[]).
       @kwarg Vector: Optional class for the vectorial sum (C{Nvector}).
       @kwarg h: Optional height, overriding the mean height (C{meter}).
       @kwarg Vector_kwds: Optional, additional B{C{Vector}} keyword
                           arguments, ignored if C{B{Vector} is None}.

       @return: Vectorial sum (B{C{Vector}}).

       @raise VectorError: No B{C{nvectors}}.
    '''
    return _sumOf(nvectors, Vector=Vector, h=h, **Vector_kwds)


@deprecated_function
def toNed(distance, bearing, elevation, **Ned_and_kwds):  # BACKWARD
    '''DEPRECATED on 23.12.06, Create an NED vector from distance,
       bearing and elevation (in local coordinate system).

       @arg distance: NED vector length (C{meter}).
       @arg bearing: NED vector bearing (compass C{degrees360}).
       @arg elevation: NED vector elevation from local coordinate
                       frame horizontal (C{degrees}).
       @kwarg Ned_name: Optional keyword arguments C{B{Ned}=L{Ned},
                        B{name}=NN} with the class to return the
                        NED, name and and possibly other B{C{Ned}}
                        keyword arguments.

       @return: An B{C{Ned}} vector equivalent to this B{C{distance}},
                B{C{bearing}} and B{C{elevation}}.

       @raise ValueError: Invalid B{C{distance}}, B{C{bearing}}
                          or B{C{elevation}}.
    '''
    n, e, d, _ = Aer(bearing, elevation, distance).xyz4

    C = _xkwds_pop(Ned_and_kwds, Ned=Ned)
    return C(n, e, -d, **_xkwds(Ned_and_kwds, name=NN))  # XXX neg(d)


__all__ += _ALL_OTHER(Cartesian, LatLon, Nvector,  # classes
                      meanOf, sumOf, toNed)

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
