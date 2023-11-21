import gi
from mainWindow import MainWindow

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class ConnectWindow(Gtk.Window):
	def __init__(self, tncon):
		super().__init__(title="ESP32 Interface Connect")

		self.set_default_size(400, -1)

		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.add(vbox)

		title = Gtk.Label(label="Connect with ESP32 over TCP")
		vbox.pack_start(title, False, False, 25)

		labelip = Gtk.Label(label="IP Address:")
		vbox.pack_start(labelip, False, False, 5)
		self.entryip = Gtk.Entry()
		self.entryip.set_text("bc.doorsign.int")
		vbox.pack_start(self.entryip, False, True, 0)

		labelport = Gtk.Label(label="Port:")
		vbox.pack_start(labelport, False, False, 5)
		self.entryport = Gtk.Entry()
		self.entryport.set_text("4711")
		vbox.pack_start(self.entryport, False, True, 0)

		labelport = Gtk.Label(label="Connection Timeout:")
		vbox.pack_start(labelport, False, False, 5)
		adjustment = Gtk.Adjustment(5.0, 2.0, 10.0, 1.0, 2.0, 0.0);
		self.spintimeout = Gtk.SpinButton.new(adjustment, 1.0, 0);
		vbox.pack_start(self.spintimeout, False, True, 0)

		buttonconnect = Gtk.Button.new_with_label("Connect")
		buttonconnect.connect("clicked", self.on_connect)
		vbox.pack_start(buttonconnect, True, True, 0)

		self.tncon = tncon

	def on_connect(self, button):
		self.tncon.open(self.entryip.get_text(), self.entryport.get_text())
		self.tncon.read_until(b"-> ")

		#TODO: Get initial Values and set Color acordingly (main or mainWindow are better places to do this)
		#	   Get switch
		#	   Get led
		#	   Get value

		self.tncon.write(b"set tick on\n") #TODO: rethink setting tick on here, maybe better in main

		self.destroy()
