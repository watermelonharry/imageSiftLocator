# -*- coding: UTF-8 -*

"""
input and output functions for module
"""
import sys

if sys.version_info < (2, 7):
    # cv2 = __import__("lib.py26.cv2")
    from lib.py26 import cv2
else:
    from lib.py27 import cv2

import hashlib
import logging
import os
import copy
import json
import random


class ImageReaderBaseClass(object):
    def __init__(self):
        raise NotImplementedError()

    def get_size(self):
        raise NotImplementedError

    def get_hash(self):
        raise NotImplementedError

    def get_image(self):
        raise NotImplementedError


class ImageDiskReader(ImageReaderBaseClass):
    """
    image openner: open image file, calculate its size, and hash code
    """

    def __init__(self, im_path=None):
        """
        open image by path
        :param im_path:
        :return:
        """
        self.logger = logging.getLogger("imageLocator.ImageDiskReader")
        self.image_path = im_path

        self.logger.debug("reading file {0}".format(self.image_path))
        self._check_file_exisit()

        self.image = None
        self.image = cv2.imread(im_path)
        self.gray_image = cv2.imread(im_path, 0)
        self._check_image_read()

        self.hash = None
        self.get_hash()
        self.height, self.width = self.gray_image.shape
        self.size = self.gray_image.size

    def __str__(self):
        return u"Image reader@ {0}".format(self.image_path)

    def _check_file_exisit(self):
        if os.path.exists(self.image_path):
            self.logger.debug("file exisits")
            return True
        else:
            self.logger.debug("file not exisits: {0}".format(self.image_path))
            raise IOError("file not exisit: {0}".format(self.image_path))

    def _check_image_read(self):
        if self.image is not None:
            return True
        raise IOError("image read fail.")

    def get_gray_image(self):
        """
        get the grey image of self.image
        :return:self.grey_image
        """
        self.logger.debug("getting gray image")
        if self.gray_image is not None:
            self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        return copy.deepcopy(self.gray_image)

    def get_size(self):
        """
        get the size of image
        :return: tuple(height,width)
        """
        self.logger.debug("get image width and height")
        if self.height and self.width:
            return (self.height, self.width)

    def get_hash(self):
        self.logger.debug("calculating image hash")
        if not self.hash:
            im_file = open(self.image_path).read()
            self.hash = hashlib.md5(im_file).hexdigest()
        return self.hash

    def get_image(self):
        self.logger.debug("getting image")
        image = copy.deepcopy(self.image)
        return image


class DBHashIO(object):
    """
    db io class to search image's hash code in database
    """
    pass

class MemIo(object):
    """
    store data in memory
    """
    pass


class DataWriterBaseClass(object):
    def __init__(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def write(self, data):
        raise NotImplementedError


class DataFileWriter(DataWriterBaseClass):
    def __init__(self, file_path = None):
        self.logger = logging.getLogger("imageLocator.DataFileWriter")
        self.file_path = file_path
        self.id = None
