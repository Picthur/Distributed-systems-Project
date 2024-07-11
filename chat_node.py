# chat_node.py

import socket
from threading import Thread
from logical_clock import *
from utils import *

# ANSI color escape sequences
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def init_node(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    return sock

def listen_for_messages(sock, clock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = data.decode()
            process_message(message, addr, clock)
        except socket.error as e:
            print(f"{RED}Error receiving message: {e}{RESET}")
        except Exception as e:
            print(f"{RED}Unexpected error: {e}{RESET}")

def main():
    ip_address = "localhost"
    available_ports = check_available_ports(ip_address)
    if not available_ports:
        print(f"{RED}No available ports. Exiting...{RESET}")
        exit(1)

    port = available_ports[0]
    print(f"Assigned port: {port}")

    sock = init_node(ip_address, port)
    clock = LogicalClock()

    Thread(target=listen_for_messages, args=(sock, clock), daemon=True).start()

    while True:
        print("\nEnter a message:")
        message = input()
        
        if message.startswith("@"):
            try:
                target_port = int(message.split()[0][1:])
                neighbor_addr = (ip_address, target_port)
                if target_port in available_ports:
                    send_message_with_timestamp(sock, message, neighbor_addr, clock)
                    print(f"\n{GREEN}Sent private message '{message}' to {neighbor_addr[0]}:{neighbor_addr[1]}{RESET}")
                else:
                    print(f"{RED}Port {target_port} is not a connected neighbor.{RESET}")
            except ValueError:
                print(f"{RED}Invalid port specified.{RESET}")
        else:
            for neighbor_port in available_ports:
                if neighbor_port != port:
                    neighbor_addr = (ip_address, neighbor_port)
                    try:
                        send_message_with_timestamp(sock, message, neighbor_addr, clock)
                    except socket.error as e:
                        print(f"{RED}Failed to send message to {neighbor_addr}: {e}{RESET}")
            print(f"\n{GREEN}Broadcasted message '{message}' to all neighbors.{RESET}")

if __name__ == "__main__":
    main()
