# logical_clock.py

import socket

# ANSI color escape sequences
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

class LogicalClock:
    def __init__(self):
        self.time = 0

    def tick(self):
        self.time += 1

    def update(self, received_time):
        self.time = max(self.time, received_time) + 1

def send_message(sock, message, address):
    try:
        sock.sendto(message.encode(), address)
    except socket.error as e:
        print(f"{RED}Failed to send message to {address}: {e}{RESET}")

def send_message_with_timestamp(sock, message, address, clock):
    clock.tick()
    timestamped_message = f"{message}|{clock.time}|timestamp"
    send_message(sock, timestamped_message, address)

def process_message(message, addr, clock):
    parts = message.split("|")
    if len(parts) == 3 and parts[2] == "timestamp":
        message = parts[0]
        received_time = int(parts[1])
        clock.update(received_time)
        print(f"\n{GREEN}Received message: {message} from {addr}{RESET}")
    else:
        print(f"\n{RED}Invalid message format from {addr}: {message}{RESET}")
