'''UI utils

Using this module to declaratively develop tkinter user interface.  Before
using this module, please call init(Tkinter.Widget) to initialize. 


Example:

    from Tkinter import *
    init(Widget)
    main = UI(Frame, "main", 
                UI(Button, "b1", text='b1').geo('pack'),
                UI(Button, "b2", text='b2').geo('pack'),
                )
    #main.master is a Tk instance.
    main.master.title("main window")

'''

import logging
logging.basicConfig()
logger = logging.getLogger("FastUI")
logger.setLevel(logging.DEBUG)

def make_ui():
    class UI:
        __aliases = {}
        def __init__(self, cls, alias=None, *args, **kwargs):
            logger.debug("Creating %s:%s:%s" % (cls, args, kwargs))
            self.__cls = cls
            self.__alias = alias
            self.__args = args
            self.__kwargs = kwargs
            self.__children = []
            self.__named_children = {}

            # call those methods on creation. Each element is a tuple:
            #   (callable, args, kwargs)
            # Upon invoking, it's like:
            #   callable( widget, *args, **kwargs )
            self.__on_creation = []

        def call_on_creation(self, method, *args, **kwargs):
            logger.debug("Adding callback: %s:%s:%s" % (method, args, kwargs))
            self.__on_creation.append(
                    (method, args, kwargs) )
            return self

        def pack(self, *args, **kwargs):
            self.call_on_creation(self.__cls.pack, *args, **kwargs)
            return self
        def grid(self, *args, **kwargs):
            self.call_on_creation(self.__cls.grid, *args, **kwargs)
            return self

        def has(self, *args, **kwargs):
            self.__children = args
            self.__named_children = kwargs
            return self

        def create(self, master=None):
            # create my self
            tmp = self.__cls(master, *self.__args, **self.__kwargs)
            if self.__alias:
                UI.__aliases[self.__alias] = tmp

            # call on creation:
            for (func, args, kwargs) in self.__on_creation:
                logger.debug("invoking %s:%s:%s" % (func, args, kwargs))
                func(tmp, *args, **kwargs)

            # create children
            for child in self.__children:
                child.create(tmp)

            for k in self.__named_children:
                o = self.__named_children[k].create(tmp)
                setattr(tmp, k, o)

            for k in UI.__aliases:
                setattr(tmp, k, UI.__aliases[k])

            return tmp
    return UI

if __name__ == '__main__':
    from Tkinter import *

    ui = make_ui()

    tk = Tk()

    tree = ui(Frame, border=10, relief='sunken').pack().has(
                ui(Button, 'b1', text='hi').pack(),
                ui(Frame, 'f1', border=20, relief='sunken').pack().has(
                    ui(Button, text='hello world!').pack()))

    gui = tree.create(tk)
    gui.update()

    import time;time.sleep(5)
    gui.b1['text']='changed!'

    tk.mainloop()
