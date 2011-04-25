from Tkinter import *
from ttk import *
from Tkinter import Checkbutton
import tkFileDialog
#from ttk import *

class Dashboard(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.entry_search_pattern = Entry(self)
        self.entry_search_pattern.bind('<FocusIn>', lambda e: self.entry_search_pattern.selection_range(0, END))

        self.button_do_search = Button(self, text='Search')

        self.checkbutton_ignore_case = Checkbutton(self, text='Ignore case')
        self.checkbutton_ignore_case.deselect()

        # show
        self.entry_search_pattern.pack()
        self.checkbutton_ignore_case.pack()
        self.button_do_search.pack()

class TargetDirPane(LabelFrame):
    def __init__(self, parent):
        LabelFrame.__init__(self, parent, text='Target Directories')

        self.button_browse = Button(self, text='Choose...', command=self.__askdir)

        self.__chosen_dir = StringVar()
        self.__chosen_dir.set("")
        self.entry_target = Entry(self, textvariable = self.__chosen_dir)

        # Show
        self.button_browse.pack()
        self.entry_target.pack()

    def __askdir(self):
        self.__chosen_dir.set(tkFileDialog.askdirectory())

class ResultPane(LabelFrame):
    def __init__(self, parent):
        LabelFrame.__init__(self, parent, text = 'Results')

        # widgets
        self.listbox = Listbox(self, height=10)

        # show
        self.listbox.pack()

class Preview(Frame):
    pass


if __name__ == '__main__':
    root = Tk()
    root.title('Max search')

    dash = Dashboard(root)
    dirpane = TargetDirPane(root)
    listbox = ResultPane(root)

    dirpane.pack(side=LEFT)
    dash.pack(side=LEFT)
    listbox.pack()

    root.mainloop()
