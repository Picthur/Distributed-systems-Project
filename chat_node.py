import socket
from threading import Thread
from logical_clock import LogicalClock
from utils import *

# ANSI color escape sequences for colored console output
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1;37m'

def main():
    # Configuration of the local IP address
    ip_address = "localhost"
    
    # Check available ports on the local IP address
    available_ports = check_available_ports(ip_address)
    if not available_ports:
        print(f"{RED}No available ports. Exiting...{RESET}")
        exit(1)

    # Choose the first available port and username
    port = available_ports[0]
    print(f"Assigned port: {port}")
    
    # Initialize the socket for this node
    sock = init_node(ip_address, port)

    # Initialize the logical clock for this node
    clock = LogicalClock()

    # Initialize the dictionary of connected neighbors
    neighbors = {}

    # Start the background thread to listen for incoming messages
    Thread(target=listen_for_messages, args=(sock, clock, neighbors), daemon=True).start()

    while True:
        # Read the message to be sent from the user
        message = input(f"\n{BOLD}Enter message:{RESET} ")

        if message.startswith("@"):
            ############## PRIVATE MESSAGE ##############
            try:
                # Extract the target port for the private message
                target_port = int(message.split()[0][1:])
                # Extract the private message to be sent
                private_message = " ".join(message.split()[1:])
                neighbor_addr = (ip_address, target_port)
                used_ports = get_used_ports(ip_address)
                if target_port in used_ports:
                    # Send the private message with a timestamp to the target neighbor address
                    target_addr = (ip_address, target_port)
                    send_message_with_timestamp(sock, f"dm-{private_message}", target_addr, clock)
                    print(f"{GREEN}Sent private message '{private_message}' to {ip_address}:{target_port}{RESET}")
                else:
                    # Display an error if the target port is not a connected neighbor
                    print(f"{RED}Port {target_port} is not a connected neighbor.{RESET}")
            except ValueError:
                # Display an error if the port format is incorrect
                print(f"{RED}Invalid port specified.{RESET}")
        else:
            ############## BROADCAST MESSAGE ############
            used_ports = get_used_ports(ip_address)
            for neighbor_port in used_ports:
                if neighbor_port != port:
                    neighbor_addr = (ip_address, neighbor_port)
                    try:
                        # Send the broadcast message with a timestamp to all connected neighbors
                        send_message_with_timestamp(sock, message, neighbor_addr, clock)
                    except socket.error as e:
                        # Display an error if sending the message failed
                        print(f"{RED}Failed to send message to {neighbor_addr}: {e}{RESET}")
            print(f"{GREEN}Broadcasted message '{message}' to all neighbors.{RESET}")

if __name__ == "__main__":
    main()
