from configparser import ConfigParser
import re


config = ConfigParser()

config.read('config/config.ini')

apps_info = {}

def clean_exec(exec_cmd):
    return re.sub(r"\s*%[a-zA-Z]", "", exec_cmd).strip()

def get_apps():
    if 'Apps' in config:
        for key, value in config['Apps'].items():
            try:
                config_ = ConfigParser(interpolation=None)
                config_.read(value)
                
                exec_command = config_.get('Desktop Entry', 'Exec')
                icon = config_.get('Desktop Entry', 'icon')
                
                clean_exec_ = clean_exec(exec_command)
                
                apps_info[icon] = clean_exec_
            
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
