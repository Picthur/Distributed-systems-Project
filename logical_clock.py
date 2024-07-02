import uuid
class LogicalClock:
    def __init__(self):
        self.time = 0

    def tick(self):
        self.time += 1

    def update(self, received_time):
        self.time = max(self.time, received_time) + 1

def send_message_with_timestamp(sock, message, address, clock):
    clock.tick()
    timestamped_message = f"{message}|{clock.time}|timestamp"
    from udp_communication import send_message
    send_message(sock, timestamped_message, address)

def process_message(message, addr, clock, neighbors):
    parts = message.split("|")
    if len(parts) == 3 and parts[2] == "timestamp":
        message = parts[0]
        received_time = int(parts[1])
        clock.update(received_time)
        print(f"\n\033[92mReceived message: {message} from {addr}\033[0m")
    if len(parts) == 3 and parts[0] == "meet":
        # need to print "You are connected to neighbor at {neighbor_ip}:{neighbor_port}"
        _, neighbor_ip, neighbor_port = parts
        neighbor_address = (neighbor_ip, int(neighbor_port))
        neighbor_id = uuid.uuid4().hex
        neighbors[neighbor_id] = neighbor_address
        print(f"\n\n\033[92mYou are connected to neighbor at {neighbor_ip}:{neighbor_port}\033[0m")
    else:
        print(f"\n\033[91mInvalid message format from {addr}: {message}\033[0m")
