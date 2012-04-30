from unittest.case import TestCase

__author__ = 'janos'


import sys
import os
import unittest
import StringIO

sys.path.append(os.path.join(os.path.pardir,"src"))
import ObjGraphicFile as objg

class testCubeGeneration(unittest.TestCase):
    def setUp(self):
        pass

    def test_cube_initialization(self):
        cube_obj = objg.Cube(0,0,0,1)
        self.assertEqual(6,len(cube_obj.faces))
        self.assertEqual(8,len(cube_obj.vertices))

class testObjGraphicFileWriter(unittest.TestCase):
    def setUp(self):
        self.f = StringIO.StringIO()

    def test_basic_obj_file_no_mtls(self):

        cube_obj = objg.Cube(0,0,0,1)

        ogfw = objg.ObjGraphicFileWriter([cube_obj])
        ogfw.generate_file(self.f)

