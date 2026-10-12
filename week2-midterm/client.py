"""Simple TCP client for the CYB333 socket assignment."""

import socket


HOST = "127.0.0.1"
PORT = 65432
BUFFER_SIZE = 1024


def run_client() -> None:
    """Connect to the server and exchange messages."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.settimeout(5)
            print(f"Connecting to {HOST}:{PORT}...")
            client_socket.connect((HOST, PORT))
            print("Connected to the server.")

            while True:
                message = input("Enter a message (or type quit): ").strip()

                if not message:
                    print("Please enter a message.")
                    continue

                client_socket.sendall(message.encode("utf-8"))
                response = client_socket.recv(BUFFER_SIZE).decode("utf-8")
                print(f"Response: {response}")

                if message.lower() == "quit":
                    print("Disconnected cleanly.")
                    break

    except ConnectionRefusedError:
        print("Error: Connection refused. Make sure the server is running.")
    except socket.timeout:
        print("Error: The connection timed out.")
    except OSError as error:
        print(f"Client error: {error}")
    except KeyboardInterrupt:
        print("\nClient closed by the user.")


if __name__ == "__main__":
    run_client()
