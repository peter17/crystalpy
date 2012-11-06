# -*- coding: utf-8 -*-
"""Script for generating crystal meshes and images."""

from __future__ import division
import pysvg
from pysvg.builders import StyleBuilder
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


class PeriodicSurface(Line):
    def __init__(self, surface1, pos_lines1, neg_lines1,
                 surface2, pos_lines2, neg_lines2, permutation):
        self.surface1_id = surface1.id
        self.surface2_id = surface2.id

        lines1_list = ["%r" % line.id for line in pos_lines1]
        lines1_list.extend(["-%r" % line.id for line in neg_lines1])
        self.lines1_list = ', '.join(lines1_list)

        lines2_list = ["%r" % line.id for line in pos_lines2]
        lines2_list.extend(["-%r" % line.id for line in neg_lines2])
        if permutation > 0:
            for _ in range(permutation):
                lines2_list.append(lines2_list.pop(0))
        elif permutation < 0:
            for _ in range(-permutation):
                lines2_list.insert(0, lines2_list.pop())
        self.lines2_list = ', '.join(lines2_list)

        Line.instances.append(self)
        self.id = len(Line.instances)

    def __repr__(self):
        return ("Periodic Surface(%d) {%s} = (%s) {%s};\n"
                % (self.surface1_id, self.lines1_list,
                   self.surface2_id, self.lines2_list))


class LineLoop:
    def __init__(self, pos_lines, neg_lines=[]):
        lines_list = ["%r" % line.id for line in pos_lines]
        lines_list.extend(["-%r" % line.id for line in neg_lines])
        self.lines_list = ', '.join(lines_list)

        Line.instances.append(self)
        self.id = len(Line.instances)

    def __repr__(self):
        return ("Line Loop(%s) = {%s};\n" % (self.id, self.lines_list))


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


class PhysicalPoint:
    def __init__(self, points, name):
        self.points = ', '.join([format(point.id) for point in points])
        self.name = name

        PhysicalEntity.instances.append(self)

    def __repr__(self):
        return ('Physical Point("%s") = {%s};\n'
                % (self.name, self.points))


class PhysicalLine:
    def __init__(self, lines, name):
        self.lines = ', '.join([format(line.id) for line in lines])
        self.name = name

        PhysicalEntity.instances.append(self)

    def __repr__(self):
        return ('Physical Line("%s") = {%s};\n'
                % (self.name, self.lines))


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


