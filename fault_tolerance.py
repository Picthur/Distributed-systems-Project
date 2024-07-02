import socket

# ANSI color escape sequences
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'
BLUE = '\033[94m'

received_message_ids = set()

def send_message_with_id(sock, message, address, message_id):
    message_with_id = f"{message}|{message_id}|id"
    try:
        sock.sendto(message_with_id.encode(), address)
        print(f"{GREEN}Sent message with id to {address[0]}:{address[1]}{RESET}")
    except socket.error as e:
        print(f"{RED}Failed to send message with id to {address}: {e}{RESET}")

def receive_and_deduplicate(message, addr, neighbors):
    try:
        parts = message.split("|")
        if len(parts) == 3 and parts[2] == "id":
            message = parts[0]
            message_id = parts[1]
            if message_id not in received_message_ids:
                received_message_ids.add(message_id)
                print(f"\n{GREEN}Received and processed message: {message} from {addr}{RESET}")
                if message.startswith("meet"):
                    _, neighbor_ip, neighbor_port = message.split()
                    neighbors[neighbor_ip] = int(neighbor_port)
            else:
                print(f"{RED}Duplicate message: {message} from {addr} ignored{RESET}")
    except ValueError as e:
        print(f"{RED}Error processing message from {addr}: {e}{RESET}")
