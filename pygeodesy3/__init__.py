
# -*- coding: utf-8 -*-

u'''A pure Python implementation of geodesy tools for various ellipsoidal and spherical earth
models using precision trigonometric, vector-based, exact, elliptic, iterative and approximate
methods for geodetic (lat-/longitude), geocentric (U{ECEF<https://WikiPedia.org/wiki/ECEF>}
cartesian) and certain U{triaxial ellipsoidal<https://GeographicLib.SourceForge.io/1.44/triaxial.html>}
coordinates and supported I{only on Python 3.7 and newer}.

Transcoded from U{JavaScript originals<https://GitHub.com/ChrisVeness/geodesy>} by I{Chris Veness
(C) 2005-2022} and from several U{C++ classes<https://GeographicLib.SourceForge.io/C++/doc/annotated.html>}
by I{Charles F. F. Karney (C) 2008-2023} and published under the same U{MIT License
<https://OpenSource.org/licenses/MIT>}**.

There are four modules for ellipsoidal earth models, C{ellipsoidal.exact}, C{.karney}, C{.vincenty}
and C{.nvector} and two for spherical ones, C{spherical.trigonometry} and C{.nvector}.  Each module
provides a geodetic B{C{LatLon}} and a geocentric B{C{Cartesian}} class with methods and functions
to compute distance, surface area, perimeter, initial and final bearing, intermediate and nearest
points, circle intersections and secants, path intersections, U{3-point resections
<https://WikiPedia.org/wiki/Position_resection_and_intersection>}, rhumb and rhumb lines, trilateration
(by intersection, by overlap and in 3d), conversions and unrolling, among other things.  For more
information and further details see the U{documentation<https://mrJean1.GitHub.io/PyGeodesy3>}, the
descriptions of U{Latitude/Longitude<https://www.Movable-Type.co.UK/scripts/latlong.html>},
U{Vincenty<https://www.Movable-Type.co.UK/scripts/latlong-vincenty.html>} and
U{Vector-based<https://www.Movable-Type.co.UK/scripts/latlong-vectors.html>} geodesy,
the original U{JavaScript source<https://GitHub.com/ChrisVeness/geodesy>} or
U{docs<https://www.Movable-Type.co.UK/scripts/geodesy/docs>} and I{Karney}'s Python
U{geographiclib<https://PyPI.org/project/geographiclib>} and U{C++ GeographicLib
<https://GeographicLib.SourceForge.io/C++/doc/index.html>}.

Also included are modules for conversions to and from U{Cassini-Soldner
<https://GeographicLib.SourceForge.io/C++/doc/classGeographicLib_1_1CassiniSoldner.html>},
U{ECEF<https://WikiPedia.org/wiki/ECEF>} (Earth-Centered, Earth-Fixed cartesian), U{UTM
<https://www.Movable-Type.co.UK/scripts/latlong-utm-mgrs.html>} (Universal Transverse Mercator
and U{Exact<https://GeographicLib.SourceForge.io/C++/doc/classGeographicLib_1_1TransverseMercatorExact.html>}),
U{UPS<https://WikiPedia.org/wiki/Universal_polar_stereographic_coordinate_system>} (Universal Polar
Stereographic) and U{Web Mercator<https://WikiPedia.org/wiki/Web_Mercator>} (Pseudo-Mercator) coordinates,
U{MGRS<https://GeographicLib.SourceForge.io/C++/doc/classGeographicLib_1_1MGRS.html>} (Military Grid Reference
System, UTM I{and} UPS) and U{OSGR<https://www.Movable-Type.co.UK/scripts/latlong-os-gridref.html>} (British
Ordinance Survery Grid Reference) grid references, U{TRF<http://ITRF.ENSG.IGN.Fr>} (Terrestrial Reference
Frames) and modules to encode and decode U{EPSG<https://EPSG.org>}, U{Geohashes
<https://www.Movable-Type.co.UK/scripts/geohash.html>}, U{Georefs (WGRS)
<https://WikiPedia.org/wiki/World_Geographic_Reference_System>} and U{Garefs (GARS)
<https://WikiPedia.org/wiki/Global_Area_Reference_System>}.

Other modules provide U{Albers equal-area<https://GeographicLib.SourceForge.io/
html/classGeographicLib_1_1AlbersEqualArea.html>} projections, U{equidistant
<https://GeographicLib.SourceForge.io/C++/doc/classGeographicLib_1_1AzimuthalEquidistant.html>}
and other I{azimuthal} projections, Lambert I{conformal conic} projections and
positions, functions to clip paths or polygons of C{LatLon} points using the
U{Cohen-Sutherland<https://WikiPedia.org/wiki/Cohen-Sutherland_algorithm>},
U{Forster-Hormann-Popa<https://www.ScienceDirect.com/science/article/pii/S259014861930007X>},
U{Greiner-Hormann<http://www.inf.USI.CH/hormann/papers/Greiner.1998.ECO.pdf>},
U{Liang-Barsky<https://www.CS.Helsinki.FI/group/goa/viewing/leikkaus/intro.html>} and
U{Sutherland-Hodgman<https://WikiPedia.org/wiki/Sutherland-Hodgman_algorithm>} methods,
functions to U{simplify<https://Bost.Ocks.org/mike/simplify>} or linearize a path of C{LatLon}
points (or a U{NumPy array<https://docs.SciPy.org/doc/numpy/reference/generated/numpy.array.html>}),
including implementations of the U{Ramer-Douglas-Peucker<https://WikiPedia.org/wiki/
Ramer-Douglas-Peucker_algorithm>}, the U{Visvalingam-Whyatt<https://hydra.Hull.ac.UK/
resources/hull:8338>} and the U{Reumann-Witkam<https://psimpl.SourceForge.net/reumann-witkam.html>}
algorithms and modified versions of the former.  Other classes provide I{boolean} operations between
(composite) polygons or U{interpolate <https://docs.SciPy.org/doc/scipy/reference/interpolate.html>}
the L{height<pygeodesy3.elevations.heights>} of C{LatLon} points and L{Geoid<pygeodesy3.elevations.geoids>}
models, compute various U{Fréchet<https://WikiPedia.org/wiki/Frechet_distance>} and U{Hausdorff
<https://WikiPedia.org/wiki/Hausdorff_distance>} distances.

Installation
============

To install PyGeodesy3, type C{python3 -m pip install PyGeodesy3} or C{python3 -m easy_install
PyGeodesy3} in a terminal or command window.

If the wheel C{PyGeodesy3-yy.m.d-py3-none-any.whl} is missing in U{PyPI Download files<https://
PyPI.org/project/PyGeodesy3/#files>}, download the file from U{GitHub/dist<https://GitHub.com/mrJean1/
PyGeodesy3/tree/master/dist>}.  Install that with C{python3 -m pip install <path-to-downloaded-wheel>}
and verify with C{python3 -m pygeodesy3}.

Alternatively, download C{PyGeodesy3-yy.m.d.zip} from U{PyPI<https://PyPI.org/project/PyGeodesy3>}
or U{GitHub<https://GitHub.com/mrJean1/PyGeodesy3>}, C{unzip} the downloaded file, C{cd} to
directory C{Pygeodesy-yy.m.d} and type C{python3 setup.py install}.

To run all PyGeodesy3 tests, type C{python3 test/run.py} or type C{python3 test/unitTestSuite.py}
before or after installation.

Dependencies
============

Installation of I{Karney}'s Python package U{geographiclib<https://PyPI.org/project/geographiclib>}
is optional, but required to use modules L{ellipsoidal.karney} and L{css}, L{azimuthal} classes
L{EquidistantKarney} and L{GnomonicKarney} and the L{HeightIDWkarney} interpolator.

Both U{numpy<https://PyPI.org/project/numpy>} and U{scipy<https://PyPI.org/project/scipy>} must be
installed for most L{Geoid...<pygeodesy3.elevations.geoids>} and L{Height...<pygeodesy3.elevations.heights>}
interpolators, except L{GeoidKarney} and the L{HeightIDW...<pygeodesy3.elevations.heights>} ones.

Functions and C{LatLon} methods L{circin6}, L{circum3}, L{circum4_}, L{soddy4}, L{trilaterate3d2} and
C{trilaterate5} and modules L{maths.auxilats} and L{rhumb.aux_} require U{numpy<https://PyPI.org/project/numpy>}.

Modules L{ellipsoidal.solve} and L{geodesic.solve} and L{projections.azimuthal} classes L{EquidistantGeodSolve}
and L{GnomonicGeodSolve} depend on I{Karney}'s C++ utility U{GeodSolve
<https://GeographicLib.SourceForge.io/C++/doc/GeodSolve.1.html>} to be executable and set with
env variable C{PYGEODESY3_GEODSOLVE} or with property L{Ellipsoid.geodsolve}.

To compare C{MGRS} results from modules L{grids.mgrs} and C{test.testMgrs} with I{Karney}'s C++ utility
U{GeoConvert<https://GeographicLib.SourceForge.io/C++/doc/GeoConvert.1.html>}, the latter must be
executable and set with env variable C{PYGEODESY3_GEOCONVERT}.

Module L{rhumb.solve} needs I{Karney}'s C++ utility U{RhumbSolve
<https://GeographicLib.SourceForge.io/C++/doc/RhumbSolve.1.html>} to be executable and set with env
variable C{PYGEODESY3_RHUMBSOLVE} or with property L{Ellipsoid.rhumbsolve}.

Documentation
=============

In addition to the C{pygeodesy3} package, the U{PyGeodesy3<https://PyPI.org/project/PyGeodesy3>}
U{distribution files<https://GitHub.com/mrJean1/PyGeodesy3/tree/master/dist>} contain the tests,
the test results (on macOS only) and the complete U{documentation<https://mrJean1.GitHub.io/PyGeodesy3>}
(generated by U{Epydoc<https://PyPI.org/project/epydoc>} using command line:
C{epydoc --html --no-private --no-source --name=PyGeodesy3 --url=... -v pygeodesy3}).

Tests
=====

The tests ran with Python 3.12 (with U{geographiclib<https://PyPI.org/project/geographiclib>} 2.0,
Python 3.11.5 (with U{geographiclib<https://PyPI.org/project/geographiclib>} 2.0, U{numpy
<https://PyPI.org/project/numpy>} 1.24.2 and U{scipy<https://PyPI.org/project/scipy>} 1.10.1), Python
3.10.8 (with U{geographiclib <https://PyPI.org/project/geographiclib>} 2.0, U{numpy
<https://PyPI.org/project/numpy>} 1.23.3, U{scipy<https://PyPI.org/project/scipy>} 1.9.1, U{GeoConvert
<https://GeographicLib.SourceForge.io/html/utilities.html>} 2.2, U{GeodSolve
<https://GeographicLib.SourceForge.io/html/utilities.html>} 2.2 and U{RhumbSolve
<https://GeographicLib.SourceForge.io/html/utilities.html>} 2.2) and Python 3.9.6, all on macOS
14.1.2 Sonoma, Apple M1 Silicon (C{arm64}), I{natively} and in 64-bit only.

All tests ran with and without C{lazy import} for Python 3 and with command line option C{-W default} and
env variable C{PYGEODESY3_WARNINGS=on} for all Python versions.  The results of those tests are included in
the distribution files.

Test coverage has been measured with U{coverage<https://PyPI.org/project/coverage>} 7.2.2.  The complete
coverage report in HTML and a PDF summary are included in the distribution files.

The tests also ran with Python 3.11.5 (and U{geographiclib<https://PyPI.org/project/geographiclib>} 2.0) on
U{Debian 11<https://Cirrus-CI.com/github/mrJean1/PyGeodesy3/master>} in 64-bit only and with Python 3.11.5
and 3.10.10 (all with U{geographiclib<https://PyPI.org/project/geographiclib>} 1.52) on U{Windows 10
<https://CI.AppVeyor.com/project/mrJean1/pygeodesy3>} in 64- and/or 32-bit.

Notes
=====

For a summary of all I{Karney}-based functionality in C{pygeodesy3}, see module U{karney
<https://mrJean1.GitHub.io/PyGeodesy3/docs/pygeodesy3.Base.karney-module.html>}.

Env variables
=============

The following environment variables are observed by C{PyGeodesy3}:

 - C{PYGEODESY3_EXCEPTION_CHAINING} - see module L{miscs.errors}.
 - C{PYGEODESY3_FMT_FORM} - see module L{miscs.dms}.
 - C{PYGEODESY3_FSUM_PARTIALS} - see module L{maths.fsums} and class L{maths.fsums.Fsum}.
 - C{PYGEODESY3_FSUM_RESIDUAL} - see module L{maths.fsums} and class L{maths.fsums.Fsum}.
 - C{PYGEODESY3_GEOCONVERT} - see module L{grids.mgrs}.
 - C{PYGEODESY3_GEODSOLVE} - see module L{geodesic.solve}.
 - C{PYGEODESY3_LAZY_IMPORT} - see module L{lazily} and variable L{lazily.isLazy}.
 - C{PYGEODESY3_NOTIMPLEMENTED} - __special__ methods return C{NotImplemented} if set to "std".
 - C{PYGEODESY3_RHUMBSOLVE} - see module L{rhumb.solve}.
 - C{PYGEODESY3_UPS_POLES} - see modules L{projections.ups} and L{grids.mgrs}.

and these to control standard or I{named} C{repr}esentations:

 - C{PYGEODESY3_BEARING_STD_REPR} - see method L{miscs.units.Bearing}C{.__repr__}.
 - C{PYGEODESY3_BOOL_STD_REPR} - see method L{miscs.units.Bool}C{.__repr__}.
 - C{PYGEODESY3_DEGREES_STD_REPR} - see method L{miscs.units.Degrees}C{.__repr__}.
 - C{PYGEODESY3_FLOAT_STD_REPR} - see method L{miscs.units.Float}C{.__repr__}.
 - C{PYGEODESY3_INT_STD_REPR} - see method L{miscs.units.Int}C{.__repr__}.
 - C{PYGEODESY3_METER_STD_REPR} - see method L{miscs.units.Meter}C{.__repr__}.
 - C{PYGEODESY3_RADIANS_STD_REPR} - see method L{miscs.units.Radians}C{.__repr__}.
 - C{PYGEODESY3_STR_STD_REPR} - see method L{miscs.units.Str}C{.__repr__}.

plus during development:

 - C{PYGEODESY3_ALL_BACKWARD} - import all modules for backward compatibility.
 - C{PYGEODESY3_FOR_DOCS} - for extended documentation by C{epydoc}.
 - C{PYGEODESY3_GEOGRAPHICLIB} - see module L{Base.karney}.
 - C{PYGEODESY3_WARNINGS} - see module L{miscs.props} and function L{DeprecationWarnings}.
 - C{PYGEODESY3_XPACKAGES} - see module L{basics}.
 - C{PYTHONDEVMODE} - see modules L{miscs.errors} and L{miscs.props}.

and:

 - C{PYGEODESY3_INIT__ALL__} - Set env variable C{PYGEODESY3_INIT__ALL__=__all__} to import
   all packages, modules, classes, functions and variables and set variable C{pygeodesy3.__all__}.

License
=======

**) U{Copyright (C) 2016-2024 -- mrJean1 at Gmail -- All Rights Reserved.
<https://OpenSource.org/licenses/MIT>}

C{Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:}

C{The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.}

C{THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.}

@newfield example: Example, Examples

@var EPS:    System's M{epsilon} ≈ 2.22044604925e-16 (C{float}).
@var EPS0:   M{EPS**2}    ≈ 4.9e-32 for near-zero comparison
@var EPS02:  M{EPS**4}    ≈ 2.4e-63 for near-zero squared comparison
@var EPS1:   M{1 - EPS}   ≈ 0.9999999999999998 (C{float}).
@var EPS2:   M{EPS * 2}   ≈ 4.440892098501e-16 (C{float}).
@var EPS_2:  M{EPS / 2}   ≈ 1.110223024625e-16 (C{float}).
@var EPS4:   M{EPS * 4}   ≈ 8.881784197001e-16 (C{float}).

@var F_D:   Format degrees as unsigned "deg°" with symbol, plus compass point suffix C{N, S, E} or C{W} (C{str}).
@var F_DM:  Format degrees as unsigned "deg°min′" with symbols, plus suffix (C{str}).
@var F_DMS: Format degrees as unsigned "deg°min′sec″" with symbols, plus suffix (C{str}).
@var F_DEG: Format degrees as unsigned "[D]DD" I{without} symbol, plus suffix (C{str}).
@var F_MIN: Format degrees as unsigned "[D]DDMM" I{without} symbols, plus suffix (C{str}).
@var F_SEC: Format degrees as unsigned "[D]DDMMSS" I{without} symbols, plus suffix (C{str}).
@var F_D60: Format degrees as unsigned "[D]DD.MMSS" C{sexagecimal} I{without} symbols, plus suffix (C{str}).
@var F__E:  Format degrees as unsigned "%E" I{without} symbols, plus suffix (C{str}).
@var F__F:  Format degrees as unsigned "%F" I{without} symbols, plus suffix (C{str}).
@var F__G:  Format degrees as unsigned "%G" I{without} symbols, plus suffix (C{str}).
@var F_RAD: Convert degrees to radians and format as unsigned "RR" with symbol, plus suffix (C{str}).

@var F_D_:   Format degrees as signed "-/deg°" with symbol, I{without} suffix (C{str}).
@var F_DM_:  Format degrees as signed "-/deg°min′" with symbols, I{without} suffix (C{str}).
@var F_DMS_: Format degrees as signed "-/deg°min′sec″" with symbols, I{without} suffix (C{str}).
@var F_DEG_: Format degrees as signed "-/[D]DD" I{without} symbol, I{without} suffix (C{str}).
@var F_MIN_: Format degrees as signed "-/[D]DDMM" I{without} symbols, I{without} suffix (C{str}).
@var F_SEC_: Format degrees as signed "-/[D]DDMMSS" I{without} symbols, I{without} suffix (C{str}).
@var F_D60_: Format degrees as signed "-/[D]DD.MMSS" C{sexagecimal} I{without} symbols, I{without} suffix (C{str}).
@var F__E_:  Format degrees as signed "-/%E" I{without} symbols, I{without} suffix (C{str}).
@var F__F_:  Format degrees as signed "-/%F" I{without} symbols, I{without} suffix (C{str}).
@var F__G_:  Format degrees as signed "-/%G" I{without} symbols, I{without} suffix (C{str}).
@var F_RAD_: Convert degrees to radians and format as signed "-/RR" I{without} symbol, I{without} suffix (C{str}).

@var F_D__:   Format degrees as signed "-/+deg°" with symbol, I{without} suffix (C{str}).
@var F_DM__:  Format degrees as signed "-/+deg°min′" with symbols, I{without} suffix (C{str}).
@var F_DMS__: Format degrees as signed "-/+deg°min′sec″" with symbols, I{without} suffix (C{str}).
@var F_DEG__: Format degrees as signed "-/+[D]DD" I{without} symbol, I{without} suffix (C{str}).
@var F_MIN__: Format degrees as signed "-/+[D]DDMM" I{without} symbols, without suffix (C{str}).
@var F_SEC__: Format degrees as signed "-/+[D]DDMMSS" I{without} symbols, I{without} suffix (C{str}).
@var F_D60__: Format degrees as signed "-/+[D]DD.MMSS" C{sexagecimal} I{without} symbols, I{without} suffix (C{str}).
@var F__E__:  Format degrees as signed "-/+%E" I{without} symbols, I{without} suffix (C{str}).
@var F__F__:  Format degrees as signed "-/+%F" I{without} symbols, I{without} suffix (C{str}).
@var F__G__:  Format degrees as signed "-/+%G" I{without} symbols, I{without} suffix (C{str}).
@var F_RAD__: Convert degrees to radians and format as signed "-/+RR" I{without} symbol, I{without} suffix (C{str}).

@var DIG:      System's M{float decimal digits} = 15 (C{int}).
@var INF:      Infinity (C{float}), see functions L{pygeodesy3.isinf} and L{pygeodesy3.isfinite} and C{NINF}.
@var INT0:     C{int(0)}, missing Z-components, C{if B{z}=B{INT0}}, see functions L{pygeodesy3.isint0}, L{pygeodesy3.meeus2}
@var MANT_DIG: System's M{float mantissa bits} = 53 (C{int}).
@var MAX:      System's M{float max} ≈ 1.798e+308 (C{float}).
@var MIN:      System's M{float min} ≈ 2.225e-308 (C{float}).
@var NAN:      Not-A-Number (C{float}), see function L{pygeodesy3.isnan}.
@var NEG0:     Negative 0.0 (C{float}), see function L{pygeodesy3.isneg0}.
@var NINF:     Negative infinity (C{float}), see function L{pygeodesy3.isninf} and C{INF}.
@var NN:       Empty (C{str}), U{I{Nomen Nescio}<https://Wiktionary.org/wiki/N.N.>}.

@var PI:    Constant M{math.pi} (C{float}).
@var PI2:   Two PI, M{PI * 2}, aka I{Tau} (C{float}).
@var PI_2:  Half PI, M{PI / 2} (C{float}).
@var PI3:   Three PI, M{PI * 3} (C{float}).
@var PI3_2: One and a half PI, M{PI * 3 / 2} (C{float}).
@var PI_3:  One third PI, M{PI / 3} (C{float}).
@var PI4:   Four PI, M{PI * 4} (C{float}).
@var PI_4:  Quarter PI, M{PI / 4} (C{float}).

@var R_MA: Equatorial earth radius (C{meter}), WGS84, EPSG:3785.
@var R_MB: Polar earth radius (C{meter}), WGS84, EPSG:3785.
@var R_M:  Mean (spherical) earth radius (C{meter}).
@var R_KM: Mean (spherical) earth radius (C{Km}, kilometer).
@var R_NM: Mean (spherical) earth radius (C{NM}, nautical miles).
@var R_SM: Mean (spherical) earth radius (C{SM}, statute miles).
@var R_FM: Former FAI-Sphere earth radius (C{meter}).
@var R_GM: Average earth radius, distance to geoid surface (C{meter})
@var R_QM: Earth' (triaxial) quadratic mean radius (C{meter})
@var R_VM: Aviation/Navigation earth radius (C{meter}).

@var S_DEG: Degrees symbol, default C{"°"}
@var S_MIN: Minutes symbol, default C{"′"} aka I{PRIME}
@var S_SEC: Seconds symbol, default C{"″"} aka I{DOUBLE_PRIME}
@var S_RAD: Radians symbol, default C{""} aka L{pygeodesy3.NN}
@var S_DMS: If C{True} include, otherwise cancel all DMS symbols, default C{True}.
@var S_SEP: Separator between C{deg°|min′|sec″|suffix}, default C{""} aka L{pygeodesy3.NN}

@var Conics:     Registered, predefined conics (C{enum-like}).
@var Datums:     Registered, predefined datums (C{enum-like}).
@var Ellipsoids: Registered, predefined ellipsoids (C{enum-like}).
@var RefFrames:  Registered, predefined reference frames (C{enum-like}).
@var Transforms: Registered, predefined transforms (C{enum-like}).

@var isLazy: Lazy import setting (C{int} 1, 2 or 3+) from C{env} variable C{PYGEODESY3_LAZY_IMPORT}, or C{False} if initializing C{lazy import} failed.

@var pygeodesy3_abspath: Fully qualified C{pygeodesy3} directory name (C{str}).

@var version: Normalized C{PyGeodesy3} version (C{str}).
'''

