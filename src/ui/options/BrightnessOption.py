import re
import tkinter
from tkinter.ttk import Frame, Label, Entry

from conversion_setting import config


def validateBrightness(newBrightness):
    valid = re.match('^[0-9]*$', newBrightness) is not None
    if valid:
        if len(newBrightness) == 0:
            config.targetBrightness = 0
        else:
            config.targetBrightness = min(int(newBrightness), 10000)
        return True
    else:
        return False


class BrightnessOption(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(1, weight=1)

        target_brightness_label = Label(master=self, text="Target subtitle brightness (nits):")
        target_brightness_label.grid(row=0, column=0, sticky=tkinter.W)

        self.target_brightness_var = tkinter.StringVar()
        self.target_brightness_var.set(config.targetBrightness)
        validate_brightness_wrapper = (master.register(validateBrightness), '%P')
        target_brightness_input = Entry(master=self, textvariable=self.target_brightness_var, validate="key",
                                        validatecommand=validate_brightness_wrapper)

        target_brightness_input.grid(row=0, column=1, sticky=tkinter.EW)
