# -*- coding: utf-8 -*-

from tests import GeneratorTestCase
from generator import InclusionType


class Mesh3DTests(GeneratorTestCase):
    def test_square_mesh_3d(self):
        map_simple = [[1, 1],
                      [1, 2]]
        holes = InclusionType(type = 'hole',
                              shape = 'ellipse',
                              dim_x = 150,
                              dim_y = 100,
                              dim_z = 300,
                              el_size = 30,
                              color = 'lightgrey')
        type1 = InclusionType(type = 'plot',
                              shape = 'rectangle',
                              tag = 'mat2',
                              dim_x = 150,
                              dim_y = 100,
                              dim_z = 150,
                              el_size = 25,
                              color = 'grey')
        physical_point_map = \
            [('PointReceiver', [(0, 0, 0), (150, 0, 0)]),
             ('PointSource', [(0, 0, 150)])]
        simple_3d = \
            {'name': 'Mesh3D',
             'dim_x': 500,
             'dim_y': 500,
             'dim_z': 300,
             'periodicity': (False, False, False),
             'nb_x': 2,
             'nb_y': 2,
             'space_x': 250,
             'space_y': 250,
             'pos_x': -125,
             'pos_y': -125,
             'crystal_shape': 'square',
             'el_size_bulk': 25,
             'bulk_tag': 'mat1',
             'inclusion_map': map_simple,
             'inclusion_types': [None, type1, holes],
             'physical_point_map': physical_point_map}
        expected = """//Mesh3D, created with crystalpy
size_bulk = 25;
size_1 = 25;
size_2 = 30;

Point(1) = {0, 0, 0, 25};
Point(2) = {150, 0, 0, 25};
Point(3) = {0, 0, 150, 25};
Point(4) = {-200.0, -75.0, 0, size_1};
Point(5) = {-200.0, -175.0, 0, size_1};
Point(6) = {-50.0, -75.0, 0, size_1};
Point(7) = {-50.0, -175.0, 0, size_1};
Point(8) = {-200.0, -75.0, -150, size_1};
Point(9) = {-200.0, -175.0, -150, size_1};
Point(10) = {-50.0, -75.0, -150, size_1};
Point(11) = {-50.0, -175.0, -150, size_1};
Point(12) = {-200.0, 175.0, 0, size_1};
Point(13) = {-200.0, 75.0, 0, size_1};
Point(14) = {-50.0, 175.0, 0, size_1};
Point(15) = {-50.0, 75.0, 0, size_1};
Point(16) = {-200.0, 175.0, -150, size_1};
Point(17) = {-200.0, 75.0, -150, size_1};
Point(18) = {-50.0, 175.0, -150, size_1};
Point(19) = {-50.0, 75.0, -150, size_1};
Point(20) = {50.0, -75.0, 0, size_1};
Point(21) = {50.0, -175.0, 0, size_1};
Point(22) = {200.0, -75.0, 0, size_1};
Point(23) = {200.0, -175.0, 0, size_1};
Point(24) = {50.0, -75.0, -150, size_1};
Point(25) = {50.0, -175.0, -150, size_1};
Point(26) = {200.0, -75.0, -150, size_1};
Point(27) = {200.0, -175.0, -150, size_1};
Point(28) = {125, 125, 0, size_2};
Point(29) = {50.0, 125, 0, size_2};
Point(30) = {200.0, 125, 0, size_2};
Point(31) = {125, 175.0, 0, size_2};
Point(32) = {125, 75.0, 0, size_2};
Point(33) = {125, 125, 300, size_2};
Point(34) = {50.0, 125, 300, size_2};
Point(35) = {200.0, 125, 300, size_2};
Point(36) = {125, 175.0, 300, size_2};
Point(37) = {125, 75.0, 300, size_2};
Point(38) = {-250.0, 250.0, 0, size_bulk};
Point(39) = {-250.0, -250.0, 0, size_bulk};
Point(40) = {250.0, 250.0, 0, size_bulk};
Point(41) = {250.0, -250.0, 0, size_bulk};
Point(42) = {-250.0, 250.0, 300, size_bulk};
Point(43) = {-250.0, -250.0, 300, size_bulk};
Point(44) = {250.0, 250.0, 300, size_bulk};
Point(45) = {250.0, -250.0, 300, size_bulk};

Line(1) = {5, 4};
Line(2) = {4, 6};
Line(3) = {6, 7};
Line(4) = {7, 5};
Line(5) = {9, 8};
Line(6) = {8, 10};
Line(7) = {10, 11};
Line(8) = {11, 9};
Line(9) = {5, 9};
Line(10) = {4, 8};
Line(11) = {6, 10};
Line(12) = {7, 11};
Line Loop(13) = {9, 5, -10, -1};
Line Loop(14) = {12, 8, -9, -4};
Line Loop(15) = {11, 7, -12, -3};
Line Loop(16) = {2, 11, -6, -10};
Plane Surface(17) = {13};
Plane Surface(18) = {14};
Plane Surface(19) = {15};
Plane Surface(20) = {16};
Line(21) = {13, 12};
Line(22) = {12, 14};
Line(23) = {14, 15};
Line(24) = {15, 13};
Line(25) = {17, 16};
Line(26) = {16, 18};
Line(27) = {18, 19};
Line(28) = {19, 17};
Line(29) = {13, 17};
Line(30) = {12, 16};
Line(31) = {14, 18};
Line(32) = {15, 19};
Line Loop(33) = {29, 25, -30, -21};
Line Loop(34) = {32, 28, -29, -24};
Line Loop(35) = {31, 27, -32, -23};
Line Loop(36) = {22, 31, -26, -30};
Plane Surface(37) = {33};
Plane Surface(38) = {34};
Plane Surface(39) = {35};
Plane Surface(40) = {36};
Line(41) = {21, 20};
Line(42) = {20, 22};
Line(43) = {22, 23};
Line(44) = {23, 21};
Line(45) = {25, 24};
Line(46) = {24, 26};
Line(47) = {26, 27};
Line(48) = {27, 25};
Line(49) = {21, 25};
Line(50) = {20, 24};
Line(51) = {22, 26};
Line(52) = {23, 27};
Line Loop(53) = {49, 45, -50, -41};
Line Loop(54) = {52, 48, -49, -44};
Line Loop(55) = {51, 47, -52, -43};
Line Loop(56) = {42, 51, -46, -50};
Plane Surface(57) = {53};
Plane Surface(58) = {54};
Plane Surface(59) = {55};
Plane Surface(60) = {56};
Ellipse(61) = {34, 33, 35, 36};
Ellipse(62) = {29, 28, 30, 31};
Ellipse(63) = {36, 33, 37, 35};
Ellipse(64) = {31, 28, 32, 30};
Ellipse(65) = {35, 33, 34, 37};
Ellipse(66) = {30, 28, 29, 32};
Ellipse(67) = {37, 33, 36, 34};
Ellipse(68) = {32, 28, 31, 29};
Line(69) = {29, 34};
Line(70) = {31, 36};
Line(71) = {30, 35};
Line(72) = {32, 37};
Line Loop(73) = {62, 70, -61, -69};
Line Loop(74) = {64, 71, -63, -70};
Line Loop(75) = {66, 72, -65, -71};
Line Loop(76) = {68, 69, -67, -72};
Ruled Surface(77) = {73};
Ruled Surface(78) = {74};
Ruled Surface(79) = {75};
Ruled Surface(80) = {76};
Line Loop(81) = {5, 6, 7, 8};
Line Loop(82) = {1, 2, 3, 4};
Plane Surface(83) = {81};
Plane Surface(84) = {82};
Surface Loop(85) = {17, 18, 19, 20, 83, 84};
Volume(86) = {85};
Line Loop(87) = {25, 26, 27, 28};
Line Loop(88) = {21, 22, 23, 24};
Plane Surface(89) = {87};
Plane Surface(90) = {88};
Surface Loop(91) = {37, 38, 39, 40, 89, 90};
Volume(92) = {91};
Line Loop(93) = {45, 46, 47, 48};
Line Loop(94) = {41, 42, 43, 44};
Plane Surface(95) = {93};
Plane Surface(96) = {94};
Surface Loop(97) = {57, 58, 59, 60, 95, 96};
Volume(98) = {97};
Line(99) = {39, 38};
Line(100) = {38, 40};
Line(101) = {40, 41};
Line(102) = {41, 39};
Line(103) = {43, 42};
Line(104) = {42, 44};
Line(105) = {44, 45};
Line(106) = {45, 43};
Line(107) = {39, 43};
Line(108) = {38, 42};
Line(109) = {40, 44};
Line(110) = {41, 45};
Line Loop(111) = {107, 103, -108, -99};
Line Loop(112) = {110, 106, -107, -102};
Line Loop(113) = {109, 105, -110, -101};
Line Loop(114) = {100, 109, -104, -108};
Plane Surface(115) = {111};
Plane Surface(116) = {112};
Plane Surface(117) = {113};
Plane Surface(118) = {114};
Line Loop(119) = {103, 104, 105, 106, -61, -63, -65, -67};
Line Loop(120) = {99, 100, 101, 102, -1, -2, -3, -4, -21, -22, -23, -24, -41, -42, -43, -44, -62, -64, -66, -68};
Plane Surface(121) = {119};
Plane Surface(122) = {120};
Surface Loop(123) = {115, 116, 117, 118, 121, 122, 84, 90, 96, -77, -78, -79, -80};
Volume(124) = {123};

Physical Point("PointReceiver") = {1, 2};
Physical Point("PointSource") = {3};
Physical Volume("mat2") = {86, 92, 98};
Physical Volume("mat1") = {124};
"""
        self.mesh_equal_string(simple_3d, expected)
