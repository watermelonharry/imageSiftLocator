# -*- coding: UTF-8 -*

"""
models for module
"""
import sys

if sys.version_info < (2, 7):
    from lib.py26 import cv2
else:
    from lib.py27 import cv2
import scipy as sp
import logging
from image_io import *

import numpy as np
import hashlib
import copy


class ImageLocatorBaseClass(object):
    """
    Abstract class for ImageLocator
    """
    def _pre_process(self):
        raise NotImplementedError("pre-process the images")

    def _calculate(self):
        raise NotImplementedError("calculate the images")

    def _output(self):
        raise NotImplementedError("return the calculation result")

    def process(self):
        """
        process images adn store result in self.result
        """
        self._pre_process()
        self._calculate()
        return self._output()

    def get_result(self):
        """
        get the calculation result
        """
        raise NotImplementedError

    def save(self):
        """
        save data to file/db/mem by calling writer.write()
        """
        raise NotImplementedError

    def get_search_index(self):
        """
        get search_index of two imgs
        """
        raise NotImplementedError


class TemplateLocator(ImageLocatorBaseClass):
    """
    locate sample_img's position in train_img by cv2.templete_match
    """

    def __init__(self, sample=None, src=None, save_list=[]):
        """
        init class
        :param sample: instance(ImageReader), eg. ImageDiskReader(file)
        :param src: instance(ImageReader), eg. ImageDiskReader(file)
        :return: None
        """
        self.logger = logging.getLogger("imageLocator.TemplateLocator")
        self.sample_reader = sample
        self.src_reader = src
        self.save_list = save_list
        self._check_params()

        self.sample_img = None
        self.src_img = None

        self.sample_img_with_tag = None
        self.train_img_with_tag = None
        self.cmp_img = None
        self.img_center_location = None

        self.result = None
        self.search_index = None
        self._calculate_search_index()

    def save(self):
        """
        save result to
        :return:
        """
        self.logger.debug("save data")
        if self.result:
            for writer in self.save_list:
                writer.save(self.result)

    def add_writer(self, writer_instance=None):
        """
        add an writer to self.save_list
        :param writer_instance: instance of DataWriterBaseClass
        :return:
        """
        self.logger.debug("add writer {0}".format(writer_instance))
        if isinstance(writer_instance, DataWriterBaseClass):
            self.save_list.append(writer_instance)
        else:
            raise AttributeError("writer must be DataWriterBaseClass instance")

    def remove_writer(self):
        # todo: 检索列表比较writer的id, 删除id对应的writer
        raise NotImplementedError

    def _calculate_search_index(self):
        """
        calculate index by the hash code of src_img and sample_image
        :return:index_hash
        """
        self.logger.debug("calculating hash")
        src_hash = self.src_reader.get_hash()
        sample_hash = self.sample_reader.get_hash()
        search_index = hashlib.md5(src_hash+sample_hash).hexdigest()
        self.search_index = search_index

        self.logger.debug("index is {0}".format(search_index))
        return search_index

    def _pre_process(self):
        """
        preprocess the images
        :return:None
        """
        self.logger.debug("pre-processing images")
        # graylize the src img
        self.src_img = self.src_reader.get_gray_image()
        self.sample_img = self.sample_reader.get_gray_image()

    # graylize the src image

    def _calculate(self, threshold=0.9):
        """
        calculating images
        :return:None
        """
        self.logger.debug("calculating images")
        try:
            res = cv2.matchTemplate(self.src_img, self.sample_img, cv2.TM_CCOEFF_NORMED)
            w, h = self.sample_img.shape[::-1]
            loc = np.where(res >= threshold)
            points = zip(*loc[::-1])
            points.sort(key=lambda x:int(x[1]))
            self.result = map(lambda x:(x[1],x[0]), points)
        except Exception as e:
            self.result = []
            self.logger.error("calculating:{0}".format(e))
            raise e

    def _output(self):
        """
        return calculating results
        :return:None
        """
        self.logger.debug("getting result")
        if self.result:
            return self.result
        else:
            self.logger.error("no result stored, calculate first")

    def _check_params(self):
        self.logger.debug("check params")
        try:
            if isinstance(self.sample_reader, ImageReaderBaseClass) and isinstance(self.src_reader,
                                                                                   ImageReaderBaseClass):
                pass
            else:
                raise AttributeError("invalid input: sample and src image should be ImageReader instance")

            if isinstance(self.save_list, list):
                for writer in self.save_list:
                    if not isinstance(writer, DataWriterBaseClass):
                        raise AttributeError("writer should be DataWriterClass instance")
            else:
                raise AttributeError("save_list should be list instance")
        except Exception as e:
            self.logger.error("check param fail: {0}".format(e))
            raise e

    def get_search_index(self):
        """
        get search_index of two images
        :return:search_index
        """
        self.logger.debug("get search index")
        if self.search_index:
            return self.search_index
        else:
            self._calculate_search_index()

    def get_result(self):
        """
        return the calculation result
        :return(list):self.result
        """
        self.logger.debug("getting result")
        if self.result:
            return copy.deepcopy(self.result)
        else:
            self.logger.debug("no result yet, calling process()")
            self.process()
            return copy.deepcopy(self.result)

    @classmethod
    def get_median_coordinates(cls, point_list=[]):
        """
        find the median coordinates of the given point list
        :param point_list: list(points), eg. [(1.0,1.0), (2.0,2.0), (3.0,3.0)]
        :return: median coordinate, eg. (2.0,2.0) /None/exception
        """
        if not isinstance(point_list, list) or len(point_list) < 3:
            raise AttributeError("invalid input: need point list with more than 3 points.")

        try:
            x_list = sorted(point_list, key=lambda x: x[0])
            x_coordinate = x_list[len(x_list) / 2][0]

            y_list = sorted(point_list, key=lambda x: x[1])
            y_coordinate = y_list[len(y_list) / 2][1]

            return (x_coordinate, y_coordinate)
        except Exception as e:
            raise e


    def show_center_with_tag(self):
        sample_h, sample_w = self.sample_reader.get_size()
        sample_h = sample_h/2
        sample_w = sample_w/2
        src_height, src_width = self.src_reader.get_size()

        base_pic = sp.zeros((src_height, src_width, 3), sp.uint8)
        base_pic[:, :, 0] = self.src_reader.get_gray_image()
        base_pic[:, :, 1] = base_pic[:, :, 0]
        base_pic[:, :, 2] = base_pic[:, :, 0]

        for points in self.get_result():
            y,x = points
            y,x = y+sample_h, x+sample_w
            cv2.line(base_pic, (x - 10, y), (x + 10, y), (0, 255, 0),2)
            cv2.line(base_pic, (x, y - 10), (x, y + 10), (0, 255, 0),2)
        cv2.imshow("center", base_pic)
        cv2.waitKey()
