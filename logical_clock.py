import uuid
import socket

# ANSI color escape sequences
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'
BLUE = '\033[94m'

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


def process_message(message, addr, clock, neighbors):
    parts = message.split("|")
    print("parts: ", parts)
    if len(parts) == 3 and parts[2] == "timestamp":
        message = parts[0]
        received_time = int(parts[1])
        clock.update(received_time)
        print(f"\n{GREEN}Received message: {message} from {addr}{RESET}")

    elif len(parts) == 3 and parts[0] == "meet":
        _, neighbor_ip, neighbor_port = parts
        neighbor_address = (neighbor_ip, int(neighbor_port))
        neighbor_id = uuid.uuid4().hex
        neighbors[neighbor_address] = neighbor_id
        print(f"\n\n{GREEN}You are connected to neighbor at {neighbor_ip}:{neighbor_port}{RESET}")

    elif len(parts) == 3 and parts[0] == "dm":
        message = parts[1]
        # you recived a dm message from a neighbor 
        _, neighbor_ip, neighbor_port = parts
        neighbor_address = (neighbor_ip, int(neighbor_port))
        received_time = int(parts[2])
        clock.update(received_time)
        print(f"\n\n{GREEN}DM message from {neighbor_ip}:{neighbor_port} : {message}{RESET}")
    else:
        print(f"\n{RED}Invalid message format from {addr}: {message}{RESET}")
