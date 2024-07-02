from fault_tolerance import send_message

class LogicalClock:
    def __init__(self):
        self.time = 0

    def tick(self):
        self.time += 1

    def update(self, received_time):
        self.time = max(self.time, received_time) + 1

def send_message_with_timestamp(sock, message, address, clock):
    clock.tick()
    timestamped_message = f"{message}|{clock.time}"
    send_message(sock, timestamped_message, address)

def process_message(message, clock):
    message, received_time = message.split("|")
    received_time = int(received_time)
    clock.update(received_time)
    return message, clock.time
