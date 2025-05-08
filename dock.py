import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GtkLayerShell', '0.1')

from gi.repository import Gtk, Gdk, GtkLayerShell
from config import *
from layouts import LayOuts
from load_apps import load
from load_css import load_css_
from load_media import *
from media import pause_play, backward, forward

class Dock(Gtk.Window):
    def __init__(self):
        super().__init__()

        GtkLayerShell.init_for_window(self)

        self.layouts()
        self.setupUI()
        self.show_media = config.getboolean('Appearance', 'ShowMedia')
        if self.show_media:
            self.media_()
            GLib.timeout_add(300, update_media, self.media_label, self.media_image)
            GLib.timeout_add(100, update_pauseplay, self.play_pause)
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

    def media_(self):
        self.media_label = Gtk.Label()
        self.media_label.get_style_context().add_class('Video-Title')
        
        self.media_image = Gtk.Image()
        self.media_image.get_style_context().add_class('Thumnbail')

        self.play_pause = Gtk.Button(label='󰐊')
        self.play_pause.connect('clicked', pause_play)
        self.play_pause.get_style_context().add_class('Play-Pause')

        self.forward = Gtk.Button(label='')
        self.forward.connect('clicked', forward)
        self.forward.get_style_context().add_class('Forward')
        

        self.backward = Gtk.Button(label='')
        self.backward.connect('clicked', backward)
        self.backward.get_style_context().add_class('Backward')


        show = show_media_buttons()
        if show:
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            hbox.set_halign(Gtk.Align.CENTER)
            hbox.pack_start(self.backward, False, False, 0)
            hbox.pack_start(self.play_pause, False, False, 0)
            hbox.pack_start(self.forward, False, False, 0)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox.set_halign(Gtk.Align.CENTER)
        
        if show and self.show_media:
            vbox.pack_start(self.media_label, False, False, 0)
            vbox.pack_start(hbox, False, False, 0)

        self.main_box.pack_start(self.media_image, False, False, 0)
        if show:
            self.main_box.pack_start(vbox, False, False, 0)
        else:
            self.main_box.pack_start(self.media_label, False, False, 0)


load_css_()

dock = Dock()
dock.connect("destroy", Gtk.main_quit)
Gtk.main()