# -*- coding: utf-8 -*-
"""Script for generating crystal meshes and images."""

from __future__ import division
import pysvg
from pysvg.core import *
from pysvg.structure import *
from pysvg.shape import *

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


class Value:
    instances = {}

    def __init__(self, name, value):
        self.name = name
        self.value = value
        assert name not in Value.instances.keys()
        Value.instances[name] = self

    def __repr__(self):
        return "%s = %s;\n" % (self.name, self.value)

    def print_all():
        result = ''
        for value in Value.instances.values():
            result += '%r' % value
        return result

    print_all = staticmethod(print_all)


class Point:
    instances = []

    def __init__(self, x, y, z, size):
        self.x = x
        self.y = y
        self.z = z

        if isinstance(size, Value):
            self.size = size.name
        else:
            self.size = size

        Point.instances.append(self)
        self.id = len(Point.instances)

    def __repr__(self):
        return ("Point(%d) = {%s, %s, %s, %s};\n"
                % (self.id, self.x, self.y, self.z, self.size))

    def print_all():
        result = ''
        for point in Point.instances:
            result += '%r' % point
        return result

    print_all = staticmethod(print_all)


class Line:
    instances = []

    def print_all():
        result = ''
        for line in Line.instances:
            result += '%r' % line
        return result

    print_all = staticmethod(print_all)


class StraightLine(Line):
    def __init__(self, pt1, pt2):
        self.pt1_id = pt1.id
        self.pt2_id = pt2.id

        Line.instances.append(self)
        self.id = len(Line.instances)

    def __repr__(self):
        return ("Line(%d) = {%s, %s};\n"
                % (self.id, self.pt1_id, self.pt2_id))


class PeriodicLine(Line):
    def __init__(self, line1, line2):
        self.line1_id = line1.id
        self.line2_id = line2.id

        Line.instances.append(self)
        self.id = len(Line.instances)

    def __repr__(self):
        return ("Periodic Line(%d) = {-%s};\n"
                % (self.line1_id, self.line2_id))


class LineLoop:
    def __init__(self, pos_lines, neg_lines=[]):
        self.pos_lines_list = ', '.join(["%r" % line.id for line in pos_lines])
        self.neg_lines_list = ', '.join(["-%r" % line.id for line in neg_lines])
        if neg_lines != []:
            self.neg_lines_list = ', ' + self.neg_lines_list

        Line.instances.append(self)
        self.id = len(Line.instances)

    def __repr__(self):
        return ("Line Loop(%s) = {%s%s};\n"
                % (self.id, self.pos_lines_list, self.neg_lines_list))


class PlaneSurface:
    def __init__(self, loop):
        self.loop = loop

        Line.instances.append(self)
        self.id = len(Line.instances)

    def __repr__(self):
        return ("Plane Surface(%s) = {%s};\n"
                % (self.id, self.loop.id))


class PhysicalEntity:
    instances = []

    def print_all():
        result = ''
        for line in PhysicalEntity.instances:
            result += '%r' % line
        return result

    print_all = staticmethod(print_all)


class PhysicalLine:
    def __init__(self, line, name):
        self.line_id = line.id
        self.name = name

        PhysicalEntity.instances.append(self)

    def __repr__(self):
        return ('Physical Line("%s") = {%s};\n'
                % (self.name, self.line_id))


class PhysicalSurface:
    def __init__(self, surfaces, name):
        self.surfaces = ', '.join([format(surface.id) for surface in surfaces])
        self.name = name

        PhysicalEntity.instances.append(self)

    def __repr__(self):
        return ('Physical Surface("%s") = {%s};\n'
                % (self.name, self.surfaces))


class Rectangle():
    def __init__(self,
                 dim_x,
                 dim_y,
                 pos_x,
                 pos_y,
                 pos_z,
                 el_size,
                 periodicity):

        self.el_size = el_size

        pt_tl = Point(pos_x - dim_x / 2, pos_y + dim_y / 2, pos_z, el_size)
        pt_bl = Point(pos_x - dim_x / 2, pos_y - dim_y / 2, pos_z, el_size)
        pt_tr = Point(pos_x + dim_x / 2, pos_y + dim_y / 2, pos_z, el_size)
        pt_br = Point(pos_x + dim_x / 2, pos_y - dim_y / 2, pos_z, el_size)

        line_left = StraightLine(pt_bl, pt_tl)
        line_top = StraightLine(pt_tl, pt_tr)
        line_right = StraightLine(pt_tr, pt_br)
        line_bottom = StraightLine(pt_br, pt_bl)

        self.lines = [line_left, line_top, line_right, line_bottom]

        if periodicity[0]:
            PeriodicLine(line_left, line_right)
            PhysicalLine(line_left, 'minus_x')
            PhysicalLine(line_right, 'plus_x')
        if periodicity[1]:
            PeriodicLine(line_bottom, line_top)
            PhysicalLine(line_bottom, 'minus_y')
            PhysicalLine(line_top, 'plus_y')


