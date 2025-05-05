import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
# gi.require_version('Gtk', '3.0')
# gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk


def load_css_():
    css_provider = Gtk.CssProvider()
    with open ('config/style.css', 'r') as f:
        css = f.read()
    css_provider.load_from_data(css.encode())

    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
    