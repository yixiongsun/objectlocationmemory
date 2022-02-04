import cv2

cap = cv2.VideoCapture("raw/m3t1a4.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
print(fps)
print(frame_count)
fourcc = cv2.VideoWriter_fourcc(*"mpv4")
output = cv2.VideoWriter("trimmed/m3t1a4.mp4", fourcc, fps, (448, 448))

print(output.get(cv2.CAP_PROP_FPS))
frame_number = 0
start = 94
cap.set(cv2.CAP_PROP_POS_MSEC, start * 1000)
# 20 minutes = 20 * 60 * 1000 ms seconds
duration = 20

while True:

    ret, frame = cap.read()

    #if ret is False:
    #    break

    if cap.get(cv2.CAP_PROP_POS_MSEC) > (start +  duration * 60) * 1000:
        break


    crop = frame[16:464, 96:584]
    crop = cv2.resize(crop, (448, 448))

    #cv2.imshow('Frame', crop)

    #k = cv2.waitKey(25) & 0xFF
    #if k == ord('q'):
    #    print(frame_number)
    output.write(crop)
    frame_number += 1
    #print(frame_number)
    #break

