import gi
from mainWindow import MainWindow

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class ConnectWindow(Gtk.Window):
	def __init__(self, tnhelper):
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

		labelbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
		labeltimeout = Gtk.Label(label="Connection Timeout:")
		labelreconnect = Gtk.Label(label="Auto Reconnect:")
		labelbox.pack_start(labeltimeout, True, False, 5)
		labelbox.pack_start(labelreconnect, True, False, 5)
		settingbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
		adjustment = Gtk.Adjustment(5.0, 2.0, 10.0, 1.0, 2.0, 0.0);
		self.spintimeout = Gtk.SpinButton.new(adjustment, 1.0, 0);
		self.switchauto = Gtk.Switch()
		self.switchauto.props.valign = Gtk.Align.CENTER
		self.switchauto.set_active(True)
		settingbox.pack_start(self.spintimeout, True, True, 5)
		settingbox.pack_start(self.switchauto, True, False, 5)
		vbox.pack_start(labelbox, False, True, 0)
		vbox.pack_start(settingbox, False, True, 0)

		buttonconnect = Gtk.Button.new_with_label("Connect")
		buttonconnect.connect("clicked", self.on_connect)
		vbox.pack_start(buttonconnect, True, True, 0)

		self.tnhelper = tnhelper

	def on_connect(self, *args):
		self.tnhelper.connect(self.entryip.get_text(), self.entryport.get_text(), self.spintimeout.get_value_as_int(), self.switchauto.get_active())

		self.destroy()
