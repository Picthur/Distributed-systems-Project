# utils.py

import socket

# ANSI color escape sequences
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'
BLUE = '\033[94m'

def check_available_ports(ip_address):
    used_ports = set()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    max_port = 1010
    min_port = 1000
    for port in range(min_port, max_port + 1):
        try:
            s.bind((ip_address, port))
        except socket.error:
            used_ports.add(port)
        finally:
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    available_ports = [port for port in range(min_port, max_port + 1) if port not in used_ports]
    print(f"\n{GREEN}Used ports: {sorted(used_ports)}{RESET}")
    print(f"{RED}Available ports: {available_ports}{RESET}")
    return available_ports

def get_used_ports(ip_address):
    used_ports = set()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    max_port = 1010
    min_port = 1000
    for port in range(min_port, max_port + 1):
        try:
            s.bind((ip_address, port))
        except socket.error:
            used_ports.add(port)
        finally:
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return used_ports

def send_message(sock, message, address):
    try:
        sock.sendto(message.encode(), address)
    except socket.error as e:
        print(f"{RED}Failed to send message to {address}: {e}{RESET}")

def send_message_with_timestamp(sock, message, address, clock):
    clock.tick()
    timestamped_message = f"{message}|{clock.time}|timestamp"
    send_message(sock, timestamped_message, address)
    print(f"Sent message '{message}' to {address[0]}:{address[1]}")

def process_message(message, addr, clock, neighbors):
    parts = message.split("|")
    if len(parts) == 3 and parts[2] == "timestamp":
        message = parts[0]
        received_time = int(parts[1])
        clock.update(received_time)
        if message.startswith("dm-"):
            private_message = message[3:]
            print(f"\n{BLUE}Private message from {addr[0]}:{addr[1]}: {private_message}{RESET}")
        else:
            print(f"\n{GREEN}{addr[0]}:{addr[1]}: {message}{RESET}")
    else:
        print(f"\n{RED}Invalid message format from {addr}: {message}{RESET}")

