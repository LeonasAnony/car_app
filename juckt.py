import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import socket

# Replace 'hostname' and 'port' with the appropriate values for your use case
HOST = '192.168.133.180'
PORT = 4711

def send_tcp_message(button_label):
    try:
        # Create a socket and connect to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            # Send a message based on the button label
            message = f"set tick on"
            s.sendall(message.encode('utf-8'))

    except Exception as e:
        print(f"Error: {e}")

def on_button_click(widget, label):
    button_label = widget.get_label()
    label.set_text(f"Button '{button_label}' clicked!")

    # Send the TCP message
    send_tcp_message(button_label)

# Create a GTK window
win = Gtk.Window()
win.set_title("Button Example")
win.connect("destroy", Gtk.main_quit)

# Create a box to hold the buttons
box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
win.add(box)

# Create three buttons
button1 = Gtk.Button(label="Button 1")
button2 = Gtk.Button(label="Button 2")
button3 = Gtk.Button(label="Button 3")

# Create a label to display button click messages
label = Gtk.Label()

# Connect button click events to a common callback
button1.connect("clicked", on_button_click, label)
button2.connect("clicked", on_button_click, label)
button3.connect("clicked", on_button_click, label)

# Add buttons and label to the box
box.pack_start(button1, True, True, 0)
box.pack_start(button2, True, True, 0)
box.pack_start(button3, True, True, 0)
box.pack_start(label, True, True, 0)

win.show_all()

Gtk.main()