import os.path as _pth
import sys as _sys

__all__            = ()
# <https://PyInstaller.ReadTheDocs.io/en/stable/runtime-information.html>
_isfrozen          = _init__all__ = getattr(_sys, 'frozen', False)  # in .lazily
pygeodesy3_abspath = _pth.dirname(_pth.abspath(__file__))  # _sys._MEIPASS + '/pygeodesy3'
_pygeodesy3_       = __package__ or _pth.basename(pygeodesy3_abspath)

if _isfrozen:  # avoid lazy import and import *
    _lazy_import2 = None
else:
    # setting __path__ should ...
    __path__ = [pygeodesy3_abspath]
    try:  # ... make this import work, ...
        from pygeodesy3 import lazily as _
    except (AttributeError, ImportError):  # ... if it doesn't,
        # extend _sys.path to include this very directory such
        # that all public and private sub-modules can be
        # imported (and checked by PyChecker, etc.)
        _sys.path.insert(0, pygeodesy3_abspath)  # XXX __path__[0]

    try:  # lazily requires Python 3.7+, see lazily.__doc__
        from pygeodesy3.lazily import _init__all__, _lazy_import2  # PYCHOK expected
        _, __getattr__ = _lazy_import2(_pygeodesy3_)  # PYCHOK expected

    except (ImportError, NotImplementedError):  # LazyImportError
        from pygeodesy3.lazily import isLazy
        if isLazy is False:  # not enabled
            raise
        _lazy_import2 = None

