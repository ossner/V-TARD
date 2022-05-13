import numpy as np
import cv2 as cv


class Camera(object):
    def __init__(self):
        self.map2 = None
        self.map1 = None
        self.attempts = 0
        self.cap = cv.VideoCapture(0)
        if not self.cap.isOpened():
            raise "Camera could not be opened, make sure one is connected"
        ret = False
        frame = None

        while not ret:
            self.attempts += 1
            ret, frame = self.cap.read()
            if self.attempts > 10:
                raise TimeoutError("Camera is not responding after multiple attempts... Shutting down")

        (w, h) = (frame.shape[1], frame.shape[0])

        dist_coeff = np.zeros((4, 1), np.float64)
        dist_coeff[0, 0] = 0.00025
        dist_coeff[1, 0] = 0
        dist_coeff[2, 0] = 0
        dist_coeff[3, 0] = 0

        cam_matrix = np.eye(3, dtype=np.float32)
        cam_matrix[0, 2] = w / 2.0  # define center x
        cam_matrix[1, 2] = h / 2.0  # define center y
        cam_matrix[0, 0] = 10.  # define focal length x
        cam_matrix[1, 1] = 10.  # define focal length y

        self.map1, self.map2 = cv.initUndistortRectifyMap(cam_matrix, dist_coeff, None, None, (w, h), cv.CV_32FC1)

    def get_frame(self):
        ret, frame = self.cap.read()
        cv_barrel = cv.remap(frame, self.map1, self.map2, cv.INTER_LINEAR)
        cv_barrel = np.hstack((cv_barrel, cv_barrel))
        (flag, encodedImage) = cv.imencode(".jpg", cv_barrel)
        return bytearray(encodedImage)
