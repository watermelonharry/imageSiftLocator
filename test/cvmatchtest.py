# -*- coding: utf-8 -*-
from imageLocator.lib import cv2
import numpy as np


def mathc_img(image, Target, value):
    img_rgb = cv2.imread(image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(Target, 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = value
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (7, 249, 151), 2)
    cv2.imshow('Detected-ori', img_rgb)
    cv2.imshow('ori-temp', template)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    template = cv2.resize(template, (0, 0), fx=0.9, fy=0.9, interpolation=cv2.INTER_AREA)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = value
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (7, 249, 151), 2)
    cv2.imshow('Detected-0.9', img_gray)
    cv2.imshow('0.9-temp', template)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


image = ("a.jpg")
Target = ('ax.jpg')
value = 0.9
mathc_img(image, Target, value)
