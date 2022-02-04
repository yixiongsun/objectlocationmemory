import cv2


# This class loads the video into memory
class Video():

    def __init__(self, filepath):
        cap = cv2.VideoCapture(filepath)

        # Get num frames
        self.frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        # Get fps
        self.fps = cap.get(cv2.CAP_PROP_FPS)

        self.frames = []

        while True:
            ret, frame = cap.read()

            if frame is None:
                break

            self.frames.append(frame)


    # Get timestamp in milliseconds
    def timestamp(self, frame):
        return 1000.0 * frame / self.fps;

    # Format ms into string
    def format_time(self, time):
         ms = int(time % 1000)
         s = int(time / 1000) % 60
         m = int(time / 60000)

         return str.format("{:02d}:{:02d}:{:03d}", m,s,ms)