
# -*- coding: utf-8 -*-

# The setuptools script to build, test and install a PyGeodesy
# distribution.

# python setup.py sdist --formats=gztar,bztar,zip  # ztar,tar
# python setup.py bdist_wheel --universal  # XXX
# python setup.py test
# python setup.py install

# <https://packaging.Python.org/key_projects/#setuptools>
# <https://packaging.Python.org/distributing>
# <https://docs.Python.org/2/distutils/sourcedist.html>
# <https://docs.Python.org/3.6/distutils/sourcedist.html>
# <https://setuptools.ReadTheDocs.io/en/latest/setuptools.html#developer-s-guide>
# <https://setuptools.ReadTheDocs.io/en/latest/setuptools.html#test-build-package-and-run-a-unittest-suite>

from setuptools import setup

__all__ = ()
__version__ = '24.01.05'


def _c2(*names):
    return ' :: '.join(names)


def _long_description():
    with open('README.rst', 'rb') as f:
        t = f.read()
        if isinstance(t, bytes):
            t = t.decode('utf-8')
        return t


def _version():
    with open('pygeodesy3/__init__.py') as f:
        for t in f.readlines():
            if t.startswith('__version__'):
                v = t.split('=')[-1].strip().strip('\'"')
                return '.'.join(map(str, map(int, v.split('.'))))


_KeyWords = ('AER', 'Albers', 'altitude', 'Andoyer', 'annulus', 'antipode', 'area', 'attitude',
             'Authalic', 'auxiliary', 'azimuth', 'azimuthal', 'azimuth-elevation-range',
             'bearing', 'bank', 'Barsky', 'Barth', 'beta', 'boolean',
             'cached', 'Cagnoli', 'cartesian', 'Cassini', 'Cassini-Soldner', 'chord',
             'circle-intersections', 'circumcenter', 'circumcircle', 'circumradius',
             'clip', 'Cohen', 'Cohen-Sutherland', 'Collins', 'composite',
             'conformal', 'conic', 'constants', 'contact-triangle',
             'Cook', 'Correia', 'cosines-law', 'coverage', 'curvature', 'cylindrical',
             'datum', 'deprecation', 'deficit', 'development', 'discrete', 'distance', 'Douglas',
             'earth', 'east-north-up', 'eccentricity', 'ECEF', 'elevation', 'ellipsoid',
             'ellipsoidal-latitude-beta', 'ellipsoidal-longitude-omega', 'elliptic',
             'ENU', 'EPSG', 'equal-area', 'equidistant', 'equirectangular', 'ETM', 'ETRF',
             'Euclidean', 'even-odd-rule', 'ExactTM', 'excess',
             'Farrell', 'Farrell-Barth', 'flattening', 'Field-Of-View', 'fmath',
             'footprint', 'Forster', 'Forster-Hormann-Popa', 'Forsythe', 'FOV',
             'fractional', 'Frechet', 'Fréchet', 'frustum', 'Fsum',
             'GARS', 'geocentric', 'GeoConvert', 'GeodesicExact', 'geodesy', 'geodetic', 'GeodSolve', 'GeodTest',
             'geographiclib', 'geohash', 'geoid', 'geoidHeight', 'GeoidHeights',
             'georef', 'Girard', 'gnomonic', 'gons', 'grades', 'gradians', 'Greiner', 'Greiner-Hormann',
             'Hartzell', 'Hausdorff', 'Haversine', 'heading', 'height', 'Heron',
             'Hodgman', 'horizon', 'Hormann', 'Hubeny',
             'IDW', 'incenter', 'incirle', 'infix_@_operator', 'inradius', 'intermediate', 'interpolate',
             'intersect', 'intersection', 'intersection3d', 'intersections',
             'Inverse-Distance-Weighting', 'Isometric', 'ITRF',
             'Jacobi', 'Jacobi-Conformal', 'Jarque-Bera', 'Jekel',
             'Karney', 'Krueger', 'Krüger', 'kurtosis',
             'Lambert', 'latitude', 'law-of-cosines', 'least-squares', 'Lesh',
             'L_Huilier', 'LHuilier', 'Liang', 'Liang-Barsky', 'linearize', 'Line-Of-Sight',
             'LocalCartesian', 'local-tangent-plane', 'local-x-y-z', 'longitude', 'LOS', 'loxodrome',
             'lstsq', 'LTP', 'lune', 'LV03', 'LV95',
             'mean', 'memoize', 'memoized', 'Mercator', 'Meeus', 'MGRS',
             'nearest', 'NED', 'normalize', 'Norrdine', 'north-east-down', 'numpy', 'n-vector', 'Nvector',
             'oblate', 'omega', 'orthographic', 'orthometric-height', 'OSGB', 'OSGR', 'overlap',
             'parallel', 'parallel-of-latitude', 'Parametric', 'path-intersection',
             'perimeter', 'Peucker', 'Pierlot', 'pitch', 'plumb', 'Point-Of-View', 'polar', 'Popa', 'POV',
             'precision-cubic-root', 'precision-hypotenuse', 'precision-powers',
             'precision-running-summation', 'precision-square-root', 'precision-summation',
             'prolate', 'Pseudo-Mercator', 'PyGeodesy', 'PyInstaller', 'PyPy',
             'radical', 'radii', 'radius', 'Ramer', 'Ramer-Douglas-Peucker', 'Rectifying',
             'Reduced', 'resect', 'resection', 'Rey-Jer', 'Reumann', 'Reumann-Witkam', 'rhumb', 'RhumbSolve',
             'running-linear-regression', 'running-statistics', 'running-stats', 'running-summation',
             'scipy', 'secant', 'semi-perimeter', 'sexagecimal', 'simplify', 'skewness',
             'Snellius', 'Snellius-Pothenot', 'Snyder', 'Soddy', 'Soddy-circles', 'Soldner',
             'sphere', 'sphere-intersections', 'spherical-deficit', 'spherical-excess', 'spherical-triangle',
             'standard-deviation', 'stereographic', 'Sudano', 'surface-area', 'Sutherland', 'Sutherland-Hodgman',
             'tangent-circles', 'Terrestrial-Reference-Frame', 'Thomas', 'Tienstra',
             'tilt', 'TMcoords', 'TMExact', 'toise', 'transverse', 'TransverseMercatorExact', 'TRF',
             'triangle', 'triangulate', 'triaxial', 'triaxial-ellipsoid',
             'trigonometry', 'trilaterate', 'trilaterate-2d', 'trilaterate-3d',
             'umbilic-point', 'unit', 'unroll', 'UPS', 'UTM', 'UTM/UPS',
             'variance', 'Veness', 'Vermeille', 'viewing-frustum', 'Vincenty', 'Visvalingam',
             'Visvalingam-Whyatt', 'volume', ' volumetric',
             'Web-Mercator', 'Welford', 'WGRS', 'WGS', 'Whyatt', 'Wildberger', 'Witkam', 'winding-number',
             'XYZ', 'yaw', 'You')

