import socket

def init_node(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", port))
    return sock

def send_message(sock, message, address):
    sock.sendto(message.encode(), address)

def broadcast_message(sock, message, addresses):
    for address in addresses:
        send_message(sock, message, address)

def listen_for_messages(sock, process_message_func):
    while True:
        data, addr = sock.recvfrom(1024)
        process_message_func(data.decode(), addr)
