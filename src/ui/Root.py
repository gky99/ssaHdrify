import platform
import tkinter
from tkinter import Tk
from tkinter.ttk import Style

from ui.MessageFrame import MessageFrame
from ui.OptionFrame import OptionFrame


def setStyle():
    sys_name = platform.system()
    tk_style = Style()
    if sys_name == 'Windows':
        tk_style.theme_use('vista')
    return


class Root(Tk):
    def __init__(self):
        super().__init__()
        self.title("Convert subtitle from SDR to HDR colorspace")
        setStyle()
        self.wm_minsize(640, 480)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Option frame
        options_frame = OptionFrame(master=self, text="Options")
        options_frame.grid(row=0, sticky="new", padx=5, pady=5)

        # Message frame
        self.textFrame = MessageFrame(master=self, text="Message", borderwidth=1)
        self.textFrame.grid(row=1, sticky=tkinter.NSEW, padx=5, pady=5)
