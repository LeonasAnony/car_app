import gi
import helper 

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MainWindow(Gtk.Window):
	def __init__(self, tncon):
		self.tncon = tncon
		
		super().__init__(title="ESP32 Interface")
		self.set_border_width(10)

		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		self.add(listbox)

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)
		label = Gtk.Label(label="LED", xalign=0)
		self.switch = Gtk.Switch()
		self.switch.props.valign = Gtk.Align.CENTER
		self.switch.set_active(False)
		self.switch.connect("state-set", self.on_switch_state_changed)
		hbox.pack_start(label, True, True, 0)
		hbox.pack_start(self.switch, False, True, 0)
		listbox.add(row)

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)
		label = Gtk.Label(label="Switch State", xalign=0)
		hbox.pack_start(label, True, True, 0)
		self.ledSwitch = helper.LEDDrawingArea()
		hbox.pack_start(self.ledSwitch, False, True, 0)
		listbox.add(row)

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)
		label = Gtk.Label(label="Heartbeat", xalign=0)
		self.ledHeartbeat = helper.LEDDrawingArea()
		hbox.pack_start(label, True, True, 0)
		hbox.pack_start(self.ledHeartbeat, False, True, 0)
		listbox.add(row)

	def on_switch_state_changed(self, switch, state):
		# Handle switch state change here
		if state:
			self.tncon.write(b"set led on\n")
		else:
			self.tncon.write(b"set led off\n")

	def dimm_led(self, led, color="r"): #TODO: eventually move this to ./helper/#
		pointer = 0
		if color == "g":
			pointer = 1
		elif color == "b":
			pointer = 2

		colorbrightness = led.rgb_color[pointer]
		if(led.rgb_color != (128,128,128)):
			match color:
				case "r":
					led.set_color((colorbrightness-10), 0, 0)
				case "g":
					led.set_color(0, (colorbrightness-10), 0)
				case "b":
					led.set_color(0, 0, (colorbrightness-10))
		if(led.rgb_color[pointer] <= 120):
			led.set_color(128,128,128)

		return True
