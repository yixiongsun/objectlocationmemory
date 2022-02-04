import wx
import pandas as pd
from objectlocationmemory import panels, video


class MyFrame(wx.Frame):
    def __init__(self, size=(800, 600)):
        super().__init__(parent=None, title='Hello World', size=size)

        # variables
        self.timestamps = []

        # Keep track of what key was pressed
        self.last_key = -1
        self.key_down = False
        self.play = False




        self.video_panel = panels.VideoPanel(self)
        #self.video_panel.load_video(v)

        # Timer to poll
        self.create_menu()
        self.Show()



    def create_menu(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        open_timestamp_menu_item = file_menu.Append(
            wx.ID_ANY, 'Open File',
            'Open file time stamp'
        )

        open_video_menu_item = file_menu.Append(
            wx.ID_ANY, 'Open Video',
            'Open video file'
        )

        save_timestamp_menu_item = file_menu.Append(
            wx.ID_ANY, 'Save',
            'Save timestamp file'
        )

        menu_bar.Append(file_menu, '&File')
        self.Bind(
            event=wx.EVT_MENU,
            handler=self.on_open_file,
            source=open_timestamp_menu_item,
        )
        self.Bind(
            event=wx.EVT_MENU,
            handler=self.on_open_video,
            source=open_video_menu_item,
        )

        self.Bind(
            event=wx.EVT_MENU,
            handler=self.save_data,
            source=save_timestamp_menu_item,
        )

        self.SetMenuBar(menu_bar)


    def load_data(self, df):

        self.timestamps = []

        # Load row data timestamps
        for idx, row in df.iterrows():
            self.timestamps.append({"location": row["location"], "start": row["start"], "stop": row["stop"]})

        # Update UI
        self.video_panel.update(self.timestamps)

    def save_data(self, event):
        fdlg = wx.FileDialog(self, "Cleaned filepath", "", "", "CSV files(*.csv)|*.*", wx.FD_SAVE)

        if fdlg.ShowModal() == wx.ID_OK:
            save_path = fdlg.GetPath() + ".csv"

        self.video_panel.save_timestamps(save_path)



    def on_open_file(self, event):
        # otherwise ask the user what new file to open
        with wx.FileDialog(self, "Open csv file", wildcard="csv files (*.csv)|*.csv",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r') as file:
                    df = pd.read_csv(pathname)
                    self.load_data(df)

            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)

    def on_open_video(self, event):
        # otherwise ask the user what new file to open
        with wx.FileDialog(self, "Open mp4 file", wildcard="mp4 files (*.mp4)|*.mp4",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()

            v = video.Video(pathname)
            self.video_panel.load_video(v)


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()