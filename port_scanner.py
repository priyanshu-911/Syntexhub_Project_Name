import socket
import threading
import argparse

from datetime import datetime


print_lock = threading.Lock()


log_file = "scan_results.txt"


def log_result(message):
    with open(log_file, "a") as f:
        f.write(message + "\n")


def scan_port(host, port, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    try:
        result = s.connect_ex((host, port))

    except socket.gaierror:
        with print_lock:
            msg = f"Hostname could not be resolved: {host}"
            print(msg)
            log_result(msg)

    except socket.error as e:
        with print_lock:
            msg = f"Socket error: {e}"
            print(msg)
            log_result(msg)

    else:
        with print_lock:
            if result == 0:
                msg = f"Port {port} OPEN"
            else:
                msg = f"Port {port} CLOSED"

            print(msg)
            log_result(msg)

    finally:
        s.close()


def start_scan(host, start_port, end_port, threads, timeout):

    print(f"\nStarting scan on {host}")
    print(f"Ports: {start_port} - {end_port}")
    print("Scanning...\n")

    log_result(f"\nScan started at {datetime.now()}")
    log_result(f"Host: {host}")
    log_result(f"Ports: {start_port}-{end_port}\n")

    thread_list = []

    for port in range(start_port, end_port + 1):

        t = threading.Thread(target=scan_port, args=(host, port, timeout))
        thread_list.append(t)
        t.start()

        if len(thread_list) >= threads:
            for th in thread_list:
                th.join()
            thread_list = []

    for th in thread_list:
        th.join()

    print("\nScan Completed")
    log_result("\nScan Completed\n")


def main():

    parser = argparse.ArgumentParser(description="TCP Port Scanner")

    parser.add_argument("-H", "--host", required=True, help="Target Host")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start Port")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End Port")
    parser.add_argument("-t", "--threads", type=int, default=50, help="Threads")
    parser.add_argument("-to", "--timeout", type=float, default=1, help="Timeout")

    args = parser.parse_args()

    try:
        host = socket.gethostbyname(args.host)

    except socket.gaierror:
        print("Error: Invalid hostname")
        return

    else:
        start_scan(host, args.start, args.end, args.threads, args.timeout)


if __name__ == "__main__":
    main()