import gi
import telnetlib
from mainWindow import MainWindow

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio

class ConnectWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="ESP32 Interface Connect")

        self.set_default_size(600, 400)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        title = Gtk.Label(label="Connect with ESP32 over TCP")
        vbox.pack_start(title, True, True, 0)

        labelip = Gtk.Label(label="IP Address:")
        vbox.pack_start(labelip, False, False, 0)
        self.entryip = Gtk.Entry()
        self.entryip.set_text("127.0.0.1")
        vbox.pack_start(self.entryip, True, True, 0)

        labelport = Gtk.Label(label="Port:")
        vbox.pack_start(labelport, False, False, 0)
        self.entryport = Gtk.Entry()
        self.entryport.set_text("8000")
        vbox.pack_start(self.entryport, True, True, 0)

        self.buttonconnect = Gtk.Button.new_with_label("Connect")
        self.buttonconnect.connect("clicked", self.on_connect)
        vbox.pack_start(self.buttonconnect, True, True, 0)

    def on_connect(self, button):
        tn = telnetlib.Telnet()
        tn.open(self.entryip.get_text(), self.entryport.get_text())
        tn.read_until("-> ".encode("utf-8"))
        
        self.destroy()
        win2 = MainWindow(tn)
        win2.connect("destroy", Gtk.main_quit)
        win2.show_all()