from wand.image import Image
import numpy as np
import cv2 as cv


def barrel_dist(img):
    img.virtual_pixel = 'transparent'
    img.distort('barrel', (0.2, 0.0, 0.0, 1.0))
    return np.array(img)


class Camera(object):
    def __init__(self):
        self.cap = cv.VideoCapture(0)

    def get_frame(self):
        ret, frame = self.cap.read()
        cv_barrel = barrel_dist(Image.from_array(frame))
        cv_barrel = np.hstack((cv_barrel, cv_barrel))
        (flag, encodedImage) = cv.imencode(".png", cv_barrel)
        return bytearray(encodedImage)
