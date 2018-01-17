# -*- coding: UTF-8 -*

"""
init file for module
"""

from __version__ import *


from image_io import ImageDiskReader
import logging

logger = logging.getLogger("imageLocator")

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
file_handler = logging.FileHandler("imageLocator.log")
file_handler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

logger.debug("init module")