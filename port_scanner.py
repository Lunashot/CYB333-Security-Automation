"""Small TCP port scanner for authorized CYB333 assignment targets only."""

import argparse
import socket
import time
from datetime import datetime


ALLOWED_TARGETS = {"127.0.0.1", "localhost", "scanme.nmap.org"}
MAX_PORTS = 100
CONNECTION_TIMEOUT = 1.0
SCAN_DELAY = 0.05


def valid_port(value: str) -> int:
    """Return a valid TCP port or report an argparse input error."""
    try:
        port = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("ports must be whole numbers") from error

    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("ports must be between 1 and 65535")
    return port


def parse_arguments() -> argparse.Namespace:
    """Read and validate command line arguments."""
    parser = argparse.ArgumentParser(
        description="Scan a small TCP port range on an approved target."
    )
    parser.add_argument(
        "target",
        help="Allowed targets: 127.0.0.1, localhost, or scanme.nmap.org",
    )
    parser.add_argument("start_port", type=valid_port, help="first port to scan")
    parser.add_argument("end_port", type=valid_port, help="last port to scan")
    return parser.parse_args()


def scan_port(ip_address: str, port: int) -> bool:
    """Return True when a TCP connection to the port succeeds."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as scan_socket:
        scan_socket.settimeout(CONNECTION_TIMEOUT)
        return scan_socket.connect_ex((ip_address, port)) == 0


def main() -> None:
    """Validate the target and scan the requested port range."""
    args = parse_arguments()
    target = args.target.lower().rstrip(".")

    if target not in ALLOWED_TARGETS:
        print("Error: This assignment only permits localhost and scanme.nmap.org.")
        return

    if args.start_port > args.end_port:
        print("Error: The starting port cannot be greater than the ending port.")
        return

    total_ports = args.end_port - args.start_port + 1
    if total_ports > MAX_PORTS:
        print(f"Error: Limit each scan to {MAX_PORTS} ports or fewer.")
        return

    try:
        ip_address = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"Error: The host {target} could not be resolved or reached.")
        return

    started = datetime.now()
    print(f"Scan started: {started:%Y-%m-%d %H:%M:%S}")
    print(f"Target: {target} ({ip_address})")
    print(f"Port range: {args.start_port}-{args.end_port}\n")

    open_ports = []
    try:
        for port in range(args.start_port, args.end_port + 1):
            if scan_port(ip_address, port):
                print(f"Port {port}: OPEN")
                open_ports.append(port)
            else:
                print(f"Port {port}: CLOSED or FILTERED")
            time.sleep(SCAN_DELAY)
    except (OSError, socket.timeout) as error:
        print(f"Scan error: {error}")
        return
    except KeyboardInterrupt:
        print("\nScan stopped cleanly by the user.")
        return

    finished = datetime.now()
    print(f"\nOpen ports: {open_ports if open_ports else 'None found'}")
    print(f"Scan finished: {finished:%Y-%m-%d %H:%M:%S}")
    print(f"Elapsed time: {(finished - started).total_seconds():.2f} seconds")


if __name__ == "__main__":
    main()
