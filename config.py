import re
import configparser
# from configparser import ConfigParser


config = configparser.ConfigParser()

config.read('config/config.ini')

# apps_info = {}
apps_info = []

def clean_exec(exec_cmd):
    return re.sub(r"\s*%[a-zA-Z]", "", exec_cmd).strip()

def get_apps(Gtk):
    if 'Apps' in config:
        for key, value in config['Apps'].items():
            try:
                if value == 'Separator':
                    separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
                    separator.set_size_request(2, 10)  # width x height
                    separator.get_style_context().add_class('Separators')
                    apps_info.append(('Separator', separator, None))
                    
                else:
                    config_ = configparser.ConfigParser(interpolation=None)
                    config_.read(value)
                    try:
                        name = config_.get('Desktop Entry', 'Name')
                        exec_command = config_.get('Desktop Entry', 'Exec')
                        icon = config_.get('Desktop Entry', 'icon')
                        
                        clean_exec_ = clean_exec(exec_command)
                    except configparser.NoSectionError:
                        print("Error: Invalid file type, The file need to be has these inside:\n[Desktop Entry]\nName=(Name of the application)\nExec=(Execute command)\nicon=(icon)\n\nPlease try again")
                    # apps_info[icon] = clean_exec_, name
                    if name and exec_command:
                        apps_info.append((name, clean_exec_, icon))
                        # apps_info.append((icon, clean_exec_, name))
                    # print(apps_info)
            except ValueError:
                print(f"Invalid entry for {key} in config.ini. Expected format: app_path")
        return apps_info


def get_position():
    pos = config.get('Appearance', 'Position')
    if pos == 'top':
        return 'top'
    elif pos == 'bottom':
        return 'bottom'
    elif pos == 'left':
        return 'left'
    elif pos == 'right':
        return 'right'

def get_switcher():
    try:
        swicther = config.getboolean('Options', 'UseSwitcher')
        if swicther:
            return True
        else:
            return False
    except ValueError:
        print("Please set the UseSwitcher to True or False\nsince its an invalid value its set to False.")
        return False


def dock_icons_sizes():
    try:
        size = config.get('Appearance', 'IconSize')
        size = size.split(', ')
        x, y = int(size[0]), int(size[1])
        
        return x, y
    except Exception as e:
        print('Make sure you set a correct value in IconSize')
        return 20, 20
    
def show_media_buttons():
    try:
        return config.getboolean('Appearance', 'ShowMediaButtons')
    except ValueError:
        print('Make sure you set ShowMediaButtons to true of false')
        return False

def thumbnail_size():
    try:
        size = config.get('Appearance', 'ThumbnailSize')
        size = size.split(', ')
        x, y = int(size[0]), int(size[1])
        
        return x, y
    except Exception as e:
        print('Make sure you set a correct value in IconSize')
        return 20, 20