if _init__all__ and not _lazy_import2:  # PYCHOK no cover
    import pygeodesy3.lazily as lazily  # PYCHOK exported
    __all__ = lazily._import_all()

    import pygeodesy3.Base        as Base         # PYCHOK INTERNAL
    import pygeodesy3.basics      as basics       # PYCHOK exported
    import pygeodesy3.constants   as constants    # PYCHOK exported
    import pygeodesy3.deprecated  as deprecated   # PYCHOK exported
    import pygeodesy3.distances   as distances    # PYCHOK exported
    import pygeodesy3.earth       as earth        # PYCHOK exported
    import pygeodesy3.elevations  as elevations   # PYCHOK exported
    import pygeodesy3.ellipsoidal as ellipsoidal  # PYCHOK exported
    import pygeodesy3.geodesic    as geodesic     # PYCHOK exported
    import pygeodesy3.grids       as grids        # PYCHOK exported
    import pygeodesy3.interns     as interns      # PYCHOK exported
    import pygeodesy3.maths       as maths        # PYCHOK exported
    import pygeodesy3.miscs       as miscs        # PYCHOK exported
    import pygeodesy3.polygonal   as polygonal    # PYCHOK exported
    import pygeodesy3.projections as projections  # PYCHOK exported
    import pygeodesy3.rhumb       as rhumb        # PYCHOK exported
    import pygeodesy3.spherical   as spherical    # PYCHOK exported

#   import pygeodesy3.geodesic.exact as ... for make dist
#   import pygeodesy3.maths.auxilats as ... for make dist

# from pygeodesy3.interns import _DOT_  # from .lazily
from pygeodesy3.lazily import _DOT_, _import_all_backward, isLazy  # PYCHOK import

__all__    += _import_all_backward()
__version__ = '24.01.10'
# see setup.py for similar logic
version     = _DOT_(*map(int, __version__.split(_DOT_)))

del _DOT_, _import_all_backward, _lazy_import2, _pth, _sys

# **) MIT License
#
# Copyright (C) 2024-2024 -- mrJean1 at Gmail -- All Rights Reserved.
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
