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
        type1 = InclusionType(type = 'plot',
                              shape = 'rectangle',
                              tag = 'mat2',
                              dim_x = 150,
                              dim_y = 100,
                              dim_z = 150,
                              el_size = 25,
                              color = 'grey')
        simple_2d = \
            {'name': 'Image2D',
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
             'physical_point_map': [],
             'physical_line_map': []}
        expected = """<svg xmlns="http://www.w3.org/2000/svg" version="1.1" x="Image2D" xmlns:xlink="http://www.w3.org/1999/xlink"  >
<rect style="stroke-width:5.0; " height="500" width="500" stroke="black" y="-250.0" x="-250.0" fill="white"  />
<rect style="stroke-width:1.5; " height="100" width="150" stroke="black" y="-175.0" x="-200.0" fill="grey"  />
<rect style="stroke-width:1.5; " height="100" width="150" stroke="black" y="75.0" x="-200.0" fill="grey"  />
<rect style="stroke-width:1.5; " height="100" width="150" stroke="black" y="-175.0" x="50.0" fill="grey"  />
<ellipse style="stroke-width:1.5; " rx="75.0" ry="50.0" stroke="black" cy="125" cx="125" fill="lightgrey"  />
</svg>
"""
        self.image_equal_string(simple_2d, expected)
