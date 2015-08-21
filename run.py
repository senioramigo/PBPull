import wx
import sys
import time
import socket
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
        self.panel = wx.Panel(self)
        self.SetBackgroundColour(blue_grey_100)
        self._child_thread_init = child_thread
        self.child_thread = self._child_thread_init(self.thread_comm, self.is_running)
        self.create_widgest()
        self.started = False
        self.url = "http://google.com"


    def create_widgest(self):
        # Create the buttons
        self.buttons = {
            'Start': { 'function': self.btn_start_click },
            'Stop': { 'function': self.btn_stop_click },
            'Open URL': {'function': self.launch_browser},
            'Exit': { 'function': self.onClose }}
        x, y = (8, 8)
        for button_name in self.buttons.keys():
            y += 32
            self.buttons[button_name]['bnt'] = wx.Button(self.panel, label=button_name, pos=(x, y), size=(100, 30))
            self.buttons[button_name]['bnt'].Bind(wx.EVT_BUTTON, self.buttons[button_name]['function'])
            self.buttons[button_name]['bnt'].SetWindowStyleFlag(wx.NO_BORDER)


        img = wx.EmptyImage(240, 240)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.BitmapFromImage(img), pos=(108, 8))

    def launch_browser(self, event):
        webbrowser.open(self.url, 2)


    def is_running(self):
        return self.started

    def thread_comm(self, filepath, url="http://google.com"):
        self.url = url
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

        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.panel.Refresh()

    def btn_start_click(self,event):
        if not self.child_thread.isAlive():
            self.SetTitle("Running")
            self.started = True
            self.child_thread.start()

    def btn_stop_click(self,event):
        if self.child_thread.isAlive():
            self.started = False
            self.SetTitle("Standby")
            self.child_thread.terminate()
            self.child_thread.join()
            self.child_thread = self._child_thread_init(self.thread_comm, self.is_running)

    def onClose(self, event):
        self.Close()

if __name__ == '__main__':

    pbpull = pull_thread
    app = wx.App()
    frame = MyFrame(pbpull)
    frame.Show()
    app.MainLoop()
