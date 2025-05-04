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


        # if pos == "left" or  pos == "right":
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        parent.add(self.main_box)
        
        # self.left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # self.middle_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # self.right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # elif pos == "top" or pos == "bottom":
        #     main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        #     parent.add(main_box)

        #     self.left_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        #     self.middle_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        #     self.right_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        #     self.left_spacer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        #     self.right_spacer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)



        # main_box.pack_start(self.left_box, False, False, 0)
        # main_box.pack_start(self.middle_box, False, False, 0)
        # main_box.pack_start(self.right_box, False, False, 0)

        # self.middle_box.set_halign(Gtk.Align.CENTER)



    # def left_position(self, parent, width_gap, desired_width, height_gap):
    #     GtkLayerShell.init_for_window(parent)
    #     GtkLayerShell.set_layer(parent, GtkLayerShell.Layer.TOP)

    #     GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.LEFT, True)
    #     GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.TOP, True)
    #     GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.BOTTOM, True)

    #     GtkLayerShell.set_margin(parent, GtkLayerShell.Edge.TOP, height_gap)
    #     GtkLayerShell.set_margin(parent, GtkLayerShell.Edge.BOTTOM, height_gap)

    #     GtkLayerShell.set_margin(parent, GtkLayerShell.Edge.LEFT, width_gap)

    #     GtkLayerShell.set_exclusive_zone(parent, desired_width)

    #     parent.set_size_request(desired_width, -1)

    #     GtkLayerShell.auto_exclusive_zone_enable(parent)


    # def right_position(self, parent, width_gap, desired_width, height_gap):
    #     GtkLayerShell.init_for_window(parent)
    #     GtkLayerShell.set_layer(parent, GtkLayerShell.Layer.TOP)

    #     GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.RIGHT, True)
    #     GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.TOP, True)
    #     GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.BOTTOM, True)

    #     GtkLayerShell.set_margin(parent, GtkLayerShell.Edge.TOP, height_gap)
    #     GtkLayerShell.set_margin(parent, GtkLayerShell.Edge.BOTTOM, height_gap)

    #     GtkLayerShell.set_margin(parent, GtkLayerShell.Edge.RIGHT, width_gap)

    #     GtkLayerShell.set_exclusive_zone(parent, desired_width)

    #     parent.set_size_request(desired_width, -1)

    #     GtkLayerShell.auto_exclusive_zone_enable(parent)

    
    # def top_position(self, parent, width_gap, height_gap):
    #     GtkLayerShell.init_for_window(parent)
    #     GtkLayerShell.set_layer(parent, GtkLayerShell.Layer.TOP)
    #     GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.TOP, True)
    #     GtkLayerShell.auto_exclusive_zone_enable(parent)
    #     GtkLayerShell.set_margin(parent, GtkLayerShell.Edge.TOP, height_gap)


    def bottom_position(self, parent, width_gap, height_gap):
        GtkLayerShell.init_for_window(parent)
        GtkLayerShell.set_layer(parent, GtkLayerShell.Layer.BOTTOM)
        GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.BOTTOM, True)
        GtkLayerShell.auto_exclusive_zone_enable(parent)
        GtkLayerShell.set_margin(parent, GtkLayerShell.Edge.BOTTOM, height_gap)