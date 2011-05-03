from Tkinter import *
from ttk import *
from uiutils import make_ui
import logging
logger = logging.getLogger("UI")

ui = make_ui()

SearchPane = ui(Frame).has(
                ui(Entry, 'searchEntry').pack(side=LEFT),
                ui(Button, 'searchButton', text='Search').pack())

OptionsPane = ui(Frame).has(
                ui(Checkbutton, 'ignCsCkBtn', text="Ignore case").pack(anchor=W),
                ui(Checkbutton, 'mtchWhlWdCkBtn', text="Match whole word").pack(anchor=W))

TargetPane = ui(Frame).has(
                ui(Entry, 'targetDirEntry').pack(),
                ui(Button, 'targetDirButton', text='Choose directory').pack())

ControlPane = ui(Frame).has(
                TargetPane.pack(side=LEFT, anchor=NW),
                ui(Frame).pack().has(
                    SearchPane.pack(),
                    OptionsPane.pack()))

ResultPane = ui(Frame).has(
                ui(Listbox).pack(expand=1, fill=BOTH))

Main = ui(Frame).pack(fill=BOTH, expand=1).has(
            ControlPane.pack(),
            ResultPane.pack(expand=1, fill=BOTH))


if __name__ == '__main__':
    logging.basicConfig()
    tk = Tk()
    main = Main.build_all(tk)
    tk.mainloop()
