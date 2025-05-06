import re
from configparser import ConfigParser


config = ConfigParser()

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
                    config_ = ConfigParser(interpolation=None)
                    config_.read(value)
                    name = config_.get('Desktop Entry', 'Name')
                    exec_command = config_.get('Desktop Entry', 'Exec')
                    icon = config_.get('Desktop Entry', 'icon')
                    
                    clean_exec_ = clean_exec(exec_command)
                    
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