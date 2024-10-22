from tkinter.ttk import LabelFrame

from ui.options.BrightnessOption import BrightnessOption
from ui.options.EotfOption import EotfOption
from ui.options.FileSelectionButton import FileSelectionButton


class OptionFrame(LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # EOTF option
        eotf_frame = EotfOption(master=self)
        eotf_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Target brightness option
        brightness_frame = BrightnessOption(master=self)
        brightness_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Select file button
        select_file_button = FileSelectionButton(master=self)
        select_file_button.grid(row=1, column=0, columnspan=2, pady=5)
