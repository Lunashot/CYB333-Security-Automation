import socket


HOST = "127.0.0.1"
PORT = 65432
BUFFER_SIZE = 1024


def run_server() -> None:
    """Listen for clients and reply to each message received."""
    try:
        # A context manager closes the socket when the program ends.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            print(f"Server listening on {HOST}:{PORT}")
            print("Press Ctrl+C to stop the server.")

            while True:
                connection, address = server_socket.accept()
                print(f"Client connected from {address[0]}:{address[1]}")

                with connection:
                    while True:
                        data = connection.recv(BUFFER_SIZE)

                        # Empty data means the client disconnected.
                        if not data:
                            print("Client disconnected cleanly.")
                            break

                        message = data.decode("utf-8")
                        print(f"Received: {message}")

                        if message.lower() == "quit":
                            connection.sendall(b"Goodbye. Connection closing.")
                            print("Client requested a clean disconnection.")
                            break

                        response = f"Server received: {message}"
                        connection.sendall(response.encode("utf-8"))

    except PermissionError:
        print("Error: Permission was denied when opening the server socket.")
    except OSError as error:
        print(f"Server error: {error}")
    except KeyboardInterrupt:
        print("\nServer shut down cleanly.")


if __name__ == "__main__":
    run_server()
