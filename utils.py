import socket

# ANSI color escape sequences
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'
BLUE = '\033[94m'


# Function to check available ports on a given IP address
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
    print(f"\nUsed ports: {sorted(used_ports)}")
    return available_ports


# Function to get the used ports on a given IP address
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


# Function to send a message to a specific neighbor 
def send_message(sock, message, address):
    try:
        sock.sendto(message.encode(), address)
    except socket.error as e:
        print(f"{RED}Failed to send message to {address}: {e}{RESET}")


# Function to send a message with a timestamp to a specific neighbor 
def send_message_with_timestamp(sock, message, address, clock):
    clock.tick()
    timestamped_message = f"{message}|{clock.time}|timestamp"
    send_message(sock, timestamped_message, address)
    print(f"Sent message '{message}' to {address[0]}:{address[1]}")


# Function to process incoming messages from neighbors and update the logical clock
def process_message(message, addr, clock):
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


# Function to initialize a node with a given IP address and port
def init_node(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    return sock


# Function to listen for incoming messages from neighbors
def listen_for_messages(sock, clock, neighbors):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = data.decode()
            process_message(message, addr, clock, neighbors)
        except socket.error as e:
            if e.errno != 10054:
                print(f"{RED}Error receiving message: {e}{RESET}")

