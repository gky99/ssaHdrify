import tkinter
from tkinter import StringVar
from tkinter.ttk import Frame, Label, Combobox

EOTF_options = ["PQ", "HLG"]

class EotfOption(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(1, weight=1)

        self.EOTF_var = StringVar()
        self.EOTF_label = Label(master=self, text="Content EOTF curve:")
        self.EOTF_label.grid(row=0, column=0, sticky=tkinter.W)
        self.EOTF_dropdown = Combobox(self, state='readonly', values=EOTF_options)
        self.EOTF_dropdown.config(state='disabled')
        self.EOTF_dropdown.current(0)
        self.EOTF_dropdown.grid(row=0, column=1, sticky=tkinter.EW)