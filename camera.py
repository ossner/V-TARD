from wand.image import Image
import numpy as np
import cv2 as cv


def barrel_dist(img):
    img.virtual_pixel = 'transparent'
    img.distort('barrel', (0.2, 0.0, 0.0, 1.0))
    return np.array(img)


def barrel_dist_cv(src):
    width  = src.shape[1]
    height = src.shape[0]
    distCoeff = np.zeros((4, 1), np.float64)

    # TODO: add your coefficients here!
    k1 = 0.0005  # negative to remove barrel distortion
    k2 = 0.0
    p1 = 0.0
    p2 = 0

    distCoeff[0, 0] = k1
    distCoeff[1, 0] = k2
    distCoeff[2, 0] = p1
    distCoeff[3, 0] = p2

    # assume unit matrix for camera
    cam = np.eye(3, dtype=np.float32)

    cam[0, 2] = width / 2.0  # define center x
    cam[1, 2] = height / 2.0  # define center y
    cam[0, 0] = 10.  # define focal length x
    cam[1, 1] = 10.  # define focal length y

    # here the undistortion will be computed
    return cv.undistort(src, cam, distCoeff)


class Camera(object):
    def __init__(self):
        self.cap = cv.VideoCapture(0)

    def get_frame(self):
        ret, frame = self.cap.read()
        # barrel = barrel_dist(Image.from_array(frame))
        cv_barrel = barrel_dist_cv(frame)
        cv_barrel = np.hstack((cv_barrel, cv_barrel))
        (flag, encodedImage) = cv.imencode(".png", cv_barrel)
        return bytearray(encodedImage)
