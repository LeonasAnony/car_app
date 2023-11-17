import gi
import telnetlib
import threading
from connectWindow import ConnectWindow
from mainWindow import MainWindow

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def open_main_window(widget, tn):
	mainWin = MainWindow(tn)
	mainWin.connect("destroy", Gtk.main_quit)
	mainWin.connect("delete-event", Gtk.main_quit)
	mainWin.show_all()

	listenThread = threading.Thread(target=telnet_listen, args=(tn, mainWin))
	listenThread.start()

def telnet_listen(tn, win): #TODO: eventually move this to ./helper/
	ledHeartbeatGreen = win.ledHeartbeat.rgb_color[1]
	if(ledHeartbeatGreen > 64):
		win.ledHeartbeat.set_color(0, (ledHeartbeatGreen-2), 0)

	match("telnet_read"): #TODO: read Telnet and switch
		case("Heartbeat"):
			win.ledHeartbeat.set_color(0,255,0)
		case("Switch ON"):
			win.ledSwitch.set_color(0,255,0)
		case("Switch OFF"):
			win.ledSwitch.set_color(255,0,0)

if __name__ == "__main__":
	tn = telnetlib.Telnet()
	conWin = ConnectWindow(tn)
	conWin.connect("delete-event", Gtk.main_quit)
	conWin.connect("destroy", open_main_window, tn)
	conWin.show_all()
	mainThread = threading.Thread(target=Gtk.main)
	mainThread.start()
