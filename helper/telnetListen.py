import re

class TelnetListen():
	def __init__(self, tn, win):
		self.tn = tn
		self.win = win

	def telnet_run (self):
		while(True):
			#TODO: detect disconnect
			msg = self.tn.read_until(b"\r\n")
			if(b"<TICK>" in msg):
				count = re.findall(r'\d+', str(msg))[0]
				self.win.counter.set_text(str(count))
				self.win.ledHeartbeat.set_color(0,255,0)
			elif(b"<EVENT><KEY>switch</KEY><VALUE>on</VALUE></EVENT>\r\n" in msg):
				self.win.ledSwitch.set_color(0,255,0)
			elif(b"<EVENT><KEY>switch</KEY><VALUE>off</VALUE></EVENT>\r\n" in msg):
				self.win.ledSwitch.set_color(255,0,0)

			