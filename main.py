import gi
import telnetlib
import time

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio

tn = telnetlib.Telnet()

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
        tn.open(self.entryip.get_text(), self.entryport.get_text())
        tn.read_until("-> ".encode("utf-8"))
        
        self.destroy()
        win2 = MainWindow()
        win2.connect("destroy", Gtk.main_quit)
        win2.show_all()



class MainWindow(Gtk.Window):
    def __init__(self):
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
            # If the switch is on, change the color of the LEDs to green
            self.led1.set_color(0, 255, 0)  # Green
            self.led2.set_color(0, 255, 0)
        else:
            # If the switch is off, change the color of the LEDs to red
            self.led1.set_color(255, 0, 0)  # Red
            self.led2.set_color(255, 0, 0)


class LEDDrawingArea(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self.set_size_request(50, 50)
        self.rgb_color = (255, 0, 0)  # Initial color is red (RGB)

        self.connect("draw", self.on_draw)

    def set_color(self, red, green, blue):
        self.rgb_color = (red, green, blue)
        self.queue_draw()

    def on_draw(self, widget, cr):
        allocation = self.get_allocation()
        width, height = allocation.width, allocation.height

        # Create a GdkRGBA color from the RGB values
        rgba_color = Gdk.RGBA()
        rgba_color.red = self.rgb_color[0] / 255
        rgba_color.green = self.rgb_color[1] / 255
        rgba_color.blue = self.rgb_color[2] / 255
        rgba_color.alpha = 1.0

        cr.set_source_rgba(rgba_color.red, rgba_color.green, rgba_color.blue, rgba_color.alpha)
        cr.arc(width / 2, height / 2, min(width, height) / 2 - 5, 0, 2 * 3.141592)
        cr.fill()
    
win = ConnectWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()