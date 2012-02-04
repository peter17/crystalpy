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
             ('PointSource', [(-150, 0, 0)])]
        physical_line_map = \
            [('LineReceiver', [(-150, -30, 0), (-150, 30, 0),
                               (-100, -30, 0), (-100, 30, 0)])]
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
             'physical_point_map': physical_point_map,
             'physical_line_map': physical_line_map}
        expected = """//Mesh2D, created with crystalpy
size_bulk = 25;
size_1 = 25;
size_2 = 30;

Point(1) = {0, 0, 0, 25};
Point(2) = {150, 0, 0, 25};
Point(3) = {-150, 0, 0, 25};
Point(4) = {-100, 30, 0, 25};
Point(5) = {-100, -30, 0, 25};
Point(6) = {-150, 30, 0, 25};
Point(7) = {-150, -30, 0, 25};
Point(8) = {-200.0, -75.0, 0, size_1};
Point(9) = {-200.0, -175.0, 0, size_1};
Point(10) = {-50.0, -75.0, 0, size_1};
Point(11) = {-50.0, -175.0, 0, size_1};
Point(12) = {-200.0, 175.0, 0, size_1};
Point(13) = {-200.0, 75.0, 0, size_1};
Point(14) = {-50.0, 175.0, 0, size_1};
Point(15) = {-50.0, 75.0, 0, size_1};
Point(16) = {50.0, -75.0, 0, size_1};
Point(17) = {50.0, -175.0, 0, size_1};
Point(18) = {200.0, -75.0, 0, size_1};
Point(19) = {200.0, -175.0, 0, size_1};
Point(20) = {125, 125, 0, size_2};
Point(21) = {50.0, 125, 0, size_2};
Point(22) = {200.0, 125, 0, size_2};
Point(23) = {125, 175.0, 0, size_2};
Point(24) = {125, 75.0, 0, size_2};
Point(25) = {-250.0, 250.0, 0, size_bulk};
Point(26) = {-250.0, -250.0, 0, size_bulk};
Point(27) = {250.0, 250.0, 0, size_bulk};
Point(28) = {250.0, -250.0, 0, size_bulk};

Line(1) = {4, 5};
Line(2) = {6, 7};
Line(3) = {9, 8};
Line(4) = {8, 10};
Line(5) = {10, 11};
Line(6) = {11, 9};
Line(7) = {13, 12};
Line(8) = {12, 14};
Line(9) = {14, 15};
Line(10) = {15, 13};
Line(11) = {17, 16};
Line(12) = {16, 18};
Line(13) = {18, 19};
Line(14) = {19, 17};
Ellipse(15) = {21, 20, 22, 23};
Ellipse(16) = {23, 20, 24, 22};
Ellipse(17) = {22, 20, 21, 24};
Ellipse(18) = {24, 20, 23, 21};
Line(19) = {26, 25};
Line(20) = {25, 27};
Line(21) = {27, 28};
Line(22) = {28, 26};
Line Loop(23) = {19, 20, 21, 22, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18};
Plane Surface(24) = {23};
Line Loop(25) = {3, 4, 5, 6};
Plane Surface(26) = {25};
Line Loop(27) = {7, 8, 9, 10};
Plane Surface(28) = {27};
Line Loop(29) = {11, 12, 13, 14};
Plane Surface(30) = {29};

Physical Point("PointReceiver") = {1, 2};
Physical Point("PointSource") = {3};
Physical Line("LineReceiver") = {1, 2};
Physical Surface("mat1") = {24};
Line{1} In Surface {24};
Line{2} In Surface {24};
Physical Surface("mat2") = {26, 28, 30};
"""
        self.mesh_equal_string(simple_2d, expected)
