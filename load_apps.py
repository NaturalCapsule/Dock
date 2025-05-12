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
from pathlib import Path
from configparser import ConfigParser

workspace_apps = {}
workspace_apps_ = {}
opened_apps = []



desktop_dirs = [
    Path("/usr/share/applications")
]

def get_opened_app_info():
    get_other_apps()
    config_ = ConfigParser(interpolation=None)
    for directory in desktop_dirs:
        if not directory.exists():
            continue
        for file in directory.glob("*.desktop"):
            config_.read(file, encoding="utf-8")
            file = str(file).lower()
            file = file.replace('/usr/share/applications/', '')
            file = file.replace('.desktop', '')


            if file in list(workspace_apps_.keys()):
                try:
                    name = config_.get("Desktop Entry", "Name")
                    exec_cmd = config_.get("Desktop Entry", "Exec")
                    icon = config_.get("Desktop Entry", "Icon")

                    exec_cmd = clean_exec(exec_cmd)
                    if name and exec_cmd:
                        opened_apps.append((name, exec_cmd, icon))
                except Exception as e:
                    print(f"Error reading {file}: {e}")
    return opened_apps


def get_other_apps():
    global workspace_apps_
    workspace_apps_.clear()

    result = subprocess.run(["hyprctl", "-j", "clients"], capture_output=True, text=True)
    clients = json.loads(result.stdout)

    workspaces = defaultdict(list)

    for client in clients:
        workspace_id = client["workspace"]["id"]
        client_class = client['class'].lower()
        client_title = client['initialTitle'].lower()

        if client_class not in app_names and client_title not in app_names:
            workspaces[workspace_id].append(client_class)

    for ws_id in sorted(workspaces):
        for app in workspaces[ws_id]:
            workspace_apps_[app] = ws_id

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

    for c in clients:
        if c['class'].lower() == name or name in c['class'].lower() or c['class'].lower() in name or c['initialTitle'].lower() == name or c['initialTitle'].lower() in name or name in c['initialTitle'].lower():
            return True
    return False

def open_app(widget, exec, name, use_changer):
    check = subprocess.run("hyprctl clients | grep -E 'workspace|class|initialTitle'", 
                           shell=True, capture_output=True, text=True)
    
    
    swicther = get_switcher()
    
    if swicther and use_changer:
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
    
    x, y = dock_icons_sizes()
    
    app = get_apps(Gtk)
    for name, exec_cmd, icon in app:
        if name == 'Separator' and icon is None:
            main_box.pack_start(exec_cmd, False, False, 0)
        else:
            button = Gtk.Button()
            button.get_style_context().add_class('App-Button')
            button.set_tooltip_text(name)

            outer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            outer_box.set_vexpand(True)
            outer_box.set_valign(Gtk.Align.FILL)

            image_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            image_box.set_valign(Gtk.Align.CENTER)
            image_box.set_halign(Gtk.Align.CENTER)

            try:
                pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 32, 0)
                scaled_pixbuf = pixbuf.scale_simple(x, y, GdkPixbuf.InterpType.BILINEAR)
                image = Gtk.Image.new_from_pixbuf(scaled_pixbuf)
            except GLib.GError:
                image = Gtk.Image.new_from_icon_name('application-x-executable', Gtk.IconSize.DIALOG)
            image_box.pack_start(image, True, True, 0)

            dot_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            dot_box.set_halign(Gtk.Align.CENTER)
            dot_box.set_valign(Gtk.Align.END)

            outer_box.pack_start(image_box, True, True, 0)
            outer_box.pack_end(dot_box, False, False, 0)

            button.add(outer_box)

            button.connect('clicked', open_app, exec_cmd, name, True)
            main_box.pack_start(button, False, False, 0)
            GLib.timeout_add(750, count_windows, name, dot_box, button)


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
            dot.set_halign(Gtk.Align.CENTER)
            dot.set_valign(Gtk.Align.CENTER)
            dot.get_style_context().add_class('Dot')

            dot_box.pack_start(dot, False, False, 0)


        dot_box.show_all()
    else:
        button.get_style_context().remove_class('Active-Apps')
        button.get_style_context().add_class('App-Button')

    return True

shown_apps = set()
app_buttons = {}


def is_app_match(client, app_name):
    app_name = app_name.casefold().lower()
    class_name = client.get('class', '').casefold()
    initial_class = client.get('initialClass', '').casefold()
    title = client.get('initialTitle', '').casefold()

    if app_name == 'obs' or app_name == 'obs studio':
        return (
            'obs' in class_name or 
            'obs' in initial_class or
            'obs' in title
        )


    elif app_name == 'rofi':
        return (
            client.get('class', '').casefold() == 'rofi' and
            client.get('initialClass', '').casefold() == 'rofi'
        )
    else:
    
        return (
            app_name == class_name or
            app_name in class_name or
            class_name in app_name or
            app_name in title or
            title in app_name
        )


# def create_button_for_app(name, exec_cmd, icon):
#     button = Gtk.Button()
#     button.set_size_request(48, 48)
#     button.get_style_context().add_class('App-Button')
#     button.set_tooltip_text(name)

#     x, y = dock_icons_sizes()

