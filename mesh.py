# -*- coding: utf-8 -*-
"""Script for generating crystal meshes and images."""

from __future__ import division
from generator import Crystal, InclusionType

__copyright__ = "© 2012 Peter Potrowl <peter017@gmail.com>"

__license__ = """
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see U{http://www.gnu.org/licenses/}.
"""

name = "MyCrystal"
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
    {'name': name,
     'dim_x': 500,
     'dim_y': 500,
     'dim_z': 300,
     'periodicity': (True, True, True),
     'nb_x': 2,
     'nb_y': 2,
     'space_x': 250,
     'space_y': 250,
     'pos_x': 0,
     'pos_y': 0,
     'crystal_shape': 'square',
     'el_size_bulk': 25,
     'bulk_tag': 'mat1',
     'inclusion_map': map_simple,
     'inclusion_types': [None, type1, holes],
     'physical_point_map': physical_point_map,
     'physical_line_map': physical_line_map}
my_crystal = Crystal(**simple_3d)
my_mesh = my_crystal.mesh()
file = open('%s.geo' % name, 'w')
file.write(my_mesh)
file.close()
print 'Geo saved'
my_svg = my_crystal.image()
my_svg.save('%s.svg' % name)
print 'SVG saved'
