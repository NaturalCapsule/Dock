import gi
import subprocess
import shlex
import os
import json

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GdkPixbuf, GLib
from config import *
from load_css import load_css_
from collections import defaultdict

workspace_apps = {}
workspace_apps_ = {}


def test():
    result = subprocess.run(["hyprctl", "-j", "clients"], capture_output=True, text=True)
    clients = json.loads(result.stdout)

    workspaces = defaultdict(list)
    for client in clients:
        workspace_id = client["workspace"]["id"]
        if client['class'].lower() != app_names and client['class'].lower() not in app_names and client['initialTitle'].lower() != app_names and client['initialTitle'].lower() not in app_names:
            workspaces[workspace_id].append(client['initialClass'].lower())
        else:
            continue

    for ws_id in sorted(workspaces):
        for app in workspaces[ws_id]:
            workspace_apps_[app] = ws_id
    print(workspace_apps_)

def list_apps_by_workspace(name):
    name = name.lower()
    result = subprocess.run(["hyprctl", "-j", "clients"], capture_output=True, text=True)
    clients = json.loads(result.stdout)

    workspaces = defaultdict(list)
    for client in clients:
        workspace_id = client["workspace"]["id"]
        if client['class'].lower() == name or name in client['class'].lower() or client['class'].lower() in name or client['initialTitle'].lower() == name or client['initialTitle'].lower() in name or name in client['initialTitle'].lower():
            workspaces[workspace_id].append(name)

    for ws_id in sorted(workspaces):
        for app in workspaces[ws_id]:
            workspace_apps[app] = ws_id


def check_names(name):
    name = name.lower()
    result = subprocess.run(['hyprctl', 'clients', '-j'], stdout=subprocess.PIPE, text=True)
    clients = json.loads(result.stdout)
    # windows = [c for c in clients if c['class'] == name or name in c['class'] or c['class'] in name or c['initialTitle'] == name or c['initialTitle'] in name or name in c['initialTitle']]

    for c in clients:
        if c['class'].lower() == name or name in c['class'].lower() or c['class'].lower() in name or c['initialTitle'].lower() == name or c['initialTitle'].lower() in name or name in c['initialTitle'].lower():
            return True
    return False

def open_app(widget, exec, name):
    check = subprocess.run("hyprctl clients | grep -E 'workspace|class|initialTitle'", 
                           shell=True, capture_output=True, text=True)
    
    
    swicther = get_switcher()
    
    if swicther:
        term = config.get('Options', 'Terminal')

        check = check_names(name)
        if check:
            list_apps_by_workspace(name)
            subprocess.Popen(['hyprctl', 'dispatch', 'workspace', f"{workspace_apps.get(name)}"])



        else:
            if exec =='htop' or exec == 'yazi' or exec == 'vim' or exec == 'nvim':
                subprocess.Popen([term, "-e", "sh", "-c", exec])
            else:
                cmd = shlex.split(exec)
                subprocess.Popen(cmd, start_new_session = True, cwd = os.path.expanduser("~"))

    else:
        if exec =='htop' or exec == 'yazi' or exec == 'vim' or exec == 'nvim':
            subprocess.Popen([term, "-e", "sh", "-c", exec])
        else:
            cmd = shlex.split(exec)
            subprocess.Popen(cmd, start_new_session = True, cwd = os.path.expanduser("~"))

def load(main_box):
    load_css_()
    
    app = get_apps(Gtk)
    for name, exec_cmd, icon in app:
        if name == 'Separator' and icon == None:
            main_box.pack_start(exec_cmd, False, False, 0)
        else:
            button = Gtk.Button()
            button.set_size_request(48, 48)
            button.get_style_context().add_class('App-Button')

            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

            pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 32, 0)
            x, y = dock_icons_sizes()
            scaled_pixbuf = pixbuf.scale_simple(x, y, GdkPixbuf.InterpType.BILINEAR)
            image = Gtk.Image.new_from_pixbuf(scaled_pixbuf)


            dot_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            dot_box.set_halign(Gtk.Align.CENTER)

            vbox.pack_start(image, False, False, 0)
            vbox.pack_start(dot_box, False, False, 0)

            test()

        
            button.add(vbox)
            button.connect('clicked', open_app, exec_cmd, name)
            main_box.pack_start(button, False, False, 0)
            GLib.timeout_add(250, count_windows, name, dot_box, button)



def count_windows(app, dot_box, button):
    app = app.lower()
    result = subprocess.run(['hyprctl', 'clients', '-j'], stdout=subprocess.PIPE, text=True)
    clients = json.loads(result.stdout)
    windows = [c for c in clients if c['class'].lower() == app or app in c['class'].lower() or c['class'].lower() in app or c['initialTitle'].lower() == app or c['initialTitle'].lower() in app or app in c['initialTitle'].lower()]

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