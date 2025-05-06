import gi
import subprocess
import shlex
import os
import json

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GdkPixbuf, GLib
from config import get_apps
from load_css import load_css_
from collections import defaultdict

workspace_apps = {}

def list_apps_by_workspace():
    result = subprocess.run(["hyprctl", "-j", "clients"], capture_output=True, text=True)
    clients = json.loads(result.stdout)

    workspaces = defaultdict(list)
    for client in clients:
        workspace_id = client["workspace"]["id"]
        app_name = client["class"]
        workspaces[workspace_id].append(app_name)

    for ws_id in sorted(workspaces):
        for app in workspaces[ws_id]:
            if app == 'Visual Studio Code':
                app = 'Code'
            workspace_apps[app] = ws_id


def open_app(widget, exec, name):
    check = subprocess.run("hyprctl clients | grep -E 'workspace|class'", 
                           shell=True, capture_output=True, text=True)


    if name in check.stdout.strip():
        list_apps_by_workspace()
        subprocess.Popen(['hyprctl', 'dispatch', 'workspace', str(workspace_apps.get(name))])


    else:
        if exec =='htop' or exec == 'yazi' or exec == 'vim' or exec == 'nvim':
            subprocess.Popen(["kitty", "-e", "sh", "-c", exec])
        else:
            cmd = shlex.split(exec)
            subprocess.Popen(cmd, start_new_session = True, cwd = os.path.expanduser("~"))

def load(main_box):
    load_css_()
    
    app = get_apps()
    for icon, exec_cmd, name in app:

        button = Gtk.Button()
        button.set_size_request(48, 48)
        button.get_style_context().add_class('App-Button')

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 32, 0)
        scaled_pixbuf = pixbuf.scale_simple(20, 20, GdkPixbuf.InterpType.BILINEAR)
        image = Gtk.Image.new_from_pixbuf(scaled_pixbuf)


        dot_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        dot_box.set_halign(Gtk.Align.CENTER)


        if name == 'Visual Studio Code':
            name = 'Code'
        # count_windows(name, dot_box, button)
        
        vbox.pack_start(image, False, False, 0)
        vbox.pack_start(dot_box, False, False, 0)

        button.add(vbox)

        button.connect('clicked', open_app, exec_cmd, name)
        main_box.pack_start(button, False, False, 0)
        GLib.timeout_add(250, count_windows, name, dot_box, button)



def count_windows(app, dot_box, button):
    result = subprocess.run(['hyprctl', 'clients', '-j'], stdout=subprocess.PIPE, text=True)
    clients = json.loads(result.stdout)
    windows = [c for c in clients if c['class'] == app]
    len_window = int(len(windows))


    for child in dot_box.get_children():
        dot_box.remove(child)

    if len_window > 0:
        button.get_style_context().remove_class('App-Button')
        button.get_style_context().add_class('Active-Apps')

        for count in range(len_window):
            dot = Gtk.Label(label='')
            dot.set_size_request(1, 1)
            dot.get_style_context().add_class('Dot')
            dot_box.pack_start(dot, False, False, 0)

        dot_box.show_all()
    else:
        button.get_style_context().remove_class('Active-Apps')
        button.get_style_context().add_class('App-Button')

    return True