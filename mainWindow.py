import gi
import telnetlib
from .helper.ledDrawing import LEDDrawingArea

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio

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
        self.led1 = LEDDrawingArea()
        hbox.pack_start(self.led1, False, True, 0)
        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label(label="Heartbeat", xalign=0)
        self.led2 = LEDDrawingArea()
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(self.led2, False, True, 0)
        listbox.add(row)


    def on_switch_state_changed(self, switch, state):
        # Handle switch state change here
        if state:
            self.tncon.write("set led on\n".encode("utf-8"))
        else:
            self.tncon.write("set led off\n".encode("utf-8"))