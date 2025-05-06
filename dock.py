import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GtkLayerShell', '0.1')

from gi.repository import Gtk, Gdk, GtkLayerShell
from config import *
from layouts import LayOuts
from load_apps import load
from load_css import load_css_

class Dock(Gtk.Window):
    def __init__(self):
        super().__init__()

        GtkLayerShell.init_for_window(self)

        self.layouts()
        self.setupUI()
        load(self.main_box)
        
        
        self.show_all()

    def layouts(self):
        pos = get_position()
        self.layouts_ = LayOuts(self)
        self.set_default_size(100, 50)
        if pos == 'bottom':
            self.layouts_.bottom_position(parent=self, height_gap=10)
        elif pos == 'left':
            self.layouts_.left_position(self, 10, 10, 10)
        elif pos == 'right':
            self.layouts_.right_position(self, 10, 10, 10)
        else:
            self.layouts_.top_position(self, 10)


    def setupUI(self):
        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_resizable(False)
        self.set_hexpand(True)
        self.set_vexpand(False)
        self.get_style_context().add_class('Dock')
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)
        
        self.set_size_request(50, 50)
        pos = get_position()
        if pos == 'bottom' or pos == 'top':
            self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        elif pos == 'left' or pos == 'right':
            self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.add(self.main_box)

load_css_()

dock = Dock()
dock.connect("destroy", Gtk.main_quit)
Gtk.main()