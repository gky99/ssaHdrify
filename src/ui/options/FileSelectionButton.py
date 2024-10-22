from tkinter import filedialog
from tkinter.ttk import Button

from hdrify import ssaProcessor


def files_picker() -> None:
    """询问用户并返回字幕文件"""
    files = filedialog.askopenfilenames(filetypes=[('ASS files', '.ass .ssa'),
                                                   ('all files', '.*')])
    for f in files:
        print(f"Converting file: {f}")
        ssaProcessor(f)
    return


class FileSelectionButton(Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Select file and convert", **kwargs)
        self.configure(command=files_picker)

