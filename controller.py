from gui import Main, ui
from Tkinter import *
from ttk import *
import tkFileDialog

import logging;logging.basicConfig()

def on_click_tar_button():
    dirname = tkFileDialog.askdirectory()
    main.targetDirEntry.delete(0,END)
    main.targetDirEntry.insert(0, dirname)

tk = Tk()
main = Main.build_all(tk)
main.targetDirButton['command'] = on_click_tar_button

main.update()
main.mainloop()
