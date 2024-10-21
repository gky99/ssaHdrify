from contextlib import redirect_stderr, redirect_stdout

from ui.Root import Root

if __name__ == '__main__':
    root = Root()

    with redirect_stderr(root.textFrame.messageStream):
        with redirect_stdout(root.textFrame.messageStream):
            print("Please select input files to convert")
            root.mainloop()
