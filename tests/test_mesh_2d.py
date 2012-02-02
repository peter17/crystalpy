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
        physical_point_map = \
            [('PointReceiver', [(0, 0, 0), (150, 0, 0)]),
             ('PointSource', [(0, 0, 150)])]
        simple_2d = \
            {'name': 'Mesh2D',
             'dim_x': 500,
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
             'inclusion_map': map_simple,
             'inclusion_types': [None, type1, holes],
             'physical_point_map': physical_point_map}
        expected = """//Mesh2D, created with crystalpy
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
Point(8) = {-200.0, 175.0, 0, size_1};
Point(9) = {-200.0, 75.0, 0, size_1};
Point(10) = {-50.0, 175.0, 0, size_1};
Point(11) = {-50.0, 75.0, 0, size_1};
Point(12) = {50.0, -75.0, 0, size_1};
Point(13) = {50.0, -175.0, 0, size_1};
Point(14) = {200.0, -75.0, 0, size_1};
Point(15) = {200.0, -175.0, 0, size_1};
Point(16) = {125, 125, 0, size_2};
Point(17) = {50.0, 125, 0, size_2};
Point(18) = {200.0, 125, 0, size_2};
Point(19) = {125, 175.0, 0, size_2};
Point(20) = {125, 75.0, 0, size_2};
Point(21) = {-250.0, 250.0, 0, size_bulk};
Point(22) = {-250.0, -250.0, 0, size_bulk};
Point(23) = {250.0, 250.0, 0, size_bulk};
Point(24) = {250.0, -250.0, 0, size_bulk};

Line(1) = {5, 4};
Line(2) = {4, 6};
Line(3) = {6, 7};
Line(4) = {7, 5};
Line(5) = {9, 8};
Line(6) = {8, 10};
Line(7) = {10, 11};
Line(8) = {11, 9};
Line(9) = {13, 12};
Line(10) = {12, 14};
Line(11) = {14, 15};
Line(12) = {15, 13};
Ellipse(13) = {17, 16, 18, 19};
Ellipse(14) = {19, 16, 20, 18};
Ellipse(15) = {18, 16, 17, 20};
Ellipse(16) = {20, 16, 19, 17};
Line(17) = {22, 21};
Line(18) = {21, 23};
Line(19) = {23, 24};
Line(20) = {24, 22};
Line Loop(21) = {17, 18, 19, 20, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16};
Plane Surface(22) = {21};
Line Loop(23) = {1, 2, 3, 4};
Plane Surface(24) = {23};
Line Loop(25) = {5, 6, 7, 8};
Plane Surface(26) = {25};
Line Loop(27) = {9, 10, 11, 12};
Plane Surface(28) = {27};

Physical Point("PointReceiver") = {1, 2};
Physical Point("PointSource") = {3};
Physical Surface("mat1") = {22};
Physical Surface("mat2") = {24, 26, 28};
"""
        self.mesh_equal_string(simple_2d, expected)
