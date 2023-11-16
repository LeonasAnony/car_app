import gi
from connectWindow import ConnectWindow

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio

if __name__ == "__main__":
    win = ConnectWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()

