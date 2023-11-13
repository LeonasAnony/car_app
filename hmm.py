import socket

# Define the target device's IP address and port
target_ip = "192.168.133.180"  # Replace with the IP address of the device you want to connect to
target_port = 4711  # Replace with the port number the device is listening on

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the target device
    client_socket.connect((target_ip, target_port))
    print(f"Connected to {target_ip}:{target_port}")

    while True:
        # Get a message from the user
        message = input("Enter a message to send (or 'quit' to exit): ")

        if message.lower() == 'quit':
            break

        # Send the message to the device
        client_socket.send(message.encode("utf-8"))

except ConnectionRefusedError:
    print("Connection to the device was refused. Make sure the device is listening on the specified port.")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the socket when done
    client_socket.close()
    print("Connection closed.")
