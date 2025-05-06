import gi
import os
gi.require_version('Gtk', '3.0')
gi.require_version("GtkLayerShell", "0.1")

from gi.repository import Gtk, GtkLayerShell


class LayOuts:
    def __init__(self, parent):
        
        if not GtkLayerShell.is_supported():
            print("Error: Layer Shell not supported. if you on Hyprland run this command: GDK_BACKEND=wayland python dock.py")
            exit(0)


    def left_position(self, parent, width_gap, desired_width, height_gap):
        GtkLayerShell.set_layer(parent, GtkLayerShell.Layer.TOP)

        GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.LEFT, True)
        GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.BOTTOM, True)

        GtkLayerShell.set_margin(parent, GtkLayerShell.Edge.TOP, height_gap)
        GtkLayerShell.set_margin(parent, GtkLayerShell.Edge.BOTTOM, height_gap)

        GtkLayerShell.set_margin(parent, GtkLayerShell.Edge.LEFT, width_gap)

        GtkLayerShell.set_exclusive_zone(parent, desired_width)

        parent.set_size_request(desired_width, -1)

        GtkLayerShell.auto_exclusive_zone_enable(parent)


    def right_position(self, parent, width_gap, desired_width, height_gap):
        # GtkLayerShell.init_for_window(parent)
        GtkLayerShell.set_layer(parent, GtkLayerShell.Layer.TOP)

        GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.RIGHT, True)
        GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.BOTTOM, True)

        GtkLayerShell.set_margin(parent, GtkLayerShell.Edge.TOP, height_gap)
        GtkLayerShell.set_margin(parent, GtkLayerShell.Edge.BOTTOM, height_gap)

        GtkLayerShell.set_margin(parent, GtkLayerShell.Edge.RIGHT, width_gap)

        GtkLayerShell.set_exclusive_zone(parent, desired_width)

        parent.set_size_request(desired_width, -1)

        GtkLayerShell.auto_exclusive_zone_enable(parent)

    
    def top_position(self, parent, height_gap):
        # GtkLayerShell.init_for_window(parent)
        GtkLayerShell.set_layer(parent, GtkLayerShell.Layer.TOP)
        GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.auto_exclusive_zone_enable(parent)
        GtkLayerShell.set_margin(parent, GtkLayerShell.Edge.TOP, height_gap)


    def bottom_position(self, parent, height_gap):
        GtkLayerShell.set_layer(parent, GtkLayerShell.Layer.BOTTOM)
        GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.BOTTOM, True)
        GtkLayerShell.auto_exclusive_zone_enable(parent)
        GtkLayerShell.set_margin(parent, GtkLayerShell.Edge.BOTTOM, height_gap)