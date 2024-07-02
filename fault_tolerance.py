import socket

def send_message(sock, message, address):
    sock.sendto(message.encode(), address)

received_message_ids = set()

def send_message_with_id(sock, message, address, message_id):
    message_with_id = f"{message}|{message_id}"
    send_message(sock, message_with_id, address)

def receive_and_deduplicate(message, addr):
    message, message_id = message.split("|")
    if message_id not in received_message_ids:
        received_message_ids.add(message_id)
        print(f"Received and processed message: {message} from {addr}")
    else:
        print(f"Duplicate message: {message} from {addr} ignored")
