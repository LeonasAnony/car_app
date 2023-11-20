class TelnetListen():
	def __init__(self, tn, win):
		self.tn = tn
		self.win = win

	def telnet_alive(self):
		try: 
			self.tn.sock_avail()
			return True
		except Exception as e:
			return False

	def telnet_run (self):
		while(True):
			if not self.telnet_alive():
				print("conenction closed")

			msg = self.tn.read_until(b"\r\n")
			if(b"<TICK>" in msg):
				self.win.ledHeartbeat.set_color(0,255,0)
			elif(b"<EVENT><KEY>switch</KEY><VALUE>on</VALUE></EVENT>\r\n" in msg):
				self.win.ledSwitch.set_color(0,255,0)
			elif(b"<EVENT><KEY>switch</KEY><VALUE>off</VALUE></EVENT>\r\n" in msg):
				self.win.ledSwitch.set_color(255,0,0)

			