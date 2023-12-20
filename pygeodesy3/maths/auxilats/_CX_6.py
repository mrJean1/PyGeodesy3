
# -*- coding: utf-8 -*-

u'''Coeficients for C{_AUXLATITUDE_ORDER} 6 from I{Karney}'s C++ class U{AuxLatitude
<https://GeographicLib.SourceForge.io/C++/doc/classGeographicLib_1_1AuxLatitude.html>}
trancoded to a double, uniquified Python C{dict[auxout][auxin]}.

Copyright (C) Charles Karney (2022-2023) Karney@Alum.MIT.edu> and licensed under the
MIT/X11 License.  For more information, see <https:#GeographicLib.SourceForge.io>.
'''
# make sure int/int division yields float quotient
from __future__ import division as _; del _  # PYCHOK semicolon

from pygeodesy3.constants import _0_0, _0_25, _0_5, _1_0, _N_1_0, _1_5, \
                                 _2_0, _N_2_0, _4_0, _6_0, _8_0, _16_0
from pygeodesy3.maths.auxilats.auxily import Aux, _Ufloats

__all__ = ()
__version__ = '23.12.18'

_f, _u = float, _Ufloats()
_coeffs_6 = _u._Coeffs(6, {  # GEOGRAPHICLIB_AUXLATITUDE_ORDER == 6
    Aux.PHI: {
        # C[phi,phi] skipped
        Aux.BETA: _u(  # C[phi,beta]; even coeffs only
            _0_0, _0_0, _1_0,
            _0_0, _0_0, _0_5,
            _0_0, 1 / _f(3),
            _0_0, _0_25,
            1 / _f(5),
            1 / _f(6),),
        Aux.THETA: _u(  # C[phi,theta]; even coeffs only
            _2_0, _N_2_0, _2_0,
            _6_0, -_4_0, _2_0,
            -_8_0, 8 / _f(3),
            -_16_0, _4_0,
            32 / _f(5),
            32 / _f(3),),
        Aux.MU: _u(  # C[phi,mu]; even coeffs only
            269 / _f(512), -27 / _f(32), _1_5,
            6759 / _f(4096), -55 / _f(32), 21 / _f(16),
            -417 / _f(128), 151 / _f(96),
            -15543 / _f(2560), 1097 / _f(512),
            8011 / _f(2560),
            293393 / _f(61440),),
        Aux.CHI: _u(  # C[phi,chi]
            -2854 / _f(675), 26 / _f(45), 116 / _f(45), _N_2_0, -2 / _f(3), _2_0,
            2323 / _f(945), 2704 / _f(315), -227 / _f(45), -8 / _f(5), 7 / _f(3),
            73814 / _f(2835), -1262 / _f(105), -136 / _f(35), 56 / _f(15),
            -399572 / _f(14175), -332 / _f(35), 4279 / _f(630),
            -144838 / _f(6237), 4174 / _f(315),
            601676 / _f(22275),),
        Aux.XI: _u(  # C[phi,xi]
            28112932 / _f(212837625), 60136 / _f(467775), -2582 / _f(14175),
            -16 / _f(35), 4 / _f(45), 4 / _f(3),
            251310128 / _f(638512875), -21016 / _f(51975), -11966 / _f(14175),
            152 / _f(945), 46 / _f(45),
            -8797648 / _f(10945935), -94388 / _f(66825), 3802 / _f(14175),
            3044 / _f(2835),
            -1472637812 / _f(638512875), 41072 / _f(93555), 6059 / _f(4725),
            455935736 / _f(638512875), 768272 / _f(467775),
            4210684958 / _f(1915538625),)
    },
    Aux.BETA: {
        Aux.PHI: _u(  # C[beta,phi]; even coeffs only
            _0_0, _0_0, _N_1_0,
            _0_0, _0_0, _0_5,
            _0_0, -1 / _f(3),
            _0_0, _0_25,
            -1 / _f(5),
            1 / _f(6),),
        # C[beta,beta] skipped
        Aux.THETA: _u(  # C[beta,theta]; even coeffs only
            _0_0, _0_0, _1_0,
            _0_0, _0_0, _0_5,
            _0_0, 1 / _f(3),
            _0_0, _0_25,
            1 / _f(5),
            1 / _f(6),),
        Aux.MU: _u(  # C[beta,mu]; even coeffs only
            205 / _f(1536), -9 / _f(32), _0_5,
            1335 / _f(4096), -37 / _f(96), 5 / _f(16),
            -75 / _f(128), 29 / _f(96),
            -2391 / _f(2560), 539 / _f(1536),
            3467 / _f(7680),
            38081 / _f(61440),),
        Aux.CHI: _u(  # C[beta,chi]
            -3118 / _f(4725), -1 / _f(3), 38 / _f(45), -1 / _f(3), -2 / _f(3), _1_0,
            -247 / _f(270), 50 / _f(21), -7 / _f(9), -14 / _f(15), 5 / _f(6),
            17564 / _f(2835), -5 / _f(3), -34 / _f(21), 16 / _f(15),
            -49877 / _f(14175), -28 / _f(9), 2069 / _f(1260),
            -28244 / _f(4455), 883 / _f(315),
            797222 / _f(155925),),
        Aux.XI: _u(  # C[beta,xi]
            7947332 / _f(212837625), 11824 / _f(467775), -1082 / _f(14175),
            -46 / _f(315), 4 / _f(45), 1 / _f(3),
            39946703 / _f(638512875), -16672 / _f(155925), -338 / _f(2025),
            68 / _f(945), 17 / _f(90),
            -255454 / _f(1563705), -101069 / _f(467775), 1102 / _f(14175),
            461 / _f(2835),
            -189032762 / _f(638512875), 1786 / _f(18711), 3161 / _f(18900),
            80274086 / _f(638512875), 88868 / _f(467775),
            880980241 / _f(3831077250),)
    },
    Aux.THETA: {
        Aux.PHI: _u(  # C[theta,phi]; even coeffs only
            _N_2_0, _2_0, _N_2_0,
            _6_0, -_4_0, _2_0,
            _8_0, -8 / _f(3),
            -_16_0, _4_0,
            -32 / _f(5),
            32 / _f(3),),
        Aux.BETA: _u(  # C[theta,beta]; even coeffs only
            _0_0, _0_0, _N_1_0,
            _0_0, _0_0, _0_5,
            _0_0, -1 / _f(3),
            _0_0, _0_25,
            -1 / _f(5),
            1 / _f(6),),
        # C[theta,theta] skipped
        Aux.MU: _u(  # C[theta,mu]; even coeffs only
            499 / _f(1536), -23 / _f(32), -1 / _f(2),
            6565 / _f(12288), -5 / _f(96), 5 / _f(16),
            -77 / _f(128), 1 / _f(32),
            -4037 / _f(7680), 283 / _f(1536),
            1301 / _f(7680),
            17089 / _f(61440),),
        Aux.CHI: _u(  # C[theta,chi]
            -3658 / _f(4725), 2 / _f(9), 4 / _f(9), -2 / _f(3), -2 / _f(3), _0_0,
            61 / _f(135), 68 / _f(45), -23 / _f(45), -4 / _f(15), 1 / _f(3),
            9446 / _f(2835), -46 / _f(35), -24 / _f(35), 2 / _f(5),
            -34712 / _f(14175), -80 / _f(63), 83 / _f(126),
            -2362 / _f(891), 52 / _f(45),
            335882 / _f(155925),),
        Aux.XI: _u(  # C[theta,xi]
            216932 / _f(2627625), 109042 / _f(467775), -2102 / _f(14175),
            -158 / _f(315), 4 / _f(45), -2 / _f(3),
            117952358 / _f(638512875), -7256 / _f(155925), 934 / _f(14175),
            -16 / _f(945), 16 / _f(45),
            -7391576 / _f(54729675), -25286 / _f(66825), 922 / _f(14175),
            -232 / _f(2835),
            -67048172 / _f(638512875), 268 / _f(18711), 719 / _f(4725),
            46774256 / _f(638512875), 14354 / _f(467775),
            253129538 / _f(1915538625),)
    },
    Aux.MU: {
        Aux.PHI: _u(  # C[mu,phi]; even coeffs only
            -3 / _f(32), 9 / _f(16), -3 / _f(2),
            135 / _f(2048), -15 / _f(32), 15 / _f(16),
            105 / _f(256), -35 / _f(48),
            -189 / _f(512), 315 / _f(512),
            -693 / _f(1280),
            1001 / _f(2048),),
        Aux.BETA: _u(  # C[mu,beta]; even coeffs only
            -1 / _f(32), 3 / _f(16), -1 / _f(2),
            -9 / _f(2048), 1 / _f(32), -1 / _f(16),
            3 / _f(256), -1 / _f(48),
            3 / _f(512), -5 / _f(512),
            -7 / _f(1280),
            -7 / _f(2048),),
        Aux.THETA: _u(  # C[mu,theta]; even coeffs only
            -15 / _f(32), 13 / _f(16), _0_5,
            -1673 / _f(2048), 33 / _f(32), -1 / _f(16),
            349 / _f(256), -5 / _f(16),
            963 / _f(512), -261 / _f(512),
            -921 / _f(1280),
            -6037 / _f(6144),),
        # C[mu,mu] skipped
        Aux.CHI: _u(  # C[mu,chi]
            7891 / _f(37800), -127 / _f(288), 41 / _f(180), 5 / _f(16), -2 / _f(3),
            _0_5,
            -1983433 / _f(1935360), 281 / _f(630), 557 / _f(1440), -3 / _f(5),
            13 / _f(48),
            167603 / _f(181440), 15061 / _f(26880), -103 / _f(140), 61 / _f(240),
            6601661 / _f(7257600), -179 / _f(168), 49561 / _f(161280),
            -3418889 / _f(1995840), 34729 / _f(80640),
            212378941 / _f(319334400),),
        Aux.XI: _u(  # C[mu,xi]
            12674323 / _f(851350500), -384229 / _f(14968800), -1609 / _f(28350),
            121 / _f(1680), 4 / _f(45), -1 / _f(6),
            -31621753811 / _f(1307674368000), -431 / _f(17325),
            16463 / _f(453600), 26 / _f(945), -29 / _f(720),
            -32844781 / _f(1751349600), 3746047 / _f(119750400), 449 / _f(28350),
            -1003 / _f(45360),
            10650637121 / _f(326918592000), 629 / _f(53460),
            -40457 / _f(2419200),
            205072597 / _f(20432412000), -1800439 / _f(119750400),
            -59109051671 / _f(3923023104000),)
    },
    Aux.CHI: {
        Aux.PHI: _u(  # C[chi,phi]
            4642 / _f(4725), 32 / _f(45), -82 / _f(45), 4 / _f(3), 2 / _f(3), _N_2_0,
            -1522 / _f(945), 904 / _f(315), -13 / _f(9), -16 / _f(15), 5 / _f(3),
            -12686 / _f(2835), 8 / _f(5), 34 / _f(21), -26 / _f(15),
            -24832 / _f(14175), -12 / _f(5), 1237 / _f(630),
            109598 / _f(31185), -734 / _f(315),
            444337 / _f(155925),),
        Aux.BETA: _u(  # C[chi,beta]
            -998 / _f(4725), 2 / _f(5), -16 / _f(45), _0_0, 2 / _f(3), _N_1_0,
            -2 / _f(27), -22 / _f(105), 19 / _f(45), -2 / _f(5), 1 / _f(6),
            116 / _f(567), -22 / _f(105), 16 / _f(105), -1 / _f(15),
            2123 / _f(14175), -8 / _f(105), 17 / _f(1260),
            128 / _f(4455), -1 / _f(105),
            149 / _f(311850),),
        Aux.THETA: _u(  # C[chi,theta]
            1042 / _f(4725), -14 / _f(45), -2 / _f(9), 2 / _f(3), 2 / _f(3), _0_0,
            -712 / _f(945), -4 / _f(45), 43 / _f(45), 4 / _f(15), -1 / _f(3),
            274 / _f(2835), 124 / _f(105), 2 / _f(105), -2 / _f(5),
            21068 / _f(14175), -16 / _f(105), -55 / _f(126),
            -9202 / _f(31185), -22 / _f(45),
            -90263 / _f(155925),),
        Aux.MU: _u(  # C[chi,mu]
            -96199 / _f(604800), 81 / _f(512), 1 / _f(360), -37 / _f(96), 2 / _f(3),
            -1 / _f(2),
            1118711 / _f(3870720), -46 / _f(105), 437 / _f(1440), -1 / _f(15),
            -1 / _f(48),
            -5569 / _f(90720), 209 / _f(4480), 37 / _f(840), -17 / _f(480),
            830251 / _f(7257600), 11 / _f(504), -4397 / _f(161280),
            108847 / _f(3991680), -4583 / _f(161280),
            -20648693 / _f(638668800),),
        # C[chi,chi] skipped
        Aux.XI: _u(  # C[chi,xi]
            -55271278 / _f(212837625), 27128 / _f(93555), -2312 / _f(14175),
            -88 / _f(315), 34 / _f(45), -2 / _f(3),
            106691108 / _f(638512875), -65864 / _f(155925), 6079 / _f(14175),
            -184 / _f(945), 1 / _f(45),
            5921152 / _f(54729675), -14246 / _f(467775), 772 / _f(14175),
            -106 / _f(2835),
            75594328 / _f(638512875), -5312 / _f(467775), -167 / _f(9450),
            2837636 / _f(638512875), -248 / _f(13365),
            -34761247 / _f(1915538625),)
    },
    Aux.XI: {
        Aux.PHI: _u(  # C[xi,phi]
            -44732 / _f(2837835), 20824 / _f(467775), 538 / _f(4725), 88 / _f(315),
            -4 / _f(45), -4 / _f(3),
            -12467764 / _f(212837625), -37192 / _f(467775), -2482 / _f(14175),
            8 / _f(105), 34 / _f(45),
            100320856 / _f(1915538625), 54968 / _f(467775), -898 / _f(14175),
            -1532 / _f(2835),
            -5884124 / _f(70945875), 24496 / _f(467775), 6007 / _f(14175),
            -839792 / _f(19348875), -23356 / _f(66825),
            570284222 / _f(1915538625),),
        Aux.BETA: _u(  # C[xi,beta]
            -70496 / _f(8513505), 2476 / _f(467775), 34 / _f(675), 32 / _f(315),
            -4 / _f(45), -1 / _f(3),
            53836 / _f(212837625), 3992 / _f(467775), 74 / _f(2025), -4 / _f(315),
            -7 / _f(90),
            -661844 / _f(1915538625), 7052 / _f(467775), 2 / _f(14175),
            -83 / _f(2835),
            1425778 / _f(212837625), 934 / _f(467775), -797 / _f(56700),
            390088 / _f(212837625), -3673 / _f(467775),
            -18623681 / _f(3831077250),),
        Aux.THETA: _u(  # C[xi,theta]
            -4286228 / _f(42567525), -193082 / _f(467775), 778 / _f(4725),
            62 / _f(105), -4 / _f(45), 2 / _f(3),
            -61623938 / _f(70945875), 92696 / _f(467775), 12338 / _f(14175),
            -32 / _f(315), 4 / _f(45),
            427003576 / _f(1915538625), 612536 / _f(467775), -1618 / _f(14175),
            -524 / _f(2835),
            427770788 / _f(212837625), -8324 / _f(66825), -5933 / _f(14175),
            -9153184 / _f(70945875), -320044 / _f(467775),
            -1978771378 / _f(1915538625),),
        Aux.MU: _u(  # C[xi,mu]
            -9292991 / _f(302702400), 7764059 / _f(239500800), 1297 / _f(18900),
            -817 / _f(10080), -4 / _f(45), 1 / _f(6),
            36019108271 / _f(871782912000), 35474 / _f(467775),
            -29609 / _f(453600), -2 / _f(35), 49 / _f(720),
            3026004511 / _f(30648618000), -4306823 / _f(59875200),
            -2917 / _f(56700), 4463 / _f(90720),
            -368661577 / _f(4036032000), -102293 / _f(1871100),
            331799 / _f(7257600),
            -875457073 / _f(13621608000), 11744233 / _f(239500800),
            453002260127 / _f(7846046208000),),
        Aux.CHI: _u(  # C[xi,chi]
            2706758 / _f(42567525), -55222 / _f(93555), 2458 / _f(4725),
            46 / _f(315), -34 / _f(45), 2 / _f(3),
            -340492279 / _f(212837625), 516944 / _f(467775), 3413 / _f(14175),
            -256 / _f(315), 19 / _f(45),
            4430783356 / _f(1915538625), 206834 / _f(467775), -15958 / _f(14175),
            248 / _f(567),
            62016436 / _f(70945875), -832976 / _f(467775), 16049 / _f(28350),
            -651151712 / _f(212837625), 15602 / _f(18711),
            2561772812 / _f(1915538625),)  # PYCHOK exported
        # C[xi,xi] skipped
    }
})
# _ptrs_6 = (0,   0,  12,  24,  36,  57,  78,  90,  90, 102, 114, 135,
#          156, 168, 180, 180, 192, 213, 234, 246, 258, 270, 270, 291,
#          312, 333, 354, 375, 396, 396, 417, 438, 459, 480, 501, 522,
#          522)  # PYCHOK exported
del _f, _u

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