#     vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
#     try:
#         pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 32, 0)
#         scaled_pixbuf = pixbuf.scale_simple(x, y, GdkPixbuf.InterpType.BILINEAR)
#         image = Gtk.Image.new_from_pixbuf(scaled_pixbuf)
#     except GLib.GError:
#         image = Gtk.Image.new_from_icon_name('application-x-executable', Gtk.IconSize.DIALOG)

#     dot_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
#     dot_box.set_halign(Gtk.Align.CENTER)

#     vbox.pack_start(image, False, False, 0)
#     vbox.pack_start(dot_box, False, False, 0)

#     button.add(vbox)
#     button.connect('clicked', open_app, exec_cmd, name, False)

#     return button, dot_box

def create_button_for_app(name, exec_cmd, icon):
    button = Gtk.Button()
    # button.set_size_request(48, 48)
    button.get_style_context().add_class('App-Button')
    button.set_tooltip_text(name)

    x, y = dock_icons_sizes()

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

    try:
        pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 32, 0)
        scaled_pixbuf = pixbuf.scale_simple(x, y, GdkPixbuf.InterpType.BILINEAR)
        image = Gtk.Image.new_from_pixbuf(scaled_pixbuf)
    except GLib.GError:
        image = Gtk.Image.new_from_icon_name('application-x-executable', Gtk.IconSize.DIALOG)

    dot_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    dot_box.set_halign(Gtk.Align.CENTER)
    dot_box.set_valign(Gtk.Align.END)
    dot_box.set_hexpand(False)
    dot_box.set_vexpand(False)

    vbox.pack_start(image, False, False, 0)
    vbox.pack_start(dot_box, False, False, 0)

    button.add(vbox)
    button.connect('clicked', open_app, exec_cmd, name, False)

    return button, dot_box


def count_other_apps(dot_box, app, button, main_box):
    app = app.casefold()
    result = subprocess.run(['hyprctl', 'clients', '-j'], stdout=subprocess.PIPE, text=True)
    clients = json.loads(result.stdout)

    seen_addresses = set()
    windows = []

    for c in clients:
        if is_app_match(c, app) and c['address'] not in seen_addresses:
            seen_addresses.add(c['address'])
            windows.append(c)

    len_window = len(windows)

    for child in dot_box.get_children():
        dot_box.remove(child)

    if len_window > 0:
        if not button.get_parent():
            main_box.pack_start(button, False, False, 0)
            button.show_all()

        button.get_style_context().remove_class('App-Button')
        button.get_style_context().add_class('Active-Apps')
        
        for _ in range(len_window):
            dot = Gtk.Label(label='')
            dot.set_size_request(1, 1)
            dot.get_style_context().add_class('Dot')
            dot_box.pack_start(dot, False, False, 0)

        dot_box.show_all()
    else:

        if app.casefold() in ('obs', 'obs studio'):
            return True
        parent = button.get_parent()
        if parent:
            parent.remove(button)

        parent = button.get_parent()
        if parent:
            parent.remove(button)

    return True



def count_windows(app, dot_box, button):
    app = app.casefold()
    result = subprocess.run(['hyprctl', 'clients', '-j'], stdout=subprocess.PIPE, text=True)
    clients = json.loads(result.stdout)
    windows = [c for c in clients if is_app_match(c, app)]
    len_window = len(windows)

    for child in dot_box.get_children():
        dot_box.remove(child)

    if len_window > 0:
        button.get_style_context().remove_class('App-Button')
        button.get_style_context().add_class('Active-Apps')

        for _ in range(len_window):
            dot = Gtk.Label(label='')
            dot.set_size_request(1, 1)
            dot.get_style_context().add_class('Dot')
            dot_box.pack_start(dot, False, False, 0)

        dot_box.show_all()
    else:
        button.get_style_context().remove_class('Active-Apps')
        button.get_style_context().add_class('App-Button')

    return True

def periodic_app_checker(main_box):
    global shown_apps, app_buttons

    result = subprocess.run(['hyprctl', 'clients', '-j'], stdout=subprocess.PIPE, text=True)
    clients = json.loads(result.stdout)

    for client in clients:
        app_class = client.get('class', '').casefold()
        app_title = client.get('initialTitle', '').casefold()
        app_class_ = client.get('initialClass', '').casefold()

        for name, exec_cmd, icon in get_opened_app_info():
            name_cf = name.lower()
            if name_cf in app_class or name_cf in app_title or name_cf in app_class_ or app_class_ in name_cf:
                if name_cf not in app_buttons:
                    button, dot_box = create_button_for_app(name, exec_cmd, icon)
                    app_buttons[name_cf] = (button, dot_box)
                    main_box.pack_start(button, False, False, 0)
                    button.show_all()
                    GLib.timeout_add(500, count_other_apps, dot_box, name, button, main_box)
                    break

    return True

def load_other_apps(main_box):
    load_css_()
    
    app = get_opened_app_info()
    for name, exec_cmd, icon in app:
        if name.lower() in app_buttons:
            continue

        button, dot_box = create_button_for_app(name, exec_cmd, icon)
        app_buttons[name.lower()] = (button, dot_box)
        main_box.pack_start(button, False, False, 0)
        button.show_all()
        GLib.timeout_add(750, count_other_apps, dot_box, name, button, main_box)

    GLib.timeout_add(2000, periodic_app_checker, main_box)