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
        simple_3d = \
            {'dim_x': 500,
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
             'map': map_simple,
             'inclusion_types': [None, type1, holes]}
        expected = """size_bulk = 25;
size_1 = 25;
size_2 = 30;

Point(1) = {-200.0, -75.0, 0, size_1};
Point(2) = {-200.0, -175.0, 0, size_1};
Point(3) = {-50.0, -75.0, 0, size_1};
Point(4) = {-50.0, -175.0, 0, size_1};
Point(5) = {-200.0, -75.0, -150, size_1};
Point(6) = {-200.0, -175.0, -150, size_1};
Point(7) = {-50.0, -75.0, -150, size_1};
Point(8) = {-50.0, -175.0, -150, size_1};
Point(9) = {-200.0, 175.0, 0, size_1};
Point(10) = {-200.0, 75.0, 0, size_1};
Point(11) = {-50.0, 175.0, 0, size_1};
Point(12) = {-50.0, 75.0, 0, size_1};
Point(13) = {-200.0, 175.0, -150, size_1};
Point(14) = {-200.0, 75.0, -150, size_1};
Point(15) = {-50.0, 175.0, -150, size_1};
Point(16) = {-50.0, 75.0, -150, size_1};
Point(17) = {50.0, -75.0, 0, size_1};
Point(18) = {50.0, -175.0, 0, size_1};
Point(19) = {200.0, -75.0, 0, size_1};
Point(20) = {200.0, -175.0, 0, size_1};
Point(21) = {50.0, -75.0, -150, size_1};
Point(22) = {50.0, -175.0, -150, size_1};
Point(23) = {200.0, -75.0, -150, size_1};
Point(24) = {200.0, -175.0, -150, size_1};
Point(25) = {125, 125, 0, size_2};
Point(26) = {50.0, 125, 0, size_2};
Point(27) = {200.0, 125, 0, size_2};
Point(28) = {125, 175.0, 0, size_2};
Point(29) = {125, 75.0, 0, size_2};
Point(30) = {125, 125, 300, size_2};
Point(31) = {50.0, 125, 300, size_2};
Point(32) = {200.0, 125, 300, size_2};
Point(33) = {125, 175.0, 300, size_2};
Point(34) = {125, 75.0, 300, size_2};
Point(35) = {-250.0, 250.0, 0, size_bulk};
Point(36) = {-250.0, -250.0, 0, size_bulk};
Point(37) = {250.0, 250.0, 0, size_bulk};
Point(38) = {250.0, -250.0, 0, size_bulk};
Point(39) = {-250.0, 250.0, 300, size_bulk};
Point(40) = {-250.0, -250.0, 300, size_bulk};
Point(41) = {250.0, 250.0, 300, size_bulk};
Point(42) = {250.0, -250.0, 300, size_bulk};

Line(1) = {2, 1};
Line(2) = {1, 3};
Line(3) = {3, 4};
Line(4) = {4, 2};
Line(5) = {6, 5};
Line(6) = {5, 7};
Line(7) = {7, 8};
Line(8) = {8, 6};
Line(9) = {2, 6};
Line(10) = {1, 5};
Line(11) = {3, 7};
Line(12) = {4, 8};
Line Loop(13) = {9, 5, -10, -1};
Line Loop(14) = {12, 8, -9, -4};
Line Loop(15) = {11, 7, -12, -3};
Line Loop(16) = {2, 11, -6, -10};
Plane Surface(17) = {13};
Plane Surface(18) = {14};
Plane Surface(19) = {15};
Plane Surface(20) = {16};
Line(21) = {10, 9};
Line(22) = {9, 11};
Line(23) = {11, 12};
Line(24) = {12, 10};
Line(25) = {14, 13};
Line(26) = {13, 15};
Line(27) = {15, 16};
Line(28) = {16, 14};
Line(29) = {10, 14};
Line(30) = {9, 13};
Line(31) = {11, 15};
Line(32) = {12, 16};
Line Loop(33) = {29, 25, -30, -21};
Line Loop(34) = {32, 28, -29, -24};
Line Loop(35) = {31, 27, -32, -23};
Line Loop(36) = {22, 31, -26, -30};
Plane Surface(37) = {33};
Plane Surface(38) = {34};
Plane Surface(39) = {35};
Plane Surface(40) = {36};
Line(41) = {18, 17};
Line(42) = {17, 19};
Line(43) = {19, 20};
Line(44) = {20, 18};
Line(45) = {22, 21};
Line(46) = {21, 23};
Line(47) = {23, 24};
Line(48) = {24, 22};
Line(49) = {18, 22};
Line(50) = {17, 21};
Line(51) = {19, 23};
Line(52) = {20, 24};
Line Loop(53) = {49, 45, -50, -41};
Line Loop(54) = {52, 48, -49, -44};
Line Loop(55) = {51, 47, -52, -43};
Line Loop(56) = {42, 51, -46, -50};
Plane Surface(57) = {53};
Plane Surface(58) = {54};
Plane Surface(59) = {55};
Plane Surface(60) = {56};
Ellipse(61) = {31, 30, 32, 33};
Ellipse(62) = {26, 25, 27, 28};
Ellipse(63) = {33, 30, 34, 32};
Ellipse(64) = {28, 25, 29, 27};
Ellipse(65) = {32, 30, 31, 34};
Ellipse(66) = {27, 25, 26, 29};
Ellipse(67) = {34, 30, 33, 31};
Ellipse(68) = {29, 25, 28, 26};
Line(69) = {26, 31};
Line(70) = {28, 33};
Line(71) = {27, 32};
Line(72) = {29, 34};
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
Line(99) = {36, 35};
Line(100) = {35, 37};
Line(101) = {37, 38};
Line(102) = {38, 36};
Line(103) = {40, 39};
Line(104) = {39, 41};
Line(105) = {41, 42};
Line(106) = {42, 40};
Line(107) = {36, 40};
Line(108) = {35, 39};
Line(109) = {37, 41};
Line(110) = {38, 42};
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

Physical Volume("mat2") = {86, 92, 98};
Physical Volume("mat1") = {124};
"""
        self.mesh_equal_string(simple_3d, expected)
