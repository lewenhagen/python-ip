#!/usr/bin/env python3

import cv2

class VideoCamera(object):
    def __init__(self, url):
        self.url = url
        self.video = cv2.VideoCapture(self.url)
        self.frames = []
        self.delay = 15
        self.counter = 0
        self.fps = 15
        self.timer = self.delay * self.fps

    def __del__(self):
        self.video.release()

    def release_cam(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        # self.frames.append(jpeg.tobytes())
        if not ret:
            return
        return jpeg.tobytes()
        # if self.delay == 0:
        #     return self.frames.pop(0)
        # else:
        #     self.counter+=1
        #
        #     if self.counter < self.timer:
        #         return cv2.imread('static/img/hour.png',0).tobytes()
        #     elif self.counter >= self.timer:
        #         print("inside")
        #         print(len(self.frames))
        #         print(self.timer)
        #         return self.frames.pop(0)
