#!/usr/bin/env python3
# import numpy as np
import cv2 as cv
from cam import Cam

def get_full_urls(item, resolution):
    return item + "/axis-cgi/mjpg/video.cgi?resolution={}&compression=25&camera=1".format(resolution)



def create_list_of_cam_objects(thelist, resolution):
    result = []
    thelist2 = [item[1] for item in thelist]
    for index, item in enumerate(thelist2):
        # cam = item + "/axis-cgi/mjpg/video.cgi?resolution=1280x720&compression=25&camera=1"
        # cam = Cam(item, get_full_urls(item), 1, 1)

        cam = Cam(item, get_full_urls(item, resolution), (index+1), 1)
        result.append(cam)

    # cam = thelist[1] + "/videostream.cgi"
    # cam = Cam(thelist[1], cam, 2, 1)

    # result.append(cam)

    return result


# def initiate_stream(cam):
#     delay = 0
#     instances = 1
#     FPS = 15
#     counter = 0
#
#     delay_image = cv.imread('img/hour.png',0)
#     cap = cv.VideoCapture(cam.fulladress)
#     if not cap.isOpened():
#         print("Cannot open camera")
#         exit()
#
#     cap.set(cv.CAP_PROP_FPS, FPS)
#
#     return cap
