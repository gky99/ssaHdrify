import io
import tkinter
from tkinter.ttk import LabelFrame


class MessageFrame(LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.messageStream = io.StringIO()
        self.messagePointer = 0
        self.callbackId = ""
        self.text = tkinter.Text(master=self)
        self.text.pack(expand=True, fill='both')

        self.updateText()

    def updateText(self):
        self.messageStream.seek(self.messagePointer, io.SEEK_SET)

        self.text.config(state=tkinter.NORMAL)
        self.text.insert(tkinter.END, self.messageStream.read())
        self.text.config(state=tkinter.DISABLED)

        self.messagePointer = self.messageStream.tell()
        self.callbackId = self.after(500, self.updateText)
