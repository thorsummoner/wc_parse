#!/usr/bin/env python

import window
import os

class RunmapWindow(window.Window):
    """
        Gui application interface.
    """

    GLADE_FILE = os.path.splitext(__file__)[0] + '.glade'
    WINDOW_NORMAL = 'window_normal'
    WINDOW_EXPERT = 'window_expert'

    ROOT_WINDOW = WINDOW_NORMAL

    def __init__(self):
        super(RunmapWindow, self).__init__()


    class Handler(window.Window.BaseHandler):
        """
            Main Window Event Handler
        """

        def on_normal(self, widget):
            self.parent.window.hide()
            self.parent.change_window(self.parent.WINDOW_NORMAL)

        def on_expert(self, widget):
            self.parent.window.hide()
            self.parent.change_window(self.parent.WINDOW_EXPERT)


if __name__ == '__main__':
    exit(RunmapWindow().main())
