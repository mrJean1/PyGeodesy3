
# -*- coding: utf-8 -*-

u'''Classes L{AuxAngle}, L{AuxDLat}, L{AuxDST} and L{AuxLat} transcoded to Python from I{Karney}'s
C++ class U{AuxAngle<https://GeographicLib.SourceForge.io/C++/doc/classGeographicLib_1_1AuxAngle.html>},
U{DAuxLatitude<https://GeographicLib.SourceForge.io/C++/doc/classGeographicLib_1_1DAuxLatitude.html>},
U{DST<https://GeographicLib.SourceForge.io/C++/doc/classGeographicLib_1_1DST.html>}, repectively
U{AuxLatitude<https://GeographicLib.SourceForge.io/C++/doc/classGeographicLib_1_1AuxLatitude.html>} all
in I{GeographicLib version 2.2+}.

Copyright (C) U{Charles Karney<mailto:Karney@Alum.MIT.edu>} (2022-2023) and licensed under the MIT/X11
License.  For more information, see the U{GeographicLib<https://GeographicLib.SourceForge.io>} documentation.

@note: Class L{AuxDST} requires package U{numpy<https://PyPI.org/project/numpy>} version 1.16 or newer
       to be installed, but only for I{exact} area calculations.

@see: U{Auxiliary latitudes<https:#GeographicLib.SourceForge.io/C++/doc/auxlat.html>} and
      U{On auxiliary latitudes<https:#ArXiv.org/abs/2212.05818>}.
'''

from pygeodesy3.maths.auxilats.auxAngle import AuxAngle, AuxBeta, AuxChi, AuxMu, \
                                               AuxPhi, AuxTheta, AuxXi  # PYCHOK exported
from pygeodesy3.maths.auxilats.auxDLat import AuxDLat  # PYCHOK exported
from pygeodesy3.maths.auxilats.auxDST import AuxDST  # PYCHOK exported
from pygeodesy3.maths.auxilats.auxily import Aux, AuxError  # PYCHOK exported
from pygeodesy3.maths.auxilats.auxLat import AuxLat  # PYCHOK exported
from pygeodesy3.lazily import _ALL_LAZY

__all__ = _ALL_LAZY.maths_auxilats  # no modules: auxAngle, auxDLat, auxDST, auxily, auxLat
__version__ = '23.12.18'

# **) MIT License
#
# Copyright (C) 2023-2024 -- mrJean1 at Gmail -- All Rights Reserved.
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
