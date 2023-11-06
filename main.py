import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class ConnectWindow(Gtk.Window):
	def __init__(self):
		super().__init__(title="ESP32 Inteface Connect")

		self.set_default_size(600, 400)

		self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.add(self.vbox)

		self.label = Gtk.Label(label="Connect with ESP32 over TCP")
		self.vbox.pack_start(self.label, True, True, 0)

		self.labelip = Gtk.Label(label="IP Address:")
		self.vbox.pack_start(self.labelip, False, False, 0)
		self.entryip = Gtk.Entry()
		self.entryip.set_text("127.0.0.1")
		self.vbox.pack_start(self.entryip, True, True, 0)

		self.labelport = Gtk.Label(label="Port:")
		self.vbox.pack_start(self.labelport, False, False, 0)
		self.entryport = Gtk.Entry()
		self.entryport.set_text("8000")
		self.vbox.pack_start(self.entryport, True, True, 0)

		self.buttonconnect = Gtk.Button.new_with_label("Connect")
		self.buttonconnect.connect("clicked", self.on_connect)
		self.vbox.pack_start(self.buttonconnect, True, True, 0)

	def on_connect(self, button):
		self.destroy()
		win2 = MainWindow()
		win2.connect("destroy", Gtk.main_quit)
		win2.show()

class MainWindow(Gtk.Window):
	def __init__(self):
		super().__init__(title="ESP32 Interface")

		self.set_default_size(800, 600)
	
win = ConnectWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()