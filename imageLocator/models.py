# -*- coding: UTF-8 -*

"""
models for module
"""
import sys

if sys.version_info < (2, 7):
	# cv2 = __import__("lib.py26.cv2")
	from lib.py26 import cv2
else:
	from lib.py27 import cv2
import scipy as sp
import logging
from image_io import ImageReaderBaseClass, DataWriterBaseClass


class ImageLocatorBaseClass(object):
	"""
	Abstract class for ImageLocator
	"""

	def __init__(self):
		raise NotImplementedError

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


class TemplateLocator(ImageLocatorBaseClass):
	"""
	locate sample_img's position in train_img by cv2.templete_match
	"""

	def __init__(self, sample=ImageReaderBaseClass(), src=ImageReaderBaseClass(), save_list=[]):
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

		self.sample_

		self.sample_img_with_tag = None
		self.train_img_with_tag = None
		self.cmp_img = None
		self.img_center_location = None

		self.result = None
		self.index = None

	def save(self):
		"""
		save result to
		:return:
		"""
		self.logger.debug("save data")
		if self.result:
			for writer in self.save_list:
				writer.save(self.result)

	def _pre_process(self):
		"""
		preprocess the images
		:return:None
		"""
		self.logger.debug("pre-processing images")

	# graylize the src image

	def _calculate(self):
		"""
		calculating images
		:return:None
		"""
		self.logger.debug("calculating images")

	def _output(self):
		"""
		return calculating results
		:return:None
		"""

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

	def show_sample_img_with_tag(self):
		cv2.imshow("sample img", self.sample_img_with_tag)
		cv2.waitKey()

	def show_train_img_with_tag(self):
		cv2.imshow("train img", self.train_img_with_tag)
		cv2.waitKey()

	def show_cmp_img_with_tag(self):
		cv2.imshow("img compare", self.cmp_img)
		cv2.waitKey()

	def show_center_with_tag(self):
		height, width = self.img_center_location
		y = int(height)
		x = int(width)

		base_pic = sp.zeros((960, 1280, 3), sp.uint8)
		base_pic[:, :, 0] = self.train_reader.get_image()
		base_pic[:, :, 1] = base_pic[:, :, 0]
		base_pic[:, :, 2] = base_pic[:, :, 0]

		cv2.line(base_pic, (x - 10, y), (x + 10, y), (0, 255, 0))
		cv2.line(base_pic, (x, y - 10), (x, y + 10), (0, 255, 0))
		cv2.imshow("center", base_pic)
		cv2.waitKey()
