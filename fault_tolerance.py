from udp_communication import send_message

received_message_ids = set()

def send_message_with_id(sock, message, address, message_id):
    message_with_id = f"{message}|{message_id}|id"
    send_message(sock, message_with_id, address)

def receive_and_deduplicate(message, addr, neighbors):
    try:
        parts = message.split("|")
        if len(parts) == 3 and parts[2] == "id":
            message = parts[0]
            message_id = parts[1]
            if message_id not in received_message_ids:
                received_message_ids.add(message_id)
                print(f"\nReceived and processed message: {message} from {addr}\033[0m")
                if message.startswith("meet"):
                    _, neighbor_ip, neighbor_port = message.split()
                    neighbors[neighbor_ip] = int(neighbor_port)
            else:
                print(f"\033[91mDuplicate message: {message} from {addr} ignored\033[0m")
        else:
            print(f"\033[91mInvalid message format from {addr}: {message}\033[0m")
    except ValueError as e:
        print(f"\033[91mError processing message from {addr}: {e}\033[0m")
