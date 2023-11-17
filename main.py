import gi
import telnetlib
import threading
from connectWindow import ConnectWindow
from mainWindow import MainWindow

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

class ESP32_Interface():
	def __init__(self):
		self.tn = telnetlib.Telnet()
		conWin = ConnectWindow(self.tn)
		conWin.connect("delete-event", Gtk.main_quit)
		conWin.connect("destroy", self.open_main_window)
		conWin.show_all()
		self.mainThread = threading.Thread(target=Gtk.main)
		self.mainThread.start()

	def stop_app(self, *args):
		Gtk.main_quit()

	def open_main_window(self, *args):
		self.mainWin = MainWindow(self.tn)
		self.mainWin.connect("destroy", self.stop_app)
		self.mainWin.connect("delete-event", self.stop_app) #TODO: add quit fun which stops threads
		self.mainWin.show_all()
		GObject.timeout_add(100, self.mainWin.dimm_led, self.mainWin.ledHeartbeat, "g")

		self.listenThread = threading.Thread(target=self.telnet_listen)
		self.listenThread.start()

	def telnet_listen(self): #TODO: eventually move this to ./helper/#
		while(True):
			msg = self.tn.read_until(b"\r\n")
			print(msg)
			if(b"<TICK>" in msg):
				self.mainWin.ledHeartbeat.set_color(0,255,0)
			elif(msg == b"<EVENT><KEY>switch</KEY><VALUE>on</VALUE></EVENT>\r\n"):
				self.mainWin.ledSwitch.set_color(0,255,0)
			elif(msg == b"<EVENT><KEY>switch</KEY><VALUE>off</VALUE></EVENT>\r\n"):
				self.mainWin.ledSwitch.set_color(255,0,0)

if __name__ == "__main__":
	ESP32_Interface()
