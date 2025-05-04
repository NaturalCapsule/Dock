import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GtkLayerShell', '0.1')

from gi.repository import Gtk, Gdk, GtkLayerShell
from get_screen import screen
from layouts import LayOuts


class Dock(Gtk.Window):
    def __init__(self):
        super().__init__()

        GtkLayerShell.init_for_window(self)

        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_resizable(False)
        self.set_hexpand(True)
        self.get_style_context().add_class('Window')
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)
        self.layouts()
        self.setupUI()
        # self.test()
        
        
        
        
        self.show_all()

    def layouts(self):
        self.layouts_ = LayOuts(self)
        
        self.set_default_size(50, 50)
        self.layouts_.bottom_position(parent=self, width_gap=10, height_gap=10)


    def setupUI(self):
        self.set_size_request(100, 50)
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(self.main_box)


    def test(self):
        button = Gtk.Button()
        
        image = Gtk.Image.new_from_icon_name('kitty', Gtk.IconSize.SMALL_TOOLBAR)
        button.set_image(image)
        
        self.main_box.pack_start(button, False, False, 0)



css_provider = Gtk.CssProvider()
with open ('config/style.css', 'r') as f:
    css = f.read()
css_provider.load_from_data(css.encode())

Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

dock = Dock()
dock.connect("destroy", Gtk.main_quit)
Gtk.main()