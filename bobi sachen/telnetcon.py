import telnetlib

class TelnetCon:
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

