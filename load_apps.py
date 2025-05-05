import gi
import subprocess
import shlex
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from config import get_apps
from load_css import load_css_

def open_app(widget, exec):
    if exec =='htop' or exec == 'yazi' or exec == 'vim' or exec == 'nvim':
        subprocess.Popen(["kitty", "-e", "sh", "-c", exec])
    else:
        cmd = shlex.split(exec)
        subprocess.Popen(cmd, start_new_session = True, cwd = os.path.expanduser("~"))

def load(main_box):
    load_css_()
    
    app = get_apps()
    for icon, exec_cmd in app.items():
        
        button = Gtk.Button()
        button.set_size_request(48, 48)
        button.get_style_context().add_class('App-Button')


        pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 32, 0)
        scaled_pixbuf = pixbuf.scale_simple(20, 20, GdkPixbuf.InterpType.BILINEAR)
        image = Gtk.Image.new_from_pixbuf(scaled_pixbuf)
        button.set_image(image)

        button.connect('clicked', open_app, exec_cmd)
        main_box.pack_start(button, False, False, 2)
