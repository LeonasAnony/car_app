import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class ConnectWindow(Gtk.Window):
	def __init__(self):
		super().__init__(title="ESP32 Inteface Connect")

		self.set_default_size(600, 400)


		self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.add(self.box)

		self.label = Gtk.Label(label="Connect with ESP32 over TCP")
		self.box.pack_start(self.label, True, True, 0)

		self.entryip = Gtk.Entry()
		self.entryip.set_text("IP Address")
		self.box.pack_start(self.entryip, True, True, 0)
		
		self.entryport = Gtk.Entry()
		self.entryport.set_text("Port")
		self.box.pack_start(self.entryport, True, True, 0)


win = ConnectWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()