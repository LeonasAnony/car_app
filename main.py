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

class DialogConnect(Gtk.Dialog):
	def __init__(self, parent):
		super().__init__(title="Connect", transient_for=parent, flags=0)
		self.add_buttons(
			Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
		)

		self.set_default_size(600, 400)

		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.add(vbox)
		
		label = Gtk.Label(label="Connect with ESP32 over TCP")
		vbox = self.get_content_area()
		vbox.add(label)

		self.entry = Gtk.Entry()
		self.entry.set_text("IP Address")
		vbox.pack_start(self.entry, True, True, 0)
		
		self.entry = Gtk.Entry()
		self.entry.set_text("Port")
		vbox.pack_start(self.entry, True, True, 0)

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()