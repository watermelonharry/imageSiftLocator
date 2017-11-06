# -*- coding: UTF-8 -*

"""
input and output functions for module
"""
import hashlib
import cv2


class ImageDiskReader(object):
    """
    image openner: open image file, calculate its size, and hash code
    """

    def __init__(self, im_path=None):
        """
        open image by path
        :param im_path:
        :return:
        """
        self.image_path = im_path
        self.image = cv2.imread(im_path, 0)
        self.hash = None
        if self.image is None:
            raise AttributeError("invalid file path")
        self.height, self.width = self.image.shape
        self.size = self.image.size

    def get_size(self):
        """
        get the size of image
        :return: tuple(height,width)
        """
        if self.image is not None:
            return (self.height, self.width)
        else:
            raise AttributeError("invalid file path")

    def get_hash(self):
        if self.image is None:
            raise AttributeError("invalid file path")
        if not self.hash:
            im_file = open(self.image_path).read()
            self.hash = hashlib.md5(im_file).hexdigest()
        return self.hash

    def get_image(self):
        if self.image is None:
            raise AttributeError("invalid file path")

        return self.image


class DBHashIO(object):
    """
    db io class to search image's hash code in database
    """