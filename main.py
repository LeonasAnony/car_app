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

		self.labelip = Gtk.Label(label="IP Address:")
		self.box.pack_start(self.labelip, False, False, 0)
		self.entryip = Gtk.Entry()
		self.entryip.set_text("127.0.0.1")
		self.box.pack_start(self.entryip, True, True, 0)

		self.labelport = Gtk.Label(label="Port:")
		self.box.pack_start(self.labelport, False, False, 0)
		self.entryport = Gtk.Entry()
		self.entryport.set_text("8000")
		self.box.pack_start(self.entryport, True, True, 0)

		self.labelbutton = Gtk.Label(label="button")
		self.box.pack_start(self.labelbutton, False, False, 0)
		self.buttonsubmit = Gtk.Button.new_with_label("Click Me")
		self.buttonsubmit.connect("clicked", self.on_click_me_clicked)
		self.box.pack_start(self.buttonsubmit, True, True, 0)

	def on_click_me_clicked(self, button):
       		print('"Click me" button was clicked')
	
win = ConnectWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()