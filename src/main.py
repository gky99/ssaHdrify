from contextlib import redirect_stderr, redirect_stdout
from os import path

from PIL import Image, ImageTk

from ui.Root import Root

if __name__ == '__main__':
    root = Root()
    icon = Image.open(path.abspath(path.join(path.dirname(__file__), 'asset/hdr.png')))
    root.wm_iconphoto(False, ImageTk.PhotoImage(icon))

    with redirect_stderr(root.textFrame.messageStream):
        with redirect_stdout(root.textFrame.messageStream):
            print("Please select input files to convert")
            root.mainloop()
