import cv2
import numpy as np
import math
import json
import pandas as pd

predictions = np.load("../predictions/m1te1a4.npy")
frame_counter = 0
cap = cv2.VideoCapture("trimmed/m1te1a4.mp4")
timeframes = []
while True:
    ret, frame = cap.read()
    if ret is False:
         break

    x_1 = int(predictions[frame_counter][0][0])
    y_1 = int(predictions[frame_counter][0][1])
        # draw circles
    frame = cv2.circle(frame, (x_1, y_1), radius=2, color=(0, 0, 255), thickness=-1)

    x_2 = int(predictions[frame_counter][1][0])
    y_2 = int(predictions[frame_counter][1][1])
        # draw circles
    frame = cv2.circle(frame, (x_2, y_2), radius=2, color=(0, 255, 0), thickness=-1)

    x_3 = int(predictions[frame_counter][2][0])
    y_3 = int(predictions[frame_counter][2][1])
        # draw circles
    frame = cv2.circle(frame, (x_3, y_3), radius=2, color=(255, 0, 0), thickness=-1)

    frame_counter += 1
    cv2.imshow('Frame', frame)
        #cv2.setMouseCallback('Frame', onMouse)
    k = cv2.waitKey(25) & 0xFF
    if k == ord('q'):
        break

        # Write to file

    #5.77 px = 1 cm
    # 2 cm dist ~ 10 px

# TODO: Loosen threshold, 22 px too tight, cutting events off
# TODO: add angle threshold -> angle between head, nose and object center must be within threshold (Use dot product > 0 to test if less than perpendicular)
# TODO: Try calculating time spent in quadrant