setup(name='PyGeodesy3',
      packages=['pygeodesy3', 'pygeodesy3.Base', 'pygeodesy3.deprecated', 'pygeodesy3.distances', 'pygeodesy3.earth',
                              'pygeodesy3.elevations', 'pygeodesy3.ellipsoidal', 'pygeodesy3.geodesic',
                              'pygeodesy3.geodesic.exact', 'pygeodesy3.grids', 'pygeodesy3.maths',
                              'pygeodesy3.maths.auxilats', 'pygeodesy3.miscs', 'pygeodesy3.polygonal',
                              'pygeodesy3.projections', 'pygeodesy3.rhumb', 'pygeodesy3.spherical',],
      description='Pure Python geodesy tools',
      version=_version(),

      author='Jean M. Brouwers',
      author_email='mrJean1@Gmail.com',
      maintainer='Jean M. Brouwers',
      maintainer_email='mrJean1@Gmail.com',

      license='MIT',
      keywords=' '.join(_KeyWords),
      url='https://GitHub.com/mrJean1/PyGeodesy3',

      long_description=_long_description(),

      package_data={'pygeodesy3': ['LICENSE']},

      test_suite='test.TestSuite',

      zip_safe=False,

      # <https://PyPI.org/pypi?%3Aaction=list_classifiers>
      classifiers=[_c2('Development Status', '3 - Alpha'),  # '5 - Production/Stable'
                   _c2('Environment', 'Console'),
                   _c2('Intended Audience', 'Developers'),
                   _c2('License', 'OSI Approved', 'MIT License'),
                   _c2('Operating System', 'OS Independent'),
                   _c2('Programming Language', 'Python'),
                   _c2('Programming Language', 'Python', '3.7'),
                   _c2('Programming Language', 'Python', '3.8'),
                   _c2('Programming Language', 'Python', '3.9'),
                   _c2('Programming Language', 'Python', '3.10'),
                   _c2('Programming Language', 'Python', '3.11'),
                   _c2('Programming Language', 'Python', '3.12'),
                   _c2('Topic', 'Software Development'),
                   _c2('Topic', 'Scientific/Engineering', 'GIS'),
      ],  # PYCHOK indent

#     download_url='https://GitHub.com/mrJean1/PyGeodesy3',
#     entry_points={},
#     include_package_data=False,
#     install_requires=[],
#     namespace_packages=[],
#     py_modules=[],
)  # PYCHOK indent
