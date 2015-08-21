import wx
import sys
import time
from threading import Thread
from pbrecentpull import Photopull

blue_grey_100 = '#CFD8DC'

class pull_thread(Thread):
        def __init__(self):
            Thread.__init__(self)
            self.setDaemon(True)
            self.photopull = Photopull()

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
        panel = wx.Panel(self)
        self.SetBackgroundColour(blue_grey_100)
        self._child_thread_init = child_thread
        self.child_thread = self._child_thread_init()
        self.child_thread.setDaemon(True)

        self.buttons = {
            'Start': { 'function': self.btn_start_click },
            'Stop': { 'function': self.btn_stop_click },
            'Exit': { 'function': self.onClose }
        }

        x, y = (8, 8)
        for button_name in self.buttons.keys():
            y += 30
            self.buttons[button_name]['bnt'] = wx.Button(panel, label=button_name, pos=(x, y), size=(175, 28))
            self.buttons[button_name]['bnt'].Bind(wx.EVT_BUTTON, self.buttons[button_name]['function'])
            self.buttons[button_name]['bnt'].SetWindowStyleFlag(wx.NO_BORDER)
        self.Show(True)


    def btn_start_click(self,event):
        if not self.child_thread.isAlive():
            self.SetTitle("Running")
            self.child_thread.start()

    def btn_stop_click(self,event):
        if self.child_thread.isAlive():
            self.SetTitle("Standby")
            self.child_thread.terminate()
            self.child_thread.join()
            self.child_thread = self._child_thread_init()

    def onClose(self, event):
        self.Close()

if __name__ == '__main__':

    pbpull = pull_thread
    app = wx.App()
    frame = MyFrame(pbpull)
    frame.Show()
    app.MainLoop()
