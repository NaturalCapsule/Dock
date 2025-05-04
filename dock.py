# import gi
# gi.require_version('Gtk', '3.0')
# gi.require_version('Gdk', '3.0')
# from gi.repository import Gtk, Gdk

# class Dock(Gtk.Window):
#     def __int__(self):
#         super().__init__(title = 'Test')
#         self.set_decorated(False)
#         self.set_keep_above(True)
#         self.set_resizable(False)
#         self.SetupUI()
        
        
#         self.show_all()

#         # self.set_type_hint(Gdk.WindowTypeHint.DOCK)
    
#     def SetupUI(self):
#         self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        
#         button = Gtk.Button(label = 'test')
#         self.main_box.add(button)
        
#         self.add(self.main_box)



# app = Dock()
# app.move(300, 300)
# app.connect("destroy", Gtk.main_quit)
# Gtk.main()



import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk
from get_screen import screen
from layouts import LayOuts

 

class Dock(Gtk.Window):
    def __init__(self):
        super().__init__()

        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_resizable(False)
        self.get_style_context().add_class('Window')
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)
        self.setupUI()
        self.layouts()

    def layouts(self):
        layouts_ = LayOuts(self)
        button = Gtk.Button(label="New")
        layouts_.main_box.pack_start(button, False, False, 0)
        layouts_.bottom_position(self, 10, 10)



    def setupUI(self):
        # self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        # button = Gtk.Button(label="New")
        # self.main_box.pack_start(button, False, False, 0)
        
        # self.add(self.main_box)
        
        x, y = screen()
        self.set_size_request(100, 100)
        self.move(x, y)
        
        self.show_all()


dock = Dock()
dock.connect("destroy", Gtk.main_quit)
Gtk.main()