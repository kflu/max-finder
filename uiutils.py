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
logging.basicConfig(level=logging.DEBUG)

def init(widget_class):
    def geo(self, method, *args, **kw):
        getattr(self, method)(*args, **kw)
        return self
    widget_class.geo = geo

def UI(cls, name, *args, **kw):
    logging.debug("calling UI for: %s ===="%name)
    tmp = cls()
    tmp.ui_meta = {
            'type':'UI',
            'name':name,
            }

    args = list(args)
    print args
    for arg in enumerate(args[:]):
        tp = getattr(arg, 'ui_meta', {}).get('type','')
        if tp.lower() == 'ui':
            setattr(tmp, arg.ui_meta['name'], arg)
            arg.master = tmp

    logging.debug('before restructuring: ' + str(list(args)))
    args = (arg for arg in args if not hasattr(arg, 'ui_meta'))
    logging.debug('after restructuring: ' + str(list(args)))

    tmp.config(*args, **kw)
    return tmp

if __name__ == '__main__':
    from Tkinter import *
    init(Widget)
    main = UI(Frame, "main", 
                UI(Button, "b1", text='b1').geo('pack'),
                UI(Button, "b2", text='b2').geo('pack'),
                )
    #main.master is a Tk instance.
    main.master.title("main window")
