from telnetcon import TelnetCon
from leddrawing import LEDDrawingArea

import gi

HOST = "bf.doorsign.int"
PORT = 4711

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio


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
        inputIp = self.entryip = Gtk.Entry()
        self.entryip.set_text("af.doorsign.int")
        vbox.pack_start(self.entryip, True, True, 0)

        labelport = Gtk.Label(label="Port:")
        vbox.pack_start(labelport, False, False, 0)
        inputPort = self.entryport = Gtk.Entry()
        self.entryport.set_text("4711")
        vbox.pack_start(self.entryport, True, True, 0)

        self.buttonconnect = Gtk.Button.new_with_label("Connect")
        self.buttonconnect.connect("clicked", self.on_connect)
        vbox.pack_start(self.buttonconnect, True, True, 0)

    def on_connect(self, button):
        tn = TelnetCon(HOST, PORT)
        self.destroy()
        win2 = MainWindow()
        win2.connect("destroy", Gtk.main_quit)
        win2.show_all()



class MainWindow(Gtk.Window):
    
    def __init__(self):
        tn = TelnetCon(HOST, PORT)

        super().__init__(title="ESP32 Interface")

#        self.set_default_size(400, 200)

        grid = Gtk.Grid()
        self.add(grid)

        # Create two DrawingAreas for the LEDs
        self.led1 = LEDDrawingArea()
        self.led2 = LEDDrawingArea()

        # Create a Switch
        self.switch = Gtk.Switch()
        self.switch.set_active(False)  # Set the initial state to off
        self.switch.connect("state-set", self.on_switch_state_changed(True, tn))

        # Add the elements to the grid
        grid.attach(self.switch, 0, 0, 3, 1)  # Switch spans all three columns in the first row
        grid.attach(self.led1, 0, 1, 1, 1)    # LED1 in the first column of the second row
        grid.attach(self.led2, 1, 1, 1, 1)    # LED2 in the second column of the second row

    def on_switch_state_changed(self, state, TelnetCon):
        # Handle switch state change here
        tn = TelnetCon
        if state:
            tn.send_command(b"set led on\n")
            # If the switch is on, change the color of the LEDs to green
            self.led1.set_color(0, 255, 0)  # Green
            self.led2.set_color(0, 255, 0)
        else:
            tn.send_command(b"set led off\n")
            # If the switch is off, change the color of the LEDs to red
            self.led1.set_color(255, 0, 0)  # Red
            self.led2.set_color(255, 0, 0)
    
win = ConnectWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()