import wx
import sys
import time
import os
import socket
from PIL import Image
import webbrowser
from threading import Thread
from pbrecentpull import Photopull

blue_grey_100 = '#CFD8DC'


class pull_thread(Thread):

    def __init__(self, thread_comm, parent_running):
        Thread.__init__(self)
        self.setDaemon(True)
        self.photopull = Photopull(thread_comm, parent_running)

    def run(self):
        self.photopull.run()

    def terminate(self):
        self.photopull.stop()


class MyFrame(wx.Frame):

    """make a frame, inherits wx.Frame"""

    def __init__(self, child_thread):
    # create a frame, no parent, default to wxID_ANY
    # wx.Frame.__init__(self, None, wx.ID_ANY, 'wxButton', pos=(300, 150), size=(320, 250))
        wx.Frame.__init__(self, None, title="Close Me")
        self.Center()
        self.panel = wx.Panel(self)
        self.SetBackgroundColour(blue_grey_100)
        self._child_thread_init = child_thread
        self.child_thread = self._child_thread_init(
            self.thread_comm, self.is_running)
        self.create_widgest()
        self.CreateMenuBar()
        self.started = False
        self.url = "http://google.com"



    def CreateMenuBar(self):
        "Create a menu bar with Open, Exit items"
        menuBar = wx.MenuBar()
        # Tell our Frame about this MenuBar
        self.SetMenuBar(menuBar)
        menuOptions = wx.Menu()
        menuBar.Append(menuOptions, '&Options')

        startButton = menuOptions.Append(-1, '&Start', 'Start pulling images')
        self.Bind(wx.EVT_MENU, self.btn_start_click, startButton)
        stopButton = menuOptions.Append(-1, 'Sto&p', 'Stop pulling images')
        self.Bind(wx.EVT_MENU, self.btn_stop_click, stopButton)

        # create a menu item for Exit and bind it to the OnExit function
        exitMenuItem = menuOptions.Append(-1, 'E&xit', 'Exit the viewer')
        self.Bind(wx.EVT_MENU, self.onClose, exitMenuItem)


    def create_widgest(self):
        # Create the buttons
        url_button = wx.Button(
                self.panel, label="Open_URL", pos=(0, 0), size=(100, 30))
        url_button.Bind(wx.EVT_BUTTON, self.launch_browser)
        img = wx.EmptyImage(240, 240)
        self.image_object = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.BitmapFromImage(img), pos=(108, 8))

    def launch_browser(self, event):
        webbrowser.open(self.url, 2)

    def is_running(self):
        return self.started

    def thread_comm(self, filepath, url="http://google.com"):
        if os.path.splitext(filepath)[1].lower() !='.png':
            window_width, window_height = self.panel.GetSize()
            max_width = window_height - 110
            max_height = window_height - 20
            img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
            # scale the image, preserving the aspect ratio
            W = img.GetWidth()
            H = img.GetHeight()

            if W > H:
                NewW = max_width
                NewH = max_width * H / W
            else:
                NewH = max_height
                NewW = max_height * W / H

            img = img.Scale(NewW,NewH)

            self.image_object.SetBitmap(wx.BitmapFromImage(img))
            self.panel.Refresh()
        else:
            print "PNG - Unable to display at this time"


    def btn_start_click(self, event):
        if not self.child_thread.isAlive():
            self.SetTitle("Running")
            self.started = True
            self.child_thread.start()

    def btn_stop_click(self, event):
        if self.child_thread.isAlive():
            self.started = False
            self.SetTitle("Standby")
            self.child_thread.terminate()
            self.child_thread.join()
            self.child_thread = self._child_thread_init(
                self.thread_comm, self.is_running)

    def onClose(self, event):
        self.Close()

if __name__ == '__main__':

    pbpull = pull_thread
    app = wx.App()
    frame = MyFrame(pbpull)
    frame.Show()
    app.MainLoop()
