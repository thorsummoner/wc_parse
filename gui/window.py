#!/usr/bin/env python

"""
    Main Window Class
"""

import os
import signal

from gi.repository import Gtk

class Window(Gtk.Window):
    """
        Gui application interface.
    """
    # pylint: disable=no-member

    ROOT_WINDOW = 'window1'

    def __init__(self, *args):
        super(Window, self).__init__(*args)

        builder = Gtk.Builder()
        builder.add_from_file(
            os.path.join(
                os.path.dirname(__file__),
                self.GLADE_FILE
            )
        )
        self.builder = builder
        self.change_window()

    def change_window(self, window=None):
        if window is None:
            window = self.ROOT_WINDOW

        self.window = self.builder.get_object(window)
        self.builder.connect_signals(self.Handler(self))

        self.window.show_all()

    @staticmethod
    def main():
        """
            Gtk.main wrapper.
        """
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        print('Main Enter')
        Gtk.main()
        print('Main Exit')

    class BaseHandler(object):
        """
            Main Window Event Handler
        """

        def __init__(self, parent):
            super(Window.BaseHandler, self).__init__()
            self.parent = parent
            parent.window.connect("delete-event", self.on_delete_window)

        @staticmethod
        def on_delete_window(*args):
            """
                Window Close Action
            """
            Gtk.main_quit(*args)

    # pylint: enable=no-member
