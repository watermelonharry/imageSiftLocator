# -*- coding: UTF-8 -*

"""
input and output functions for module
"""
import unittest
import os

from imageLocator.image_io import ImageDiskReader
from imageLocator.models import TemplateLocator

cwd = os.getcwd()


class TemplateLocatorTest(unittest.TestCase):
    def setUp(self):
        self.src_reader = ImageDiskReader(im_path="test_imgs/a.jpg")
        self.sample_reader = ImageDiskReader(im_path="test_imgs/ax.jpg")

    def tearDown(self):
        pass

    def test_template_init(self):
        tem = TemplateLocator(sample=self.sample_reader, src=self.src_reader)
        assert tem.get_search_index() is not None

    def test_template_error_init(self):
        try:
            tem = TemplateLocator(sample=self.sample_reader, src=[])
            raise AssertionError("templateLocator can init with error input")
        except AttributeError as e:
            pass

    def test_process(self):
        tem = TemplateLocator(sample=self.sample_reader, src=self.src_reader)
        # tem.process()
        assert tem.get_result() is not None
        assert len(tem.get_result()) == 14
        print(tem.get_result())
        """
        result should be like
        [(972, 134), (972, 165), (972, 196), (972, 227),
        (972, 258), (972, 289), (972, 320), (972, 351),
        (972, 382), (972, 413), (972, 444), (133, 526),
        (1022, 632), (1022, 666)]
        """

    def test_show_center(self):
        tem = TemplateLocator(sample=self.sample_reader, src=self.src_reader)
        tem.show_center_with_tag()