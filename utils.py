import socket

# ANSI color escape sequences
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'
BLUE = '\033[94m'
DARK_CYAN = '\033[36m'
BOLD = '\033[1;37m'

# Function to get the local IP address
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to a public DNS server to get the local IP address
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    finally:
        s.close()
    return local_ip

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
    print(f"\nUsed ports: {BOLD}{sorted(used_ports)}{RESET}")
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

# Function to process incoming messages from neighbors and update the logical clock
def process_message(message, addr, clock, neighbors):
    parts = message.split("|")
    if len(parts) == 3 and parts[2] == "timestamp":
        message = parts[0]
        try:
            received_time = int(parts[1])
        except ValueError:
            print(f"{RED}Received invalid timestamp: {parts[1]}{RESET}")
            return
        clock.update(received_time)
        if message.startswith("dm-"):
            private_message = message.split("-")[2]
            sender_username = message.split("-")[1]
            print(f"\n{BLUE}Private message [{addr[0]}]{sender_username}:{RESET} {private_message}")
        else:
            sender_username = message.split("-")[0]
            actual_message = "-".join(message.split("-")[1:])
            print(f"\n{DARK_CYAN}[{addr[1]}] {sender_username}:{RESET} {actual_message}")
    else:
        username = neighbors[addr[1]]
        print(f"\n{RED}Invalid message format from {username}:{RESET} {message}")

# Function to initialize a node with a given IP address and port
def init_node(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((ip, port))
    except socket.error as e:
        print(f"{RED}Failed to bind socket: {e}{RESET}")
        raise
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
