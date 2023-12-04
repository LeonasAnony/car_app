import re
import time
import telnetlib

class TelnetHelper():
	def __init__(self):
		self.con = telnetlib.Telnet()
		self.connected = False
		self.ready = False


	def connect(self, ip, port, timeout, autoreconnect):
		print("connect")
		self.ip = ip
		self.port = port
		self.timeout = timeout
		self.autoreconnect = autoreconnect

		self.reconnect()


	def disconnect(self, *args):
		print("disconnecting")
		self.ready = False
		if hasattr(self, "win"):
			self.win.buttonDisconnect.set_sensitive(False)
		time.sleep(1)

		try:
			self.con.write(b"set tick off\n")
			if(b"off" not in self.con.read_until(b"off", 3)):
				raise Exception
		except Exception as error:
			print("disconnect() Error: ", type(error).__name__)
			if hasattr(self, "win"):
				self.win.ledConnection.set_color(255,255,0)
			time.sleep(0.1)
			self.disconnect()
			return
		
		print("tick set off")
		time.sleep(0.1)
		self.con.close()
		self.win.ledConnection.set_color(255,0,0)
		self.connected = False


	def reconnect(self, *args):
		print("reconnecting")
		self.ready = False
		self.reconnecting = True
		time.sleep(1)

		try:
			self.con.close()
			time.sleep(0.1)
			self.con.open(self.ip, self.port)
			if b"-> " not in self.con.read_until(b"-> ", 5):
				raise Exception
		except Exception as error:
			print("reconnect() Error: ", type(error).__name__)
			time.sleep(0.1)
			self.reconnect()
			return

		print("reconnected")
		self.connected = True
		time.sleep(0.1)
		try:
			self.con.write(b"set tick on\n")
			if(b"on" not in self.con.read_until(b"on", 3)):
				raise Exception
		except Exception as error:
			print("reconnect() Error: ", type(error).__name__)
			if hasattr(self, "win"):
				self.win.ledConnection.set_color(255,0,0)
			time.sleep(0.1)
			self.reconnect()
			return

		print("tick set on")
		self.lastTickTime = time.time()
		if hasattr(self, "win"):
			self.win.buttonDisconnect.set_sensitive(True)
			self.win.ledConnection.set_color(0,255,0)

		self.ready = True
		self.reconnecting = False


	def listen_run (self):
		while(True):
			if self.ready:
#				print(time.time()-self.lastTickTime)
				if(time.time()-self.lastTickTime >= self.timeout):
					self.ready = False
					self.connected = False
					self.win.ledConnection.set_color(255,0,0)
					self.win.buttonDisconnect.set_sensitive(False)
					continue

				try:
					msg = self.con.read_until(b"\r\n", 1)
				except Exception as error:
					print("listen_run() Error: ", type(error).__name__)
					continue # disconnected while in read_until

				if(b"<TICK>" in msg):
					count = re.findall(r'\d+', str(msg))[0]
					self.win.counter.set_text(str(count))
					self.win.ledHeartbeat.set_color(0,255,0)
					self.lastTickTime = time.time()
					print("Tick:", count)
				elif(b"<EVENT><KEY>switch</KEY><VALUE>on</VALUE></EVENT>\r\n" in msg):
					self.win.ledSwitch.set_color(0,255,0)
				elif(b"<EVENT><KEY>switch</KEY><VALUE>off</VALUE></EVENT>\r\n" in msg):
					self.win.ledSwitch.set_color(255,0,0)

			elif self.autoreconnect and not self.connected and not self.reconnecting:
				print("autoreconnect")
				self.win.ledConnection.set_color(255,255,0)
				self.reconnect()
			
			else:
				print("not connected, not autoreconnecting, waiting")
				self.win.ledConnection.set_color(255,0,0)
				time.sleep(1)


	def init_values(self, win):
		self.win = win
		self.win.buttonDisconnect.set_sensitive(True)
		self.win.ledConnection.set_color(0,255,0)
		#TODO: Get initial Values and set Color acordingly (main or mainWindow are better places to do this)
		#	   Get switch
		#	   Get led
		#	   Get value
