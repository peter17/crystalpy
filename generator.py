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


class RuledSurface:
    def __init__(self, loop):
        self.loop = loop

        Line.instances.append(self)
        self.id = len(Line.instances)

    def __repr__(self):
        return ("Ruled Surface(%s) = {%s};\n"
                % (self.id, self.loop.id))


class Volume:
    def __init__(self, loop):
        self.loop = loop

        Line.instances.append(self)
        self.id = len(Line.instances)

    def __repr__(self):
        return ("Volume(%s) = {%s};\n"
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


class PhysicalVolume:
    def __init__(self, volumes, name):
        self.volumes = ', '.join([format(volume.id) for volume in volumes])
        self.name = name

        PhysicalEntity.instances.append(self)

    def __repr__(self):
        return ('Physical Volume("%s") = {%s};\n'
                % (self.name, self.volumes))


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


class Ellipse(Line):
    def __init__(self, pt_begin, pt_center, pt_axis, pt_end):
        self.pt_begin = pt_begin.id
        self.pt_center = pt_center.id
        self.pt_axis = pt_axis.id
        self.pt_end = pt_end.id

        Line.instances.append(self)
        self.id = len(Line.instances)

    def __repr__(self):
        return ("Ellipse(%s) = {%s, %s, %s, %s};\n"
               % (self.id, self.pt_begin, self.pt_center,
                  self.pt_axis, self.pt_end))


class FullEllipse:
    def __init__(self,
                 size_x,
                 size_y,
                 pos_x,
                 pos_y,
                 pos_z,
                 el_size):

        self.el_size = el_size

        pt_c = Point(pos_x, pos_y, 0, el_size)
        pt_l = Point(pos_x - size_x / 2, pos_y, 0, el_size)
        pt_r = Point(pos_x + size_x / 2, pos_y, 0, el_size)
        pt_t = Point(pos_x, pos_y + size_y / 2, 0, el_size)
        pt_b = Point(pos_x, pos_y - size_y / 2, 0, el_size)

        ellipse_1 = Ellipse(pt_l, pt_c, pt_r, pt_t)
        ellipse_2 = Ellipse(pt_t, pt_c, pt_b, pt_r)
        ellipse_3 = Ellipse(pt_r, pt_c, pt_l, pt_b)
        ellipse_4 = Ellipse(pt_b, pt_c, pt_t, pt_l)

        self.lines = [ellipse_1, ellipse_2, ellipse_3, ellipse_4]


class SurfaceLoop:
    def __init__(self, pos_lines, neg_lines=[]):
        self.pos_lines_list = ', '.join(["%r" % line.id for line in pos_lines])
        self.neg_lines_list = ', '.join(["-%r" % line.id for line in neg_lines])
        if neg_lines != []:
            self.neg_lines_list = ', ' + self.neg_lines_list

        Line.instances.append(self)
        self.id = len(Line.instances)

    def __repr__(self):
        return ("Surface Loop(%s) = {%s%s};\n"
                % (self.id, self.pos_lines_list, self.neg_lines_list))


class CircularCylinder:
    def __init__(self,
                 radius,
                 pos_x,
                 pos_y,
                 dim_z,
                 el_size):

        self.el_size = el_size

        pt_c_bottom = Point(pos_x, pos_y, 0, el_size)
        pt_l_bottom = Point(pos_x - radius, pos_y, 0, el_size)
        pt_r_bottom = Point(pos_x + radius, pos_y, 0, el_size)

        pt_c_top = Point(pos_x, pos_y, dim_z, el_size)
        pt_l_top = Point(pos_x - radius, pos_y, dim_z, el_size)
        pt_r_top = Point(pos_x + radius, pos_y, dim_z, el_size)

        circle_1_top = Circle(pt_l_top, pt_c_top, pt_r_top)
        circle_1_bottom = Circle(pt_l_bottom, pt_c_bottom, pt_r_bottom)

        circle_2_top = Circle(pt_r_top, pt_c_top, pt_l_top)
        circle_2_bottom = Circle(pt_r_bottom, pt_c_bottom, pt_l_bottom)

        line1 = StraightLine(pt_l_bottom, pt_l_top)
        line2 = StraightLine(pt_r_bottom, pt_r_top)

        loop1 = LineLoop([circle_1_bottom, line2], [circle_1_top, line1])
        loop2 = LineLoop([circle_2_bottom, line1], [circle_2_top, line2])

        self.lines_top = [circle_1_top, circle_2_top]
        self.lines_bottom = [circle_1_bottom, circle_2_bottom]

        self.surfaces = []

        self.surfaces.append(RuledSurface(loop1))
        self.surfaces.append(RuledSurface(loop2))

        self.lines = [line1, line2]


class EllipticCylinder:
    def __init__(self,
                 size_x,
                 size_y,
                 pos_x,
                 pos_y,
                 dim_z,
                 el_size):

        self.el_size = el_size

        pt_c_bottom = Point(pos_x, pos_y, 0, el_size)
        pt_l_bottom = Point(pos_x - size_x / 2, pos_y, 0, el_size)
        pt_r_bottom = Point(pos_x + size_x / 2, pos_y, 0, el_size)
        pt_t_bottom = Point(pos_x, pos_y + size_y / 2, 0, el_size)
        pt_b_bottom = Point(pos_x, pos_y - size_y / 2, 0, el_size)

        pt_c_top = Point(pos_x, pos_y, dim_z, el_size)
        pt_l_top = Point(pos_x - size_x / 2, pos_y, dim_z, el_size)
        pt_r_top = Point(pos_x + size_x / 2, pos_y, dim_z, el_size)
        pt_t_top = Point(pos_x, pos_y + size_y / 2, dim_z, el_size)
        pt_b_top = Point(pos_x, pos_y - size_y / 2, dim_z, el_size)

        ellipse_1_top = Ellipse(pt_l_top, pt_c_top, pt_r_top, pt_t_top)
        ellipse_1_bottom = Ellipse(pt_l_bottom, pt_c_bottom, pt_r_bottom, pt_t_bottom)

        ellipse_2_top = Ellipse(pt_t_top, pt_c_top, pt_b_top, pt_r_top)
        ellipse_2_bottom = Ellipse(pt_t_bottom, pt_c_bottom, pt_b_bottom, pt_r_bottom)

        ellipse_3_top = Ellipse(pt_r_top, pt_c_top, pt_l_top, pt_b_top)
        ellipse_3_bottom = Ellipse(pt_r_bottom, pt_c_bottom, pt_l_bottom, pt_b_bottom)

        ellipse_4_top = Ellipse(pt_b_top, pt_c_top, pt_t_top, pt_l_top)
        ellipse_4_bottom = Ellipse(pt_b_bottom, pt_c_bottom, pt_t_bottom, pt_l_bottom)

        line1 = StraightLine(pt_l_bottom, pt_l_top)
        line2 = StraightLine(pt_t_bottom, pt_t_top)
        line3 = StraightLine(pt_r_bottom, pt_r_top)
        line4 = StraightLine(pt_b_bottom, pt_b_top)

        loop1 = LineLoop([ellipse_1_bottom, line2], [ellipse_1_top, line1])
        loop2 = LineLoop([ellipse_2_bottom, line3], [ellipse_2_top, line2])
        loop3 = LineLoop([ellipse_3_bottom, line4], [ellipse_3_top, line3])
        loop4 = LineLoop([ellipse_4_bottom, line1], [ellipse_4_top, line4])

        self.lines_top = [ellipse_1_top, ellipse_2_top, ellipse_3_top, ellipse_4_top]
        self.lines_bottom = [ellipse_1_bottom, ellipse_2_bottom, ellipse_3_bottom, ellipse_4_bottom]

        self.surfaces = []

        self.surfaces.append(RuledSurface(loop1))
        self.surfaces.append(RuledSurface(loop2))
        self.surfaces.append(RuledSurface(loop3))
        self.surfaces.append(RuledSurface(loop4))

        self.lines = [line1, line2, line3, line4]


class Cuboid():
    def __init__(self,
                 dim_x,
                 dim_y,
                 dim_z,
                 pos_x,
                 pos_y,
                 pos_z,
                 el_size,
                 periodicity):

        self.el_size = el_size

        pt_tl_bottom = Point(pos_x - dim_x / 2, pos_y + dim_y / 2, pos_z, el_size)
        pt_bl_bottom = Point(pos_x - dim_x / 2, pos_y - dim_y / 2, pos_z, el_size)
        pt_tr_bottom = Point(pos_x + dim_x / 2, pos_y + dim_y / 2, pos_z, el_size)
        pt_br_bottom = Point(pos_x + dim_x / 2, pos_y - dim_y / 2, pos_z, el_size)

        pt_tl_top = Point(pos_x - dim_x / 2, pos_y + dim_y / 2, pos_z + dim_z, el_size)
        pt_bl_top = Point(pos_x - dim_x / 2, pos_y - dim_y / 2, pos_z + dim_z, el_size)
        pt_tr_top = Point(pos_x + dim_x / 2, pos_y + dim_y / 2, pos_z + dim_z, el_size)
        pt_br_top = Point(pos_x + dim_x / 2, pos_y - dim_y / 2, pos_z + dim_z, el_size)

        line_left_bottom = StraightLine(pt_bl_bottom, pt_tl_bottom)
        line_top_bottom = StraightLine(pt_tl_bottom, pt_tr_bottom)
        line_right_bottom = StraightLine(pt_tr_bottom, pt_br_bottom)
        line_bottom_bottom = StraightLine(pt_br_bottom, pt_bl_bottom)

        line_left_top = StraightLine(pt_bl_top, pt_tl_top)
        line_top_top = StraightLine(pt_tl_top, pt_tr_top)
        line_right_top = StraightLine(pt_tr_top, pt_br_top)
        line_bottom_top = StraightLine(pt_br_top, pt_bl_top)

        line_bottom_left = StraightLine(pt_bl_bottom, pt_bl_top)
        line_top_left = StraightLine(pt_tl_bottom, pt_tl_top)
        line_top_right = StraightLine(pt_tr_bottom, pt_tr_top)
        line_bottom_right = StraightLine(pt_br_bottom, pt_br_top)

        self.lines_top = [line_left_top, line_top_top,
                          line_right_top, line_bottom_top]

        self.lines_bottom = [line_left_bottom, line_top_bottom,
                             line_right_bottom, line_bottom_bottom]

        self.lines = [line_bottom_left, line_top_left,
                      line_top_right, line_bottom_right]

        loop1 = LineLoop([line_bottom_left, line_left_top],
                         [line_top_left, line_left_bottom])
        loop2 = LineLoop([line_bottom_right, line_bottom_top],
                         [line_bottom_left, line_bottom_bottom])
        loop3 = LineLoop([line_top_right, line_right_top],
                         [line_bottom_right, line_right_bottom])
        loop4 = LineLoop([line_top_bottom, line_top_right],
                         [line_top_top, line_top_left])

        self.surfaces = []

        self.surfaces.append(PlaneSurface(loop1))
        self.surfaces.append(PlaneSurface(loop2))
        self.surfaces.append(PlaneSurface(loop3))
        self.surfaces.append(PlaneSurface(loop4))

        if periodicity[0]:
            PeriodicLine(line_left_bottom, line_right_bottom)
            PhysicalLine(line_left_bottom, 'minus_x_bottom')
            PhysicalLine(line_right_bottom, 'plus_x_bottom')
            PeriodicLine(line_left_top, line_right_top)
            PhysicalLine(line_left_top, 'minus_x_top')
            PhysicalLine(line_right_top, 'plus_x_top')
            PeriodicLine(line_bottom_left, line_bottom_right)
            PeriodicLine(line_top_left, line_top_right)
        if periodicity[1]:
            PeriodicLine(line_bottom_bottom, line_top_bottom)
            PhysicalLine(line_bottom_bottom, 'minus_y_bottom')
            PhysicalLine(line_top_bottom, 'plus_y_bottom')
            PeriodicLine(line_bottom_top, line_top_top)
            PhysicalLine(line_bottom_top, 'minus_y_top')
            PhysicalLine(line_top_top, 'plus_y_top')
            PeriodicLine(line_bottom_left, line_top_left)
            PeriodicLine(line_bottom_right, line_top_right)


class Matrix:
    def __init__(self,
                 dim_x,
                 dim_y,
                 dim_z,
                 pos_x,
                 pos_y,
                 pos_z,
                 el_size,
                 periodicity,
                 tag):
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.dim_z = dim_z
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
        if self.dim_z == 0:
            return Rectangle(self.dim_x, self.dim_y,
                             self.pos_x, self.pos_y, self.pos_z,
                             self.el_size, self.periodicity)
        else:
            return Cuboid(self.dim_x, self.dim_y, self.dim_z,
                          self.pos_x, self.pos_y, self.pos_z,
                          self.el_size, self.periodicity)


class Inclusion:
    instances = []

    def __init__(self,
                 type,
                 pos_x,
                 pos_y,
                 dim_z):
        self.type = type
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.dim_z = dim_z
        Inclusion.instances.append(self)

    def image(self):
        if self.type.shape == 'ellipse':
            return pysvg.shape.ellipse(self.pos_x,
                                       self.pos_y,
                                       self.type.dim_x / 2,
                                       self.type.dim_y / 2,
                                       stroke='black',
                                       fill=self.type.color)
        elif self.type.shape == 'rectangle':
            return pysvg.shape.rect(self.pos_x - self.type.dim_x / 2,
                                    self.pos_y - self.type.dim_y / 2,
                                    self.type.dim_x,
                                    self.type.dim_y,
                                    stroke='black',
                                    fill=self.type.color)

    def mesh(self):
        if self.dim_z == 0:
            if self.type.shape == 'ellipse':
                if self.type.dim_x == self.type.dim_y:
                    return FullCircle(self.type.dim_x / 2,
                                      self.pos_x, self.pos_y, 0,
                                      self.type.el_size)
                else:
                    return FullEllipse(self.type.dim_x, self.type.dim_y,
                                       self.pos_x, self.pos_y, 0,
                                       self.type.el_size)
            elif self.type.shape == 'rectangle':
                    return Rectangle(self.type.dim_x, self.type.dim_y,
                                     self.pos_x, self.pos_y, 0,
                                     self.type.el_size, [None, None])
            else:
                raise Exception('Wrong inclusion shape')
        else:
            if self.type.shape == 'ellipse':
                if self.type.dim_x == self.type.dim_y:
                    return CircularCylinder(self.type.dim_x / 2,
                                            self.pos_x, self.pos_y, self.dim_z,
                                            self.type.el_size)
                else:
                    return EllipticCylinder(self.type.dim_x, self.type.dim_y,
                                            self.pos_x, self.pos_y, self.dim_z,
                                            self.type.el_size)
            elif self.type.shape == 'rectangle':
                    return Cuboid(self.type.dim_x, self.type.dim_y, self.dim_z,
                                  self.pos_x, self.pos_y, 0,
                                  self.type.el_size, [None, None, None])
            else:
                raise Exception('Wrong inclusion shape')


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

        if map is not None:
            assert len(map) == nb_y, "Wrong map size!"
            assert len(map[0]) == nb_x, "Wrong map size!"
        assert crystal_shape in ['square', 'hexa'], "Wrong crystal type!"

        self.matrix = Matrix(dim_x, dim_y, dim_z, 0, 0, 0,
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
                    Inclusion(type, x, y, dim_z)

    def image(self, filename):
        mysvg = pysvg.structure.svg("My periodic structure")
        mysvg.addElement(self.matrix.image())
        for inclusion in Inclusion.instances:
            mysvg.addElement(inclusion.image())
        mysvg.save(filename)

    def mesh_2d(self):
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

    def mesh_3d(self):
        inclusions_lines_all_top = []
        inclusions_lines_all_bottom = []
        inclusions_by_tag = {}
        inclusion_surfaces = []

        for inclusion in Inclusion.instances:
            inclusion_mesh = inclusion.mesh()
            for line in inclusion_mesh.lines_top:
                inclusions_lines_all_top.append(line)
            for line in inclusion_mesh.lines_bottom:
                inclusions_lines_all_bottom.append(line)
            if inclusion.type.type != 'hole':
                if inclusion.type.tag not in inclusions_by_tag.keys():
                    inclusions_by_tag[inclusion.type.tag] = []
                inclusions_by_tag[inclusion.type.tag].append(inclusion_mesh)
            inclusion_surfaces.extend(inclusion_mesh.surfaces)

        matrix_mesh = self.matrix.mesh()
        loop_top = LineLoop(matrix_mesh.lines_top, inclusions_lines_all_top)
        loop_bottom = LineLoop(matrix_mesh.lines_bottom, inclusions_lines_all_bottom)
        surface_top = PlaneSurface(loop_top)
        surface_bottom = PlaneSurface(loop_bottom)
        matrix_mesh.surfaces.append(surface_top)
        matrix_mesh.surfaces.append(surface_bottom)
        surface_loop = SurfaceLoop(matrix_mesh.surfaces, inclusion_surfaces)
        matrix_volume = Volume(surface_loop)
        PhysicalVolume([matrix_volume], self.matrix.tag)

        for tag, inclusions in inclusions_by_tag.iteritems():
            inclusion_volumes = []
            for inclusion in inclusions:
                inclusion_surfaces = inclusion.surfaces
                loop = LineLoop(inclusion.lines_top)
                inclusion_surfaces.append(PlaneSurface(loop))
                loop = LineLoop(inclusion.lines_bottom)
                inclusion_surfaces.append(PlaneSurface(loop))
                surface_loop = SurfaceLoop(inclusion_surfaces)
                inclusion_volumes.append(Volume(surface_loop))
            PhysicalVolume(inclusion_volumes, tag)

    def mesh(self):
        if self.dim_z == 0:
            self.mesh_2d()
        else:
            self.mesh_3d()

        result = Value.print_all() + '\n'
        result += Point.print_all() + '\n'
        result += Line.print_all() + '\n'
        result += PhysicalEntity.print_all()
        return result


class InclusionType:
    def __init__(self,
                 type,
                 shape,
                 dim_x,
                 dim_y,
                 el_size,
                 tag=None,
                 color='lightgrey'):
        """
        @param type: 'inclusion' (matter) or 'hole' (void)
        @param shape: 'ellipse' or 'rectangle'
        @param tag: what to tag in the mesh for those inclusions
        """
        self.type = type
        self.shape = shape
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.el_size = el_size
        self.tag = tag
        self.color = color
