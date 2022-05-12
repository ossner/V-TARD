from wand.image import Image
import numpy as np
import cv2 as cv


class Camera(object):
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        ret = False
        frame = None

        while not ret:
            ret, frame = self.cap.read()
        
        (w,h)=(frame.shape[1],frame.shape[0])
        
        distCoeff = np.zeros((4, 1), np.float64)
        distCoeff[0, 0] = 0.00025
        distCoeff[1, 0] = 0
        distCoeff[2, 0] = 0
        distCoeff[3, 0] = 0

        cam=cam = np.eye(3, dtype=np.float32)
        cam[0, 2] = w / 2.0  # define center x
        cam[1, 2] = h / 2.0  # define center y
        cam[0, 0] = 10.  # define focal length x
        cam[1, 1] = 10.  # define focal length y
        
        self.map1, self.map2 = cv.initUndistortRectifyMap(cam, distCoeff, None, None, (w, h), cv.CV_32FC1)




    def get_frame(self):
        ret, frame = self.cap.read()
        cv_barrel = cv.remap(frame, self.map1, self.map2, cv.INTER_LINEAR)
        cv_barrel = np.hstack((cv_barrel, cv_barrel))
        (flag, encodedImage) = cv.imencode(".png", cv_barrel)
        return bytearray(encodedImage)
