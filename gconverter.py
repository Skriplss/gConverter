import wx
import logging
import sys
from UI.MainFrame import MainFrame


class GCodeToRapidApp(wx.App):
    def __init__(self, redirect=False, filename=None, usebestvisual=False, clearsigint=True):
        super().__init__(redirect, filename, usebestvisual, clearsigint)
        self.frame = None

    def OnInit(self):
        self.setup_logging()
        self.frame = MainFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

    @staticmethod
    def setup_logging():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)]
        )
# end of class GCodeToRapidApp

if __name__ == "__main__":
    app = GCodeToRapidApp()
    app.MainLoop()
