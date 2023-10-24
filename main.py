import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class MainWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="ESP32 Interface")

		self.set_border_width(6)

		dialog = DialogConnect(self)
		response = dialog.run()

		if response == Gtk.ResponseType.OK:
			print("The OK button was clicked")
		elif response == Gtk.ResponseType.CANCEL:
			print("The Cancel button was clicked")

		dialog.destroy()

class ConnectWindow(Gtk.Dialog):
	def __init__(self):
		super().__init__(title="ESP32 Connect")
		#self.add_buttons(
		#	Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
		#)

		self.set_default_size(600, 400)

		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.add(vbox)
		
		self.label = Gtk.Label(label="Connect with ESP32 over TCP")
		vbox.pack_start(self.label, True, True, 0)

		self.entryip = Gtk.Entry()
		self.entryip.set_text("IP Address")
		vbox.pack_start(self.entryip, True, True, 0)
		
		self.entryport = Gtk.Entry()
		self.entryport.set_text("Port")
		vbox.pack_start(self.entryport, True, True, 0)

win = ConnectWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()