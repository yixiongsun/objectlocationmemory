import cv2
import numpy as np
import math
import json
import pandas as pd


with open("../trials.json") as f:
    parameters = json.load(f)
print(parameters.keys())

# Count durations in quadrants
def quadrant(x):
    if x[0] < 218 and x[1] < 224:
        return "TL"
    elif x[0] >= 218 and x[1] < 224:
        return "TR"
    elif x[0] < 218 and x[1] >= 224:
        return "BL"
    return "BR"


# Format ms into string
def format_time(time):
    ms = int(time % 1000)

    s = int(time / 1000) % 60
    m = int(time / 60000)

    return str.format("{:02d}:{:02d}:{:03d}", m,s,ms)



# Load all frames into memory
keys = list(parameters.keys())



for ind in range(0,32):

    trial = parameters[keys[ind]]
    #if keys[ind] == "0IRO":
        #continue
    predictions = np.load("predictions/" + keys[ind] +  ".npy")
    last_frame = -1
    frame_counter = 0
    cap = cv2.VideoCapture("dataset/" + keys[ind] + ".mp4")
    fps = cap.get(cv2.CAP_PROP_FPS)
    timeframes = []
    def timestamp(frame):
        return 1000.0 * frame / fps;

    last_q = ""

    for i in range(0, len(predictions)):

        x_1 = int(predictions[i][0][0])
        y_1 = int(predictions[i][0][1])
        # draw circles
        #frame = cv2.circle(frame, (x_1, y_1), radius=2, color=(0, 0, 255), thickness=-1)



        q = quadrant((x_1, y_1))

        if last_q == "":
            timeframe = [q, format_time(timestamp(i))]
            last_q = q
        elif last_q != q:
            timeframe.append(format_time(timestamp(i)))
            timeframes.append(timeframe)
            timeframe = [q, format_time(timestamp(i))]
            last_q = q



        #frame = cv2.line(frame, (218, 0), (218, 448), color=(0,255,0), thickness=1)
        #frame = cv2.line(frame, (0, 224), (448, 224), color=(0,255,0), thickness=1)




        #cv2.imshow('Frame', frame)
        #cv2.setMouseCallback('Frame', onMouse)
        #k = cv2.waitKey(25) & 0xFF
        #if k == ord('q'):
        #    break

        # Write to file
    timeframe.append(format_time(timestamp(i)))
    timeframes.append(timeframe)
    #print(timeframes)

    df = pd.DataFrame(timeframes, columns=['location', 'start', 'stop'])
    df.to_csv("quadrants/" + keys[ind] + ".csv")
    #5.77 px = 1 cm
    # 2 cm dist ~ 10 px