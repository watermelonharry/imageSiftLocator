# -*- coding: UTF-8 -*

"""
input and output functions for module
"""
import unittest
import os

from imageLocator.image_io import ImageDiskReader

cwd = os.getcwd()


class ImageDiskReaderTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_open_valid_from_disk(self):
        path = cwd + '\\x1.jpg'
        ta = ImageDiskReader(im_path=path)
        self.assertEqual(ta.get_size(), (24, 55))
        hashstr = ta.get_hash()
        self.assertEqual(ta.get_hash(), hashstr)

    def test_open_invalid_from_disk(self):
        path = cwd + '\\x1.jppp'
        try:
            ta = ImageDiskReader(im_path=path)
            raise AttributeError
        except Exception as e:
            print("{0}".format(e))