class LineInSurface:
    def __init__(self, line, surface):
        self.line = line
        self.surface = surface

        PhysicalEntity.instances.append(self)

    def __repr__(self):
        return ('Line{%s} In Surface {%s};\n'
                % (self.line.id, self.surface))


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
            PhysicalLine([line_left], 'minus_x')
            PhysicalLine([line_right], 'plus_x')
        if periodicity[1]:
            PeriodicLine(line_bottom, line_top)
            PhysicalLine([line_bottom], 'minus_y')
            PhysicalLine([line_top], 'plus_y')


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
        lines_list = ["%r" % line.id for line in pos_lines]
        lines_list.extend(["-%r" % line.id for line in neg_lines])
        self.lines_list = ', '.join(lines_list)

        Line.instances.append(self)
        self.id = len(Line.instances)

    def __repr__(self):
        return ("Surface Loop(%s) = {%s};\n" % (self.id, self.lines_list))


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

        surface_left = PlaneSurface(loop1)
        surface_bottom = PlaneSurface(loop2)
        surface_right = PlaneSurface(loop3)
        surface_top = PlaneSurface(loop4)

        self.surfaces = []

        self.surfaces.append(surface_left)
        self.surfaces.append(surface_bottom)
        self.surfaces.append(surface_right)
        self.surfaces.append(surface_top)

        if periodicity[0]:
            PeriodicLine(line_left_bottom, line_right_bottom)
            PhysicalLine([line_left_bottom], 'minus_x_bottom')
            PhysicalLine([line_right_bottom], 'plus_x_bottom')
            PeriodicLine(line_left_top, line_right_top)
            PhysicalLine([line_left_top], 'minus_x_top')
            PhysicalLine([line_right_top], 'plus_x_top')
            PeriodicLine(line_bottom_left, line_bottom_right)
            PeriodicLine(line_top_left, line_top_right)
            PhysicalSurface([surface_right], 'surface_right')
            PhysicalSurface([surface_left], 'surface_left')
            PeriodicSurface(surface_right,
                            [line_top_right, line_right_top],
                            [line_bottom_right, line_right_bottom],
                            surface_left,
                            [line_left_bottom, line_top_left],
                            [line_left_top, line_bottom_left], 1)
        if periodicity[1]:
            PeriodicLine(line_bottom_bottom, line_top_bottom)
            PhysicalLine([line_bottom_bottom], 'minus_y_bottom')
            PhysicalLine([line_top_bottom], 'plus_y_bottom')
            PeriodicLine(line_bottom_top, line_top_top)
            PhysicalLine([line_bottom_top], 'minus_y_top')
            PhysicalLine([line_top_top], 'plus_y_top')
            PeriodicLine(line_bottom_left, line_top_left)
            PeriodicLine(line_bottom_right, line_top_right)
            PhysicalSurface([surface_top], 'surface_top')
            PhysicalSurface([surface_bottom], 'surface_bottom')
            PeriodicSurface(surface_top,
                            [line_top_bottom, line_top_right],
                            [line_top_top, line_top_left],
                            surface_bottom,
                            [line_bottom_right, line_bottom_top],
                            [line_bottom_left, line_bottom_bottom], -1)


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
        style_line = StyleBuilder()
        style_line.setStrokeWidth(self.dim_x / 100)
        return pysvg.shape.rect(self.pos_x - self.dim_x / 2,
                                self.pos_y - self.dim_y / 2,
                                self.dim_x,
                                self.dim_y,
                                stroke='black',
                                fill='white',
                                style=style_line.getStyle())

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
        style_line = StyleBuilder()
        style_line.setStrokeWidth(self.type.dim_x / 100)
        if self.type.shape == 'ellipse':
            return pysvg.shape.ellipse(self.pos_x,
                                       self.pos_y,
                                       self.type.dim_x / 2,
                                       self.type.dim_y / 2,
                                       stroke='black',
                                       fill=self.type.color,
                                       style=style_line.getStyle())
        elif self.type.shape == 'rectangle':
            return pysvg.shape.rect(self.pos_x - self.type.dim_x / 2,
                                    self.pos_y - self.type.dim_y / 2,
                                    self.type.dim_x,
                                    self.type.dim_y,
                                    stroke='black',
                                    fill=self.type.color,
                                    style=style_line.getStyle())

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
            if self.type.type == 'plot':
                dim_z = -self.type.dim_z
            else:
                dim_z = self.dim_z
            if self.type.shape == 'ellipse':
                if self.type.dim_x == self.type.dim_y:
                    return CircularCylinder(self.type.dim_x / 2,
                                            self.pos_x, self.pos_y, dim_z,
                                            self.type.el_size)
                else:
                    return EllipticCylinder(self.type.dim_x, self.type.dim_y,
                                            self.pos_x, self.pos_y, dim_z,
                                            self.type.el_size)
            elif self.type.shape == 'rectangle':
                    return Cuboid(self.type.dim_x, self.type.dim_y, dim_z,
                                  self.pos_x, self.pos_y, 0,
                                  self.type.el_size, [None, None, None])
            else:
                raise Exception('Wrong inclusion shape')


