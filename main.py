import gi
import telnetlib
import threading
import sys
import time
from connectWindow import ConnectWindow
from mainWindow import MainWindow
import helper

#TODO: DEBUG/ Logger

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

class ESP32_Interface():
	def __init__(self):
		self.tn = telnetlib.Telnet()
		self.conWin = ConnectWindow(self.tn)
		self.conWin.connect("delete-event", Gtk.main_quit)
		self.conWin.connect("destroy", self.open_main_window)
		self.conWin.show_all()
		self.mainThread = threading.Thread(target=Gtk.main)
		self.mainThread.start()

	def stop_app(self, *args):
		Gtk.main_quit()
		self.tn.write(b"set tick off\n")
		time.sleep(0.5)
		self.tn.close()
		sys.exit()

	def open_main_window(self, *args):
		self.mainWin = MainWindow(self.tn)
		self.mainWin.connect("destroy", self.stop_app)
		self.mainWin.connect("delete-event", self.stop_app)
		self.mainWin.show_all()
		GLib.timeout_add(100, self.mainWin.ledHeartbeat.dimm_led, "g")
		
		tnlisten = helper.TelnetListen(self.tn, self.mainWin, self.conWin.spintimeout.get_value_as_int())
		self.listenThread = threading.Thread(target=tnlisten.telnet_run)
		self.listenThread.start()


if __name__ == "__main__":
	ESP32_Interface()
