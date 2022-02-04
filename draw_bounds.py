import cv2
import numpy as np
import math
import json



def rectangle_with_center(r, radius):
    return (r[0] - radius, r[1] - radius), (r[0] + radius, r[1] + radius)


cap = cv2.VideoCapture("trimmed/m3t1a4.mp4")
timeframes = []
ret, frame = cap.read()
while True:





        # Draw contour around objects (radi = 16, = 22 with 2 cm boundary)
    # TL
    #frame = cv2.circle(frame, (101, 109), radius=46, color=(255, 0, 0), thickness=1)

    # TR
    frame = cv2.circle(frame, (314, 110), radius=45, color=(255, 0, 0), thickness=1)

    # BR
    frame = cv2.circle(frame, (306, 344), radius=43, color=(255, 0, 0), thickness=1)

    #BL
    #frame = cv2.circle(frame, (94, 341), radius=43, color=(255, 0, 0), thickness=1)


    # TL
    #frame = cv2.rectangle(frame, *rectangle_with_center((103,109), 43), color=(255, 0, 0), thickness=1)

    # TR
    #frame = cv2.rectangle(frame, *rectangle_with_center((321,115), 21), color=(255, 0, 0), thickness=1)

    # BR
    #frame = cv2.rectangle(frame, *rectangle_with_center((300, 345), 43), color=(255, 0, 0), thickness=1)

    # BL
    #frame = cv2.rectangle(frame, *rectangle_with_center((111,339), 21), color=(255, 0, 0), thickness=1)

    #frame = cv2.line(frame, (218, 0), (218, 448), color=(0,255,0), thickness=1)
    #frame = cv2.line(frame, (0, 224), (448, 224), color=(0,255,0), thickness=1)




    cv2.imshow('Frame', frame)
    k = cv2.waitKey(25) & 0xFF
    if k == ord('q'):
        break

        # Write to file

    #df = pd.DataFrame(timeframes, columns=['location', 'start', 'stop'])
    #df.to_csv("timestamps/" + keys[ind] + ".csv")
    #5.77 px = 1 cm
    # 2 cm dist ~ 10 px

# TODO: Loosen threshold, 22 px too tight, cutting events off
# TODO: add angle threshold -> angle between head, nose and object center must be within threshold (Use dot product > 0 to test if less than perpendicular)
# TODO: Try calculating time spent in quadrant