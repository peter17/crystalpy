# -*- coding: utf-8 -*-
"""Script for generating crystal meshes."""

from __future__ import division
from generator import InclusionType, Mesh, Value

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

map_simple = [[1, 1],
              [1, 2]]
size_inclusions = Value('size_inclusions', 250)
holes = InclusionType('hole',
                      radius = 90,
                      el_size = Value('size_holes', 300))
type1 = InclusionType('inclusion',
                      tag = 'mat2',
                      radius = 100,
                      el_size = size_inclusions)
kwargs = {'dim_x': 500,
          'dim_y': 500,
          'dim_z': 0,
          'periodicity': (False, True, False),
          'nb_x': 2,
          'nb_y': 2,
          'space_x': 250,
          'space_y': 250,
          'pos_x': -125,
          'pos_y': -125,
          'el_size_bulk': Value('size_bulk', 150),
          'bulk_tag': 'mat1',
          'inclusion_tag': 'mat2',
          'map': map_simple,
          'inclusion_types': [None, type1, holes]}
my_crystal = Mesh(**kwargs)
file = open('MyCrystal.geo', 'w')
file.write("%s" % my_crystal)
file.close()
print 'Geo saved'
