import wx
import cv2
import pandas as pd


class VideoPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.ind = -1

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.list_ctrl = wx.ListCtrl(self, size=(-1, 500),
                                     style=wx.LC_REPORT | wx.BORDER_SUNKEN)

        self.list_ctrl.InsertColumn(0, 'Location', width=100)
        self.list_ctrl.InsertColumn(1, 'Start', width=100)
        self.list_ctrl.InsertColumn(2, 'Stop', width=100)
        main_sizer.Add(self.list_ctrl, 0, 0, 5)
        self.SetSizer(main_sizer)

        self.list_ctrl.Bind(wx.EVT_KEY_UP, self.handle_key_up)
        self.list_ctrl.Bind(wx.EVT_KEY_DOWN, self.handle_key_down)


        self.current_time_text = wx.StaticText(self, -1, label="00:00:000", pos = (520, 480))
        self.start_time_text = wx.StaticText(self, -1, label="00:00:000", pos = (450, 480))
        self.end_time_text = wx.StaticText(self, -1, label="00:00:000", pos=(590, 480))
        self.current_frame_text = wx.StaticText(self, -1, label="0", pos=(520, 500))
        self.start_frame_text = wx.StaticText(self, -1, label="0", pos=(450, 500))
        self.end_frame_text = wx.StaticText(self, -1, label="0", pos=(590, 500))
        self.trim_end_button = wx.Button(self, -1, label="Trim end", pos=(400, 520))
        self.trim_start_button = wx.Button(self, -1, label="Trim start", pos=(300, 520))
        self.delete_button = wx.Button(self, -1, label="Delete", pos=(500, 520))
        self.DI_text = wx.StaticText(self, -1, label="DI:", pos=(600, 520))

        self.play_video = False
        self.reverse = False
        self.key_down = False
        self.render = False
        self.Bind(wx.EVT_KEY_UP, self.handle_key_down)
        self.Bind(wx.EVT_KEY_DOWN, self.handle_key_down)

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.handle_select_timestamp, self.list_ctrl)

        self.trim_start_button.Bind(wx.EVT_BUTTON, self.trim_start)
        self.trim_end_button.Bind(wx.EVT_BUTTON, self.trim_end)

        self.delete_button.Bind(wx.EVT_BUTTON, self.delete_timestamp)


    def trim_start(self, event):
        if self.ind == -1:
            return

        self.data[self.ind]["start"] = self.current_frame

        self.update(self.data, self.ind)
        self.Refresh()

    def trim_end(self, event):
        if self.ind == -1:
            return

        self.data[self.ind]["stop"] = self.current_frame

        self.update(self.data, self.ind)
        self.Refresh()

    def delete_timestamp(self, event):
        if self.ind == -1:
            return
        self.pause()
        self.reverse = False

        del self.data[self.ind]

        self.ind -= 1
        self.update(self.data, self.ind)
        self.Refresh()


    def save_timestamps(self, filepath):

        # Convert data to timestamps
        save_data = []

        for timestamp in self.data:
            new_timestamp = timestamp
            new_timestamp["start"] = self.video.format_time(self.video.timestamp(int(timestamp["start"])))
            new_timestamp["stop"] = self.video.format_time(self.video.timestamp(int(timestamp["stop"])))

            save_data.append(new_timestamp)

        df = pd.DataFrame(save_data)
        print(df)
        df.to_csv(filepath)


    def update(self, data, ind=-1):
        self.data = data
        self.list_ctrl.ClearAll()
        self.list_ctrl.InsertColumn(0, 'Location', width=100)
        self.list_ctrl.InsertColumn(1, 'Start', width=100)
        self.list_ctrl.InsertColumn(2, 'Stop', width=100)

        index = 0
        for timestamp in data:
            self.list_ctrl.InsertItem(index, timestamp["location"])
            self.list_ctrl.SetItem(index, 1, str(timestamp["start"]))
            self.list_ctrl.SetItem(index, 2, str(timestamp["stop"]))
            index += 1

        # After loading timestamp, select first data
        if ind != -1:
            self.ind = ind
            self.list_ctrl.Select(ind)
        else:
            self.ind = 0
            self.list_ctrl.Select(0)

        # If we have a video, select timeframe
        if hasattr(self, "video"):
            self.render = True
            self.set_timeframe(data[self.ind]["start"], data[self.ind]["stop"])

    def set_timeframe(self, start_frame, end_frame):
        self.start_frame = int(start_frame)
        self.end_frame = int(end_frame)
        self.current_frame = int(start_frame)

        self.render_text()

    def calculate_DI(self):
        new = 0
        old = 0
        for timestamp in self.data:
            if timestamp['location'][1] == "L":
                new += self.video.timestamp(int(timestamp["stop"])) - self.video.timestamp(int(timestamp["start"]))
            else:
                old += self.video.timestamp(int(timestamp["stop"])) - self.video.timestamp(int(timestamp["start"]))
        return new / (new + old)


    def render_text(self):
        self.start_frame_text.SetLabel(str(self.start_frame))
        self.current_frame_text.SetLabel(str(self.current_frame))
        self.end_frame_text.SetLabel(str(self.end_frame))
        self.start_time_text.SetLabel(self.video.format_time(self.video.timestamp(self.start_frame)))
        self.current_time_text.SetLabel(self.video.format_time(self.video.timestamp(self.current_frame)))
        self.end_time_text.SetLabel(self.video.format_time(self.video.timestamp(self.end_frame)))

        self.DI_text.SetLabel("{0:.2f}".format(self.calculate_DI()))



    # on loading video, check if file is loaded
    def load_video(self, video):
        self.play_video = False
        self.reverse = False
        self.render = False
        self.video = video


        if hasattr(self, 'timer'):
            self.timer.Stop()

        print("loaded video")
        if hasattr(self, "data"):
            print("has data")
            # After loading timestamp, select first data
            self.list_ctrl.Select(self.ind)

            # If we have a video, select timeframe
            self.set_timeframe(self.data[self.ind]["start"], self.data[self.ind]["stop"])
            self.render = True
        else:
            self.start_frame = 0
            self.end_frame = 0

            self.current_frame = 0


        f = cv2.cvtColor(video.frames[self.current_frame], cv2.COLOR_BGR2RGB)

        self.bmp = wx.Bitmap.FromBuffer(448, 448, f)
        self.Refresh()

        self.timer = wx.Timer(self)
        self.timer.Start(1000. / video.fps)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)


    def play(self):
        self.play_video = True

    def pause(self):
        self.play_video = False

    def handle_key_down(self, event):
        if not hasattr(self, "video"):
            return

        keycode = event.GetKeyCode()

        if self.key_down:
            return

        if keycode == 46:
            self.key_down = True
            self.play()
        elif keycode == 44:

            self.key_down = True
            self.play()
            self.reverse = True


    def handle_key_up(self, event):
        if not hasattr(self, "video"):
            return
        keycode = event.GetKeyCode()

        if keycode == wx.WXK_SPACE:
            if self.key_down:
                return
            if self.play_video:
                self.pause()
            else:
                self.play()
        elif keycode == 46:
            self.key_down = False
            self.pause()
        elif keycode == 44:
            self.key_down = False

            self.pause()
            self.reverse = False

    def handle_select_timestamp(self, event):
        ind = event.Index
        self.ind = ind
        # If we have a video, select timeframe
        if hasattr(self, "video"):
            self.play_video = False
            self.reverse = False
            self.set_timeframe(self.data[ind]["start"], self.data[ind]["stop"])
            self.render = True
            f = cv2.cvtColor(self.video.frames[self.current_frame], cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(f)
            self.Refresh()




    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        if self.render:
            dc.DrawBitmap(self.bmp, 330, 0)

    def NextFrame(self, event):

        if self.play_video is False:
            return

        if self.reverse:
            if self.current_frame > self.start_frame:
                self.current_frame -= 1
            else:
                self.current_frame = self.end_frame - 1
        else:
            if self.current_frame < self.end_frame - 1:
                self.current_frame += 1
            else:
                self.current_frame = self.start_frame

        f = cv2.cvtColor(self.video.frames[self.current_frame], cv2.COLOR_BGR2RGB)
        self.bmp.CopyFromBuffer(f)
        self.Refresh()

        # Render timestamp + frame number on screen
        self.render_text()
