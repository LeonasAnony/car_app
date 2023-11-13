import time
import tkinter as tk
import telnetlib

HOST = "af.doorsign.int"
PORT = 4711
LED_ON_COMMAND = b"set led on\n"
LED_OFF_COMMAND = b"set led off\n"
TICK_ON_COMMAND = b"set tick on\n"
#input_value = 
#SET_VALUE_COMMAND = b"set value " + input_value + "\n"

class TelnetLEDController:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.telnet_connection = None

    def connect(self):
        try:
            self.telnet_connection = telnetlib.Telnet(self.host, self.port, timeout=1)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def send_command(self, command):
        try:
            self.telnet_connection.write(command)
            self.telnet_connection.read_until(b"\n", timeout=1)  # Read server response (optional)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def read_messages(self):
        try:
            message = self.telnet_connection.read_until(b"\n", timeout=1)
            return message.decode("utf-8")
        except Exception as e:
            print(f"Error: {e}")
            return None

    def close_connection(self):
        if self.telnet_connection:
            self.telnet_connection.close()

controller = TelnetLEDController(HOST, PORT)

def on_led_toggle():
    if led_state.get():
        success = controller.send_command(LED_ON_COMMAND)
        label.config(text="LED Status: ON" if success else "Failed to turn ON LED")
    else:
        success = controller.send_command(LED_OFF_COMMAND)
        label.config(text="LED Status: OFF" if success else "Failed to turn OFF LED")

connected = False

def on_reconnect():
    if not connected:
        if controller.connect():
            print("reconnected")
            connection_state.config(text="Connected")
            root.after(1000, set_tick_on)
    else:
        print("Failed to re-establish Telnet connection.")

def set_tick_on():
    controller.send_command(TICK_ON_COMMAND)

def print_messages():
    global connected
    message = controller.read_messages()
    if message:
        if not connected:
            print("connected")
            connected = True
            reconnect_button["state"] = "disabled"
        print("Received message:", message.strip())
    elif connected:
        print("disconnected")
        connection_state.config(text="Disconnected")
        connected = False
        reconnect_button["state"] = "normal"
    root.after(500, print_messages)  # Check for new messages every 1 second

root = tk.Tk()
root.title("LED Controller")

connection_state = tk.Label(root, text="Disconnected")
connection_state.pack()

led_state = tk.BooleanVar()

toggle_button = tk.Checkbutton(root, text="Toggle LED", variable=led_state, command=on_led_toggle)
toggle_button.pack()

reconnect_button = tk.Button(root, text="Reconnect", command=on_reconnect)
reconnect_button.pack()

label = tk.Label(root, text="LED Status: OFF")
label.pack()

# Attempt to establish the telnet connection
if controller.connect():
    connection_state.config(text="Connected")
    root.after(1000, set_tick_on)
    root.after(1000, print_messages)  # Start checking for messages
    root.mainloop()
    # Close the telnet connection when the application is closed
    controller.close_connection()
else:
    print("Failed to establish Telnet connection.")