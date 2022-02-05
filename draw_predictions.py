import cv2
import numpy as np
import math
import json
import pandas as pd
with open("trials.json") as f:
    parameters = json.load(f)
print(parameters.keys())

# Circle and Box coordinates
# Circle: TL = (111, 108), BL = (107, 337), TR = (,), BR = (,)
# Box: TL = (111, 108), BL = (107, 337), TR = (,), BR = (,)

frame_counter = 0

def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
       # draw circle here (etc...)
       print('x = %d, y = %d'%(x, y))

def dist(x,y):
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

def check_in_radius(x, r, head):
    #if dot_product(head, x, r) < 0:
    #    return False
    radius = r[2]
    if dist(x,r) <= radius:
        return True
    return False

# x between xmin and xmax, y between ymin and ymax
def check_in_bounds(x, r, head):

    if dot_product(head, x, r) < 0:
        return False

    radius = r[2]

    xmin = r[0] - radius
    xmax = r[0] + radius
    ymin = r[1] - radius
    ymax = r[1] + radius

    if x[0] >= xmin and x[0] <= xmax:
        if x[1] >= ymin and x[1] <= ymax:
            return True
    return False

# dot product of xy and xz (x is shared point)
def dot_product(x, y, z):
    a = (y[0] - x[0], y[1] - x[1])
    b = (z[0] - x[0], z[1] - x[1])
    return a[0] * b[0] + a[1] * b[1]

def rectangle_with_center(r, radius):
    return (r[0] - radius, r[1] - radius), (r[0] + radius, r[1] + radius)


# Load all frames into memory
keys = list(parameters.keys())



for ind in range(0,8):

    trial = parameters[keys[ind]]
    predictions = np.load("predictions/" + keys[ind] +  ".npy")
    last_frame = -1
    frame_counter = 0
    cap = cv2.VideoCapture("trimmed/" + keys[ind] + ".mp4")
    timeframes = []
    while True:
        ret, frame = cap.read()
        if ret is False:
            break

        x_1 = int(predictions[frame_counter][0][0])
        y_1 = int(predictions[frame_counter][0][1])
        # draw circles
        #frame = cv2.circle(frame, (x_1, y_1), radius=2, color=(0, 0, 255), thickness=-1)

        x_2 = int(predictions[frame_counter][1][0])
        y_2 = int(predictions[frame_counter][1][1])
        # draw circles
       # frame = cv2.circle(frame, (x_2, y_2), radius=2, color=(0, 255, 0), thickness=-1)

        #x_3 = int(predictions[frame_counter][2][0])
        #y_3 = int(predictions[frame_counter][2][1])
        # draw circles
        #frame = cv2.circle(frame, (x_3, y_3), radius=2, color=(255, 0, 0), thickness=-1)

        frame_counter += 1

        # Draw contour around objects (radi = 16, = 22 with 2 cm boundary)




        old = trial["old"]
        new = trial["new"]

        old_coords = (trial["coordinates"][old]['x'], trial["coordinates"][old]['y'], trial["coordinates"][old]['r'])
        new_coords = (trial["coordinates"][new]['x'], trial["coordinates"][new]['y'], trial["coordinates"][new]['r'])

        if trial["type"] == "circle":
            #frame = cv2.circle(frame, old_coords, radius=22, color=(255, 0, 0), thickness=1)
            #frame = cv2.circle(frame, new_coords, radius=22, color=(255, 0, 0), thickness=1)

            if check_in_radius((x_1, y_1), old_coords, (x_2, y_2)):
                if last_frame == -1:
                    timeframe = [old, frame_counter]
                    print(old + " start:", frame_counter)
                last_frame = frame_counter
            elif check_in_radius((x_1, y_1), new_coords, (x_2, y_2)):
                if last_frame == -1:
                    timeframe = [new, frame_counter]

                    print(new + " start:", frame_counter)
                last_frame = frame_counter
            else:
                if last_frame != -1:
                    timeframe.append(frame_counter)
                    timeframes.append(timeframe)
                    print(last_frame)
                    last_frame = -1

        else:
            frame = cv2.rectangle(frame, *rectangle_with_center(old_coords, 21), color=(255, 0, 0), thickness=1)
            frame = cv2.rectangle(frame, *rectangle_with_center(new_coords, 21), color=(255, 0, 0), thickness=1)

            if check_in_bounds((x_1, y_1), old_coords, 29, (x_2, y_2)):
                if last_frame == -1:
                    timeframe = [old, frame_counter]

                    print(old + " start:", frame_counter)
                last_frame = frame_counter
            elif check_in_bounds((x_1, y_1), new_coords, 29, (x_2, y_2)):
                if last_frame == -1:
                    timeframe = [new, frame_counter]

                    print(new + " start:", frame_counter)
                last_frame = frame_counter
            else:
                if last_frame != -1:
                    timeframe.append(frame_counter)
                    timeframes.append(timeframe)
                    print(last_frame)
                    last_frame = -1

        #frame = cv2.circle(frame, (318, 110), radius=22, color=(255, 0, 0), thickness=1)
        #frame = cv2.circle(frame, (318, 338), radius=22, color=(255, 0, 0), thickness=1)
        #frame = cv2.circle(frame, (116, 107), radius=22, color=(255, 0, 0), thickness=1)
        #frame = cv2.circle(frame, (112, 336), radius=22, color=(255, 0, 0), thickness=1)

        #frame = cv2.rectangle(frame, *rectangle_with_center((316,339), 21), color=(255, 0, 0), thickness=1)
        #frame = cv2.rectangle(frame, *rectangle_with_center((111,105), 21), color=(255, 0, 0), thickness=1)
        #frame = cv2.rectangle(frame, *rectangle_with_center((322,113), 21), color=(255, 0, 0), thickness=1)
        #frame = cv2.rectangle(frame, *rectangle_with_center((113,336), 21), color=(255, 0, 0), thickness=1)

        #frame = cv2.line(frame, (218, 0), (218, 448), color=(0,255,0), thickness=1)
        #frame = cv2.line(frame, (0, 224), (448, 224), color=(0,255,0), thickness=1)




        #cv2.imshow('Frame', frame)
        #cv2.setMouseCallback('Frame', onMouse)
        #k = cv2.waitKey(25) & 0xFF
       # if k == ord('q'):
        #    break

        # Write to file

    df = pd.DataFrame(timeframes, columns=['location', 'start', 'stop'])
    df.to_csv("timestamps/" + keys[ind] + ".csv")
    #5.77 px = 1 cm
    # 2 cm dist ~ 10 px

# TODO: Loosen threshold, 22 px too tight, cutting events off
# TODO: add angle threshold -> angle between head, nose and object center must be within threshold (Use dot product > 0 to test if less than perpendicular)
# TODO: Try calculating time spent in quadrant