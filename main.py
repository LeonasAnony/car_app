import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio


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
        win2.show_all()

class MainWindow(Gtk.Window):
    def __init__(self):
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
        self.switch.connect("state-set", self.on_switch_state_changed)

        # Add the elements to the grid
        grid.attach(self.switch, 0, 0, 3, 1)  # Switch spans all three columns in the first row
        grid.attach(self.led1, 0, 1, 1, 1)    # LED1 in the first column of the second row
        grid.attach(self.led2, 1, 1, 1, 1)    # LED2 in the second column of the second row

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