class Crystal:
    def __init__(self,
                 name,
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
                 inclusion_map,
                 inclusion_types,
                 physical_point_map,
                 physical_line_map):

        # Reset the instances lists
        Value.instances = {}
        Point.instances = []
        Line.instances = []
        PhysicalEntity.instances = []
        Inclusion.instances = []

        self.name = name
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.dim_z = dim_z
        el_size_bulk_value = Value('size_bulk', el_size_bulk)
        self.physical_lines = []

        if inclusion_map is not None:
            assert len(inclusion_map) == nb_y, "Wrong map size!"
            assert len(inclusion_map[0]) == nb_x, "Wrong map size!"
        assert crystal_shape in ['square', 'hexa'], "Wrong crystal type!"

        self.matrix = Matrix(dim_x, dim_y, dim_z, 0, 0, 0,
                             el_size_bulk_value, periodicity, bulk_tag)

        for type in inclusion_types:
            if type is not None:
                el_size_name = "size_%s" % len(Value.instances)
                el_size_value = Value(el_size_name, type.el_size)
                type.el_size = el_size_value

        dim_crystal_x = (nb_x - 1) * space_x
        dim_crystal_y = (nb_y - 1) * space_y
        crystal_base_x = pos_x - dim_crystal_x / 2
        crystal_base_y = pos_y - dim_crystal_y / 2

        for i in range(nb_x):
            for j in range(nb_y):
                if crystal_shape == 'hexa' and j % 2 == 1:
                    x = crystal_base_x + i * space_x + space_x / 2
                    y = crystal_base_y + j * space_y
                else:
                    x = crystal_base_x + i * space_x
                    y = crystal_base_y + j * space_y
                type_id = 0 if inclusion_map is None else inclusion_map[j][i]
                type = inclusion_types[type_id]
                if type is not None:
                    Inclusion(type, x, y, dim_z)

        for physical_point_type in physical_point_map:
            point_type = physical_point_type[0]
            point_list = physical_point_type[1]
            points = []
            for point in point_list:
                my_point = Point(point[0],
                                 point[1],
                                 point[2],
                                 el_size_bulk)
                points.append(my_point)
            PhysicalPoint(points, point_type)

        for physical_line_type in physical_line_map:
            line_type = physical_line_type[0]
            point_list = physical_line_type[1]

            assert len(point_list) % 2 == 0, 'Need an even number of points!'
            lines = []
            while point_list:
                point1 = point_list.pop()
                point2 = point_list.pop()
                pt1 = Point(point1[0],
                            point1[1],
                            point1[2],
                            el_size_bulk)
                pt2 = Point(point2[0],
                            point2[1],
                            point2[2],
                            el_size_bulk)
                my_line = StraightLine(pt1, pt2)
                lines.append(my_line)
                if point1[2] == point2[2]:
                    self.physical_lines.append((my_line, point1[2]))
            PhysicalLine(lines, line_type)

    def image(self):
        mysvg = pysvg.structure.svg(self.name)
        mysvg.addElement(self.matrix.image())
        for inclusion in Inclusion.instances:
            mysvg.addElement(inclusion.image())
        return mysvg

    def mesh_2d(self):
        inclusions_lines_all = []
        inclusions_lines_by_tag = {}

        for inclusion in Inclusion.instances:
            inclusion_mesh = inclusion.mesh()
            inclusions_lines_all.extend(inclusion_mesh.lines)
            if inclusion.type.type != 'hole':
                if inclusion.type.tag not in inclusions_lines_by_tag.keys():
                    inclusions_lines_by_tag[inclusion.type.tag] = []
                inclusions_lines_by_tag[inclusion.type.tag].append(inclusion_mesh.lines)

        loop = LineLoop(self.matrix.mesh().lines, inclusions_lines_all)
        surface = PlaneSurface(loop)
        PhysicalSurface([surface], self.matrix.tag)
        for straight_line, line_z in self.physical_lines:
            if line_z == 0:
                LineInSurface(straight_line, surface.id)

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
        inclusions_surfaces = []
        plot_surfaces_bottom = []

        for inclusion in Inclusion.instances:
            inclusion_mesh = inclusion.mesh()
            inclusion_mesh.type = inclusion.type.type
            if inclusion.type.type != 'plot':
                inclusions_lines_all_top.extend(inclusion_mesh.lines_top)
            inclusions_lines_all_bottom.extend(inclusion_mesh.lines_bottom)
            if inclusion.type.type != 'hole':
                if inclusion.type.tag not in inclusions_by_tag.keys():
                    inclusions_by_tag[inclusion.type.tag] = []
                inclusions_by_tag[inclusion.type.tag].append(inclusion_mesh)
            if inclusion.type.type != 'plot':
                inclusions_surfaces.extend(inclusion_mesh.surfaces)

        for tag, inclusions in inclusions_by_tag.iteritems():
            inclusion_volumes = []
            for inclusion in inclusions:
                inclusion_surfaces = inclusion.surfaces

                loop_top = LineLoop(inclusion.lines_top)
                loop_bottom = LineLoop(inclusion.lines_bottom)
                surface_top = PlaneSurface(loop_top)
                surface_bottom = PlaneSurface(loop_bottom)
                inclusion_surfaces.append(surface_top)
                inclusion_surfaces.append(surface_bottom)
                if inclusion.type == 'plot':
                    plot_surfaces_bottom.append(surface_bottom)

                surface_loop = SurfaceLoop(inclusion_surfaces)
                inclusion_volumes.append(Volume(surface_loop))
            PhysicalVolume(inclusion_volumes, tag)

        matrix_mesh = self.matrix.mesh()
        loop_top = LineLoop(matrix_mesh.lines_top, inclusions_lines_all_top)
        loop_bottom = LineLoop(matrix_mesh.lines_bottom, inclusions_lines_all_bottom)
        surface_top = PlaneSurface(loop_top)
        surface_bottom = PlaneSurface(loop_bottom)
        for straight_line, line_z in self.physical_lines:
            if line_z == 0:
                LineInSurface(straight_line, surface_bottom.id)
            if line_z == self.dim_z:
                LineInSurface(straight_line, surface_top.id)
        matrix_mesh.surfaces.append(surface_top)
        matrix_mesh.surfaces.append(surface_bottom)
        matrix_mesh.surfaces.extend(plot_surfaces_bottom)
        surface_loop = SurfaceLoop(matrix_mesh.surfaces, inclusions_surfaces)
        matrix_volume = Volume(surface_loop)
        PhysicalVolume([matrix_volume], self.matrix.tag)

    def mesh(self):
        if self.dim_z == 0:
            self.mesh_2d()
        else:
            self.mesh_3d()

        result = "//%s, created with crystalpy\n" % self.name
        result += Value.print_all() + '\n'
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
                 dim_z,
                 el_size,
                 tag=None,
                 color='lightgrey'):
        """
        @param type:
            'inclusion' (matter inside the matrix)
            'hole' (void inside the matrix)
            'plot' (matter, outside the matrix)
        @param shape: 'ellipse' or 'rectangle'
        @param tag: what to tag in the mesh for those inclusions
        """

        self.type = type
        self.shape = shape
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.dim_z = dim_z
        self.el_size = el_size
        self.tag = tag
        self.color = color
