import gi
import subprocess
import shlex
import os
import json

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GdkPixbuf
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
            # print(workspace_apps)
        # print()

def open_app(widget, exec, name):
    check = subprocess.run("hyprctl clients | grep -E 'workspace|class'", 
                           shell=True, capture_output=True, text=True)

    if name == 'Visual Studio Code':
        name = 'Code'

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


        pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 32, 0)
        scaled_pixbuf = pixbuf.scale_simple(20, 20, GdkPixbuf.InterpType.BILINEAR)
        image = Gtk.Image.new_from_pixbuf(scaled_pixbuf)
        button.set_image(image)

        button.connect('clicked', open_app, exec_cmd, name)
        main_box.pack_start(button, False, False, 2)



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
