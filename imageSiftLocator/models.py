# -*- coding: UTF-8 -*

"""
models for module
"""
import cv2
import scipy as sp

sift = cv2.SIFT()


class ImageLocator(object):
    """
    locate sample_img's position in train_img
    """

    def __init__(self, sample=None, train=None):
        """
        init class
        :param sample_img: instance(ImageReader), eg. ImageDiskReader(file)
        :param train_img: instance(ImageReader), eg. ImageDiskReader(file)
        :return: None
        """
        if sample and train:
            self.sample_reader = sample
            self.train_reader = train
        else:
            raise AttributeError("invalid input: sample and train image should be ImageReader instance")

        self.sample_img_with_tag = None
        self.train_img_with_tag = None
        self.cmp_img = None

        self.img_center_location = None


    def find_location(self):
        if self.img_center_location:
            return self.img_center_location

        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(self.sample_reader.get_image(), None)
        kp2, des2 = sift.detectAndCompute(self.train_reader.get_image(), None)

        # show key point
        kp1_img = cv2.drawKeypoints(self.sample_reader.get_image(), kp1)
        self.sample_img_with_tag = kp1_img
        # cv2.imshow("kp1_img",kp1_img)
        kp2_img = cv2.drawKeypoints(self.train_reader.get_image(), kp2)
        self.train_img_with_tag = kp2_img
        # cv2.imshow("kp2_img",kp2_img)

        # FLANN parameters
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)  # or pass empty dictionary
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)
        print 'matches...', len(matches)
        # Apply ratio test
        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append(m)
        print 'good', len(good)
        # #####################################
        # visualization

        h1, w1 = self.sample_reader.get_image().shape[:2]
        h2, w2 = self.train_reader.get_image().shape[:2]

        view = sp.zeros((max(h1, h2), w1 + w2, 3), sp.uint8)
        view[:h1, :w1, 0] = self.sample_reader.get_image()
        view[:h2, w1:, 0] = self.train_reader.get_image()
        view[:, :, 1] = view[:, :, 0]
        view[:, :, 2] = view[:, :, 0]

        dst_point_list = []
        for m in good:
            # draw the keypoints
            # print m.queryIdx, m.trainIdx, m.distance
            color = tuple([sp.random.randint(0, 255) for _ in xrange(3)])
            # print 'kp1,kp2',kp1,kp2
            cv2.line(view, (int(kp1[m.queryIdx].pt[0]), int(kp1[m.queryIdx].pt[1])),
                     (int(kp2[m.trainIdx].pt[0] + w1), int(kp2[m.trainIdx].pt[1])), color)
            dst_point = (kp2[m.trainIdx].pt[0], kp2[m.trainIdx].pt[1])
            dst_point_list.append(dst_point)

        # store cmp_img in class
        self.cmp_img = view
        self.img_center_location = self.get_median_coordinates(dst_point_list)
        return self.img_center_location


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
        height,width  = self.img_center_location
        y = int(height)
        x = int(width)

        base_pic = sp.zeros((960,1280, 3), sp.uint8)
        base_pic[:,:,0] = self.train_reader.get_image()
        base_pic[:, :, 1] = base_pic[:, :, 0]
        base_pic[:, :, 2] = base_pic[:, :, 0]

        cv2.line(base_pic, (x-10,y),(x+10,y),(0,255,0))
        cv2.line(base_pic, (x,y-10),(x,y+10),(0,255,0))
        cv2.imshow("center", base_pic)
        cv2.waitKey()