class Circle(Line):
    def __init__(self, pt_l, pt_c, pt_r):
        self.pt_l = pt_l.id
        self.pt_c = pt_c.id
        self.pt_r = pt_r.id

        Line.instances.append(self)
        self.id = len(Line.instances)

    def __repr__(self):
        return ("Circle(%s) = {%s, %s, %s};\n"
               % (self.id, self.pt_l, self.pt_c, self.pt_r))


class FullCircle:
    def __init__(self,
                 radius,
                 pos_x,
                 pos_y,
                 pos_z,
                 el_size):

        self.el_size = el_size

        pt_c = Point(pos_x, pos_y, pos_z, el_size)
        pt_l = Point(pos_x - radius, pos_y, pos_z, el_size)
        pt_r = Point(pos_x + radius, pos_y, pos_z, el_size)

        circle_top = Circle(pt_l, pt_c, pt_r)
        circle_bottom = Circle(pt_r, pt_c, pt_l)

        self.lines = [circle_top, circle_bottom]


class Matrix:
    def __init__(self,
                 dim_x,
                 dim_y,
                 pos_x,
                 pos_y,
                 pos_z,
                 el_size,
                 periodicity,
                 tag):
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.el_size = el_size
        self.periodicity = periodicity
        self.tag = tag

    def image(self):
        return pysvg.shape.rect(self.pos_x - self.dim_x / 2,
                                self.pos_y - self.dim_y / 2,
                                self.dim_x,
                                self.dim_y,
                                stroke='black',
                                fill='white')

    def mesh(self):
        return Rectangle(self.dim_x, self.dim_y,
                         self.pos_x, self.pos_y, self.pos_z,
                         self.el_size, self.periodicity)


class Inclusion:
    instances = []

    def __init__(self,
                 type,
                 pos_x,
                 pos_y,
                 pos_z):
        self.type = type
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        Inclusion.instances.append(self)

    def image(self):
        return pysvg.shape.circle(self.pos_x,
                                  self.pos_y,
                                  self.type.radius,
                                  stroke='black',
                                  fill=self.type.color)

    def mesh(self):
        return FullCircle(self.type.radius,
                          self.pos_x, self.pos_y, self.pos_z,
                          self.type.el_size)


class Crystal:
    def __init__(self,
                 dim_x,
                 dim_y,
                 dim_z,
                 periodicity,
                 nb_x,
                 nb_y,
                 space_x,
                 space_y,
                 pos_x,
                 pos_y,
                 crystal_shape,  # square or hexa
                 el_size_bulk,
                 bulk_tag,
                 inclusion_tag,
                 map,
                 inclusion_types):
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.dim_z = dim_z

        assert dim_z == 0, '3D meshes are not supported yet'
        if map is not None:
            assert len(map) == nb_y, "Wrong map size!"
            assert len(map[0]) == nb_x, "Wrong map size!"
        assert crystal_shape in ['square', 'hexa'], "Wrong crystal type!"

        self.matrix = Matrix(dim_x, dim_y, 0, 0, 0,
                             el_size_bulk, periodicity, bulk_tag)

        for i in range(nb_x):
            for j in range(nb_y):
                if crystal_shape == 'hexa' and j % 2 == 1:
                    x = pos_x + i * space_x + space_x / 2
                    y = pos_y + j * space_y
                else:
                    x = pos_x + i * space_x
                    y = pos_y + j * space_y
                type_id = 0 if map is None else map[j][i]
                type = inclusion_types[type_id]
                if type is not None:
                    Inclusion(type, x, y, 0)

    def image(self, filename):
        mysvg = pysvg.structure.svg("My periodic structure")
        mysvg.addElement(self.matrix.image())
        for inclusion in Inclusion.instances:
            mysvg.addElement(inclusion.image())
        mysvg.save(filename)

    def mesh(self):
        inclusions_lines_all = []
        inclusions_lines_by_tag = {}

        for inclusion in Inclusion.instances:
            for line in inclusion.mesh().lines:
                inclusions_lines_all.append(line)
            if inclusion.type.type != 'hole':
                if inclusion.type.tag not in inclusions_lines_by_tag.keys():
                    inclusions_lines_by_tag[inclusion.type.tag] = []
                inclusions_lines_by_tag[inclusion.type.tag].append(inclusion.mesh().lines)

        loop = LineLoop(self.matrix.mesh().lines, inclusions_lines_all)
        surface = PlaneSurface(loop)
        PhysicalSurface([surface], self.matrix.tag)

        for tag, inclusion_lines in inclusions_lines_by_tag.iteritems():
            inclusion_surfaces = []
            for lines in inclusion_lines:
                loop = LineLoop(lines)
                inclusion_surfaces.append(PlaneSurface(loop))
            PhysicalSurface(inclusion_surfaces, tag)

        result = Value.print_all() + '\n'
        result += Point.print_all() + '\n'
        result += Line.print_all() + '\n'
        result += PhysicalEntity.print_all()
        return result


class InclusionType:
    def __init__(self,
                 type,
                 radius,
                 el_size,
                 tag=None,
                 color='lightgrey'):
        """
        @param type: 'inclusion' (matter) or 'hole' (void)
        @param tag: what to tag in the mesh for those inclusions
        """
        self.type = type
        self.tag = tag
        self.radius = radius
        self.el_size = el_size
        self.color = color
