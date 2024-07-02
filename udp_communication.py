import socket

def init_node(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    return sock

def send_message(sock, message, address):
    try:
        sock.sendto(message.encode(), address)
    except socket.error as e:
        print(f"\033[91mFailed to send message to {address}: {e}\033[0m")

def listen_for_messages(sock, clock, neighbors, process_message):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = data.decode()
            process_message(message, addr, clock, neighbors)
        except socket.error as e:
            print(f"\033[91mError receiving message: {e}\033[0m")
        except Exception as e:
            print(f"\033[91mUnexpected error: {e}\033[0m")
