#!/usr/bin/env python3

import numpy as np
import cv2 as cv

cam1= "http://192.168.1.132/axis-cgi/mjpg/video.cgi?resolution=1280x720&compression=25&camera=1"
delay = 0
instances = 1
frames = []
FPS = 15
counter = 0
delay_message = "Hur mycket delay ska det vara: (sek) "
amount_message = "Hur många instanser? (1-4)"
delay_image = cv.imread('img/hour.png',0)

while True:
    delay = input(delay_message)
    try:
        delay = int(delay)
    except:
        delay = input(delay_message)

    instances = input(amount_message)
    try:
        instances = int(instances)
        break
    except:
        pass


cap = cv.VideoCapture(cam1)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    cap.set(cv.CAP_PROP_FPS, FPS)
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv.namedWindow('frame', cv.WINDOW_NORMAL)
    cv.setWindowProperty('frame', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    # Our operations on the frame come here
    # gray = cv.cvtColor(frame, cv.COLORRGB)
    # Display the resulting frame
    frames.append(frame)

    if instances == 2:
        image = frames[0]
        numpy_horizontal_concat = np.concatenate((image, image), axis=1)
        if counter >= (FPS*delay):
            cv.imshow('frame', numpy_horizontal_concat)
            frames.pop(0)
        else:
            cv.imshow('frame', image)
    else:
        if counter >= (FPS*delay):
            cv.imshow('frame', frames.pop(0))
        else:
            cv.imshow('frame', delay_image)
        counter += 1

    if cv.waitKey(30) == ord('q'):
        break
    if cv.waitKey(30) == ord('w'):
        delay = int(input(message))

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
