import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

def screen():
    display = Gdk.Display.get_default()
    if display:
        monitor = display.get_monitor(0)
        if monitor:
            geometry = monitor.get_geometry()
            screen_width = geometry.width // 2
            screen_height = geometry.height // 4
            return screen_width, screen_height
        else:
            print('no monitor detected!')
    else:
        print('no monitor detected!')