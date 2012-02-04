# -*- coding: utf-8 -*-
from unittest import TestCase
from generator import Crystal

class GeneratorTestCase(TestCase):
    def mesh_equal_string(self, description, result):
        my_crystal = Crystal(**description)
        mesh = my_crystal.mesh()
        print mesh
        self.assertEquals(mesh, result)

    def image_equal_string(self, description, result):
        my_crystal = Crystal(**description)
        self.assertEquals(my_crystal.image().getXML(), result)
