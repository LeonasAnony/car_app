import telnetlib
class TEilelia:
    con_alive = True

    def is_telnet_alive(tn):
        try:
            tn.sock_avail()
            return True
        except Exception as e:
            return False

    # Example usage:
    host = "127.0.0.1"
    port = 8000

    tn = telnetlib.Telnet(host, port)

    # Your Telnet operations go here
        

    # Check if the connection is still alive
    if is_telnet_alive(tn):
        print("Telnet connection is alive")
    else:
        print("Telnet connection is not alive")

    # Close the connection when done
    tn.close()
