# -*- coding: UTF-8 -*

"""
models for module
"""

from models import TemplateLocator
from image_io import *
from __constants__ import *

import logging

logger = logging.getLogger("imageLocator")


def get_template_locator(src_path=None, sample_path=None):
    logger.debug("init template_locator")

    src_reader = get_reader(path=src_path)
    sample_reader = get_reader(path=sample_path)
    return TemplateLocator(sample=sample_reader, src=src_reader)


def get_reader(type=READER_DISK, **kwargs):
    logger.debug("init image reader, type {0}, params {1}".format(type, kwargs))
    if type == READER_DISK:
        return ImageDiskReader(im_path=kwargs.get("path"))
    elif type == READER_DB:
        raise NotImplementedError
    elif type == READER_HTTP:
        raise NotImplementedError