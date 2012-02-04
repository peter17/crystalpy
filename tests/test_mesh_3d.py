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
        physical_line_map = \
            [('LineReceiver', [(-150, -20, 300), (-150, 20, 300)])]
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
             'physical_point_map': physical_point_map,
             'physical_line_map': physical_line_map}
        expected = """//Mesh3D, created with crystalpy
size_bulk = 25;
size_1 = 25;
size_2 = 30;

Point(1) = {0, 0, 0, 25};
Point(2) = {150, 0, 0, 25};
Point(3) = {0, 0, 150, 25};
Point(4) = {-150, 20, 300, 25};
Point(5) = {-150, -20, 300, 25};
Point(6) = {-200.0, -75.0, 0, size_1};
Point(7) = {-200.0, -175.0, 0, size_1};
Point(8) = {-50.0, -75.0, 0, size_1};
Point(9) = {-50.0, -175.0, 0, size_1};
Point(10) = {-200.0, -75.0, -150, size_1};
Point(11) = {-200.0, -175.0, -150, size_1};
Point(12) = {-50.0, -75.0, -150, size_1};
Point(13) = {-50.0, -175.0, -150, size_1};
Point(14) = {-200.0, 175.0, 0, size_1};
Point(15) = {-200.0, 75.0, 0, size_1};
Point(16) = {-50.0, 175.0, 0, size_1};
Point(17) = {-50.0, 75.0, 0, size_1};
Point(18) = {-200.0, 175.0, -150, size_1};
Point(19) = {-200.0, 75.0, -150, size_1};
Point(20) = {-50.0, 175.0, -150, size_1};
Point(21) = {-50.0, 75.0, -150, size_1};
Point(22) = {50.0, -75.0, 0, size_1};
Point(23) = {50.0, -175.0, 0, size_1};
Point(24) = {200.0, -75.0, 0, size_1};
Point(25) = {200.0, -175.0, 0, size_1};
Point(26) = {50.0, -75.0, -150, size_1};
Point(27) = {50.0, -175.0, -150, size_1};
Point(28) = {200.0, -75.0, -150, size_1};
Point(29) = {200.0, -175.0, -150, size_1};
Point(30) = {125, 125, 0, size_2};
Point(31) = {50.0, 125, 0, size_2};
Point(32) = {200.0, 125, 0, size_2};
Point(33) = {125, 175.0, 0, size_2};
Point(34) = {125, 75.0, 0, size_2};
Point(35) = {125, 125, 300, size_2};
Point(36) = {50.0, 125, 300, size_2};
Point(37) = {200.0, 125, 300, size_2};
Point(38) = {125, 175.0, 300, size_2};
Point(39) = {125, 75.0, 300, size_2};
Point(40) = {-250.0, 250.0, 0, size_bulk};
Point(41) = {-250.0, -250.0, 0, size_bulk};
Point(42) = {250.0, 250.0, 0, size_bulk};
Point(43) = {250.0, -250.0, 0, size_bulk};
Point(44) = {-250.0, 250.0, 300, size_bulk};
Point(45) = {-250.0, -250.0, 300, size_bulk};
Point(46) = {250.0, 250.0, 300, size_bulk};
Point(47) = {250.0, -250.0, 300, size_bulk};

Line(1) = {4, 5};
Line(2) = {7, 6};
Line(3) = {6, 8};
Line(4) = {8, 9};
Line(5) = {9, 7};
Line(6) = {11, 10};
Line(7) = {10, 12};
Line(8) = {12, 13};
Line(9) = {13, 11};
Line(10) = {7, 11};
Line(11) = {6, 10};
Line(12) = {8, 12};
Line(13) = {9, 13};
Line Loop(14) = {10, 6, -11, -2};
Line Loop(15) = {13, 9, -10, -5};
Line Loop(16) = {12, 8, -13, -4};
Line Loop(17) = {3, 12, -7, -11};
Plane Surface(18) = {14};
Plane Surface(19) = {15};
Plane Surface(20) = {16};
Plane Surface(21) = {17};
Line(22) = {15, 14};
Line(23) = {14, 16};
Line(24) = {16, 17};
Line(25) = {17, 15};
Line(26) = {19, 18};
Line(27) = {18, 20};
Line(28) = {20, 21};
Line(29) = {21, 19};
Line(30) = {15, 19};
Line(31) = {14, 18};
Line(32) = {16, 20};
Line(33) = {17, 21};
Line Loop(34) = {30, 26, -31, -22};
Line Loop(35) = {33, 29, -30, -25};
Line Loop(36) = {32, 28, -33, -24};
Line Loop(37) = {23, 32, -27, -31};
Plane Surface(38) = {34};
Plane Surface(39) = {35};
Plane Surface(40) = {36};
Plane Surface(41) = {37};
Line(42) = {23, 22};
Line(43) = {22, 24};
Line(44) = {24, 25};
Line(45) = {25, 23};
Line(46) = {27, 26};
Line(47) = {26, 28};
Line(48) = {28, 29};
Line(49) = {29, 27};
Line(50) = {23, 27};
Line(51) = {22, 26};
Line(52) = {24, 28};
Line(53) = {25, 29};
Line Loop(54) = {50, 46, -51, -42};
Line Loop(55) = {53, 49, -50, -45};
Line Loop(56) = {52, 48, -53, -44};
Line Loop(57) = {43, 52, -47, -51};
Plane Surface(58) = {54};
Plane Surface(59) = {55};
Plane Surface(60) = {56};
Plane Surface(61) = {57};
Ellipse(62) = {36, 35, 37, 38};
Ellipse(63) = {31, 30, 32, 33};
Ellipse(64) = {38, 35, 39, 37};
Ellipse(65) = {33, 30, 34, 32};
Ellipse(66) = {37, 35, 36, 39};
Ellipse(67) = {32, 30, 31, 34};
Ellipse(68) = {39, 35, 38, 36};
Ellipse(69) = {34, 30, 33, 31};
Line(70) = {31, 36};
Line(71) = {33, 38};
Line(72) = {32, 37};
Line(73) = {34, 39};
Line Loop(74) = {63, 71, -62, -70};
Line Loop(75) = {65, 72, -64, -71};
Line Loop(76) = {67, 73, -66, -72};
Line Loop(77) = {69, 70, -68, -73};
Ruled Surface(78) = {74};
Ruled Surface(79) = {75};
Ruled Surface(80) = {76};
Ruled Surface(81) = {77};
Line Loop(82) = {6, 7, 8, 9};
Line Loop(83) = {2, 3, 4, 5};
Plane Surface(84) = {82};
Plane Surface(85) = {83};
Surface Loop(86) = {18, 19, 20, 21, 84, 85};
Volume(87) = {86};
Line Loop(88) = {26, 27, 28, 29};
Line Loop(89) = {22, 23, 24, 25};
Plane Surface(90) = {88};
Plane Surface(91) = {89};
Surface Loop(92) = {38, 39, 40, 41, 90, 91};
Volume(93) = {92};
Line Loop(94) = {46, 47, 48, 49};
Line Loop(95) = {42, 43, 44, 45};
Plane Surface(96) = {94};
Plane Surface(97) = {95};
Surface Loop(98) = {58, 59, 60, 61, 96, 97};
Volume(99) = {98};
Line(100) = {41, 40};
Line(101) = {40, 42};
Line(102) = {42, 43};
Line(103) = {43, 41};
Line(104) = {45, 44};
Line(105) = {44, 46};
Line(106) = {46, 47};
Line(107) = {47, 45};
Line(108) = {41, 45};
Line(109) = {40, 44};
Line(110) = {42, 46};
Line(111) = {43, 47};
Line Loop(112) = {108, 104, -109, -100};
Line Loop(113) = {111, 107, -108, -103};
Line Loop(114) = {110, 106, -111, -102};
Line Loop(115) = {101, 110, -105, -109};
Plane Surface(116) = {112};
Plane Surface(117) = {113};
Plane Surface(118) = {114};
Plane Surface(119) = {115};
Line Loop(120) = {104, 105, 106, 107, -62, -64, -66, -68};
Line Loop(121) = {100, 101, 102, 103, -2, -3, -4, -5, -22, -23, -24, -25, -42, -43, -44, -45, -63, -65, -67, -69};
Plane Surface(122) = {120};
Plane Surface(123) = {121};
Surface Loop(124) = {116, 117, 118, 119, 122, 123, 85, 91, 97, -78, -79, -80, -81};
Volume(125) = {124};

Physical Point("PointReceiver") = {1, 2};
Physical Point("PointSource") = {3};
Physical Line("LineReceiver") = {1};
Physical Volume("mat2") = {87, 93, 99};
Line{1} In Surface {122};
Physical Volume("mat1") = {125};
"""
        self.mesh_equal_string(simple_3d, expected)
