import gi
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
		self.tnhelper = helper.TelnetHelper()
		self.conWin = ConnectWindow(self.tnhelper)
		self.conWin.connect("delete-event", Gtk.main_quit)
		self.conWin.connect("destroy", self.open_main_window)
		self.conWin.show_all()
		self.mainThread = threading.Thread(target=Gtk.main)
		self.mainThread.start()

	def stop_app(self, *args):
		Gtk.main_quit()
		self.tnhelper.con.write(b"set tick off\n")
		time.sleep(0.2)
		self.tnhelper.con.close()
		sys.exit()

	def open_main_window(self, *args):
		self.mainWin = MainWindow(self.tnhelper)
		self.mainWin.connect("destroy", self.stop_app)
		self.mainWin.connect("delete-event", self.stop_app)
		self.mainWin.show_all()

		self.tnhelper.init_values(self.mainWin)

		GLib.timeout_add(100, self.mainWin.ledHeartbeat.dimm_led, "g")

		self.listenThread = threading.Thread(target=self.tnhelper.listen_run)
		self.listenThread.start()


if __name__ == "__main__":
	ESP32_Interface()
