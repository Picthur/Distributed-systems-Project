# chat_node.py

import socket
from threading import Thread
import uuid
from logical_clock import *
from fault_tolerance import *

# ANSI color escape sequences
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'
BLUE = '\033[94m'

def init_node(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    return sock


def listen_for_messages(sock, clock, neighbors):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = data.decode()
            process_message(message, addr, clock, neighbors)
            receive_and_deduplicate(message, addr, neighbors)
        except socket.error as e:
            print(f"{RED}Error receiving message: {e}{RESET}")
        except Exception as e:
            print(f"{RED}Unexpected error: {e}{RESET}")

if __name__ == "__main__":
    ip_address = "localhost".strip()
    port = int(input("Enter your port: ").strip())
    node_address = (ip_address, port)
    
    sock = init_node(ip_address, port)
    clock = LogicalClock()

    neighbors = {} 

    Thread(target=listen_for_messages, args=(sock, clock, neighbors), daemon=True).start()
    
    while True:
        print("\nCurrent Neighbors:")
        for neighbor_addr, neighbor_id in neighbors.items():
            print(f"{neighbor_id}: {neighbor_addr[0]}:{neighbor_addr[1]}")
        
        print("\nCommands: meet <ip> <port>, broadcast <message>, dm")
        user_input = input("Enter command: ").strip()
        
        ############## Meet Neighbor ############## 
        if user_input.startswith("meet"):
            _, neighbor_ip, neighbor_port = user_input.split()
            neighbor_address = (neighbor_ip, int(neighbor_port))
            neighbor_id = uuid.uuid4().hex
            neighbors[neighbor_address] = neighbor_id
            message = f"meet|{ip_address}|{port}"
            send_message(sock, message, neighbor_address)
            print(f"\n{GREEN}Met neighbor at {neighbor_ip}:{neighbor_port} with id {neighbor_id}{RESET}")
        
        ############## Broadcast ##############
        elif user_input.startswith("broadcast"):
            if not neighbors:
                print(f"{RED}No neighbors to broadcast message to.{RESET}")
                continue
            
            message = user_input[len("broadcast "):].strip()
            if message:
                for neighbor_addr in neighbors:
                    send_message_with_timestamp(sock, message, neighbor_addr, clock)
                print(f"\n{GREEN}Broadcasted message '{message}' to all neighbors.{RESET}")
            else:
                print(f"{RED}Please provide a message to broadcast.{RESET}")
        
        ############## Direct Message ##############
        elif user_input.startswith("dm"):
            if not neighbors:
                print(f"{RED}No neighbors to send message to.{RESET}")
                continue
            
            print("\nChoose a neighbor to send a message to:")
            for idx, neighbor_addr in enumerate(neighbors.keys(), start=1):
                print(f"{BLUE}{idx}{RESET}. {neighbor_addr[0]}:{neighbor_addr[1]}")
            
            choice = input("\nEnter the number of the neighbor: ").strip()
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(neighbors):
                    neighbor_addr = list(neighbors.keys())[choice - 1]
                    message = input("Enter your message: ").strip()
                    if message:
                        msgSend = f"dm|{message}"
                        send_message_with_timestamp(sock, msgSend, neighbor_addr, clock)
                        print(f"\n{GREEN}Sent message '{message}' to {neighbor_addr[0]}:{neighbor_addr[1]}{RESET}")
                    else:
                        print(f"{RED}Please enter a non-empty message.{RESET}")
                else:
                    print(f"{RED}Invalid neighbor number.{RESET}")
            else:
                print(f"{RED}Invalid input. Please enter a number.{RESET}")
        
        ############## Invalid Command ##############
        else:
            print(f"{RED}Invalid command. Please enter 'meet', 'broadcast', or 'dm'.{RESET}")
