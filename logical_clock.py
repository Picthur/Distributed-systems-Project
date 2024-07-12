# ANSI color escape sequences
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'
BLUE = '\033[94m'

class LogicalClock:
    def __init__(self):
        self.time = 0

    def tick(self):
        self.time += 1

    def update(self, received_time):
        # Check if the received timestamp is valid 
        if not isinstance(received_time, int):
            print(f"{RED}Received invalid timestamp: {received_time}{RESET}")
            return
        self.time = max(self.time, received_time) + 1
