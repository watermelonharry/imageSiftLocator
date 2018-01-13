# -*- coding: UTF-8 -*

"""
input and output functions for module
"""
import unittest
import os

from imageSiftLocator.io import ImageDiskReader
from imageSiftLocator.models import ImageLocator

cwd = os.getcwd()


class ImageLocatorTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_median_from_correct_list(self):
        x_list= [1,11,2,22,3,33,4,44,5,55,6,66]
        y_list= [21,56,87,99,3,5,14,79,3,102,23,39]

        correct_list = zip(x_list,y_list)
        result = ImageLocator.get_median_coordinates(correct_list)
        self.assertEqual(result, (11,39))

    def test_get_median_from_empty_list(self):
        try:
            err = ImageLocator.get_median_coordinates([])
        except Exception as e:
            self.assertTrue(isinstance(e, AttributeError))

        try:
            err = ImageLocator.get_median_coordinates([(1,1),(2,2)])
        except Exception as e:
            self.assertTrue(isinstance(e, AttributeError))

    def test_calculate_location(self):
        sample_path = r'D:\Code\imageSiftLocator\test\x1-90.jpg'
        train_path = r'D:\Code\imageSiftLocator\test\x2.jpg'
        sample_reader = ImageDiskReader(im_path=sample_path)
        train_reader = ImageDiskReader(im_path=train_path)

        img_locator = ImageLocator(sample=sample_reader, train=train_reader)
        result = img_locator.find_location()
        print(result)

        img_locator.show_cmp_img_with_tag()
        img_locator.show_sample_img_with_tag()
        img_locator.show_train_img_with_tag()
        img_locator.show_center_with_tag()