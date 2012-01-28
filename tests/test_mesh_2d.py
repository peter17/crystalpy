# -*- coding: utf-8 -*-

from tests import GeneratorTestCase
from generator import InclusionType


class Mesh2DTests(GeneratorTestCase):
    def test_square_mesh_2d(self):
        map_simple = [[1, 1],
                      [1, 2]]
        holes = InclusionType(type = 'hole',
                              shape = 'ellipse',
                              dim_x = 150,
                              dim_y = 100,
                              dim_z = 300,
                              el_size = 30,
                              color = 'lightgrey')
        type1 = InclusionType(type = 'inclusion',
                              shape = 'rectangle',
                              tag = 'mat2',
                              dim_x = 150,
                              dim_y = 100,
                              dim_z = 150,
                              el_size = 25,
                              color = 'grey')
        simple_2d = \
            {'dim_x': 500,
             'dim_y': 500,
             'dim_z': 0,
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
Point(5) = {-200.0, -75.0, 0, size_1};
Point(6) = {-200.0, -175.0, 0, size_1};
Point(7) = {-50.0, -75.0, 0, size_1};
Point(8) = {-50.0, -175.0, 0, size_1};
Point(9) = {-200.0, 175.0, 0, size_1};
Point(10) = {-200.0, 75.0, 0, size_1};
Point(11) = {-50.0, 175.0, 0, size_1};
Point(12) = {-50.0, 75.0, 0, size_1};
Point(13) = {-200.0, 175.0, 0, size_1};
Point(14) = {-200.0, 75.0, 0, size_1};
Point(15) = {-50.0, 175.0, 0, size_1};
Point(16) = {-50.0, 75.0, 0, size_1};
Point(17) = {50.0, -75.0, 0, size_1};
Point(18) = {50.0, -175.0, 0, size_1};
Point(19) = {200.0, -75.0, 0, size_1};
Point(20) = {200.0, -175.0, 0, size_1};
Point(21) = {50.0, -75.0, 0, size_1};
Point(22) = {50.0, -175.0, 0, size_1};
Point(23) = {200.0, -75.0, 0, size_1};
Point(24) = {200.0, -175.0, 0, size_1};
Point(25) = {125, 125, 0, size_2};
Point(26) = {50.0, 125, 0, size_2};
Point(27) = {200.0, 125, 0, size_2};
Point(28) = {125, 175.0, 0, size_2};
Point(29) = {125, 75.0, 0, size_2};
Point(30) = {-250.0, 250.0, 0, size_bulk};
Point(31) = {-250.0, -250.0, 0, size_bulk};
Point(32) = {250.0, 250.0, 0, size_bulk};
Point(33) = {250.0, -250.0, 0, size_bulk};

Line(1) = {2, 1};
Line(2) = {1, 3};
Line(3) = {3, 4};
Line(4) = {4, 2};
Line(5) = {6, 5};
Line(6) = {5, 7};
Line(7) = {7, 8};
Line(8) = {8, 6};
Line(9) = {10, 9};
Line(10) = {9, 11};
Line(11) = {11, 12};
Line(12) = {12, 10};
Line(13) = {14, 13};
Line(14) = {13, 15};
Line(15) = {15, 16};
Line(16) = {16, 14};
Line(17) = {18, 17};
Line(18) = {17, 19};
Line(19) = {19, 20};
Line(20) = {20, 18};
Line(21) = {22, 21};
Line(22) = {21, 23};
Line(23) = {23, 24};
Line(24) = {24, 22};
Ellipse(25) = {26, 25, 27, 28};
Ellipse(26) = {28, 25, 29, 27};
Ellipse(27) = {27, 25, 26, 29};
Ellipse(28) = {29, 25, 28, 26};
Line(29) = {31, 30};
Line(30) = {30, 32};
Line(31) = {32, 33};
Line(32) = {33, 31};
Line Loop(33) = {29, 30, 31, 32, -1, -2, -3, -4, -9, -10, -11, -12, -17, -18, -19, -20, -25, -26, -27, -28};
Plane Surface(34) = {33};
Line Loop(35) = {5, 6, 7, 8};
Plane Surface(36) = {35};
Line Loop(37) = {13, 14, 15, 16};
Plane Surface(38) = {37};
Line Loop(39) = {21, 22, 23, 24};
Plane Surface(40) = {39};

Physical Surface("mat1") = {34};
Physical Surface("mat2") = {36, 38, 40};
"""
        self.mesh_equal_string(simple_2d, expected)
