import threading
import sys
from udp_communication import init_node, broadcast_message, listen_for_messages
from logical_clock import LogicalClock, send_message_with_timestamp, process_message
from fault_tolerance import send_message_with_id, receive_and_deduplicate

if __name__ == "__main__":
    port = int(sys.argv[1])
    node_address = ("localhost", port)
    
    # Known addresses of other nodes (adjust as needed)
    other_addresses = [("localhost", 12346), ("localhost", 12347)]

    sock = init_node(port)
    clock = LogicalClock()

    threading.Thread(target=listen_for_messages, args=(sock, lambda msg, addr: receive_and_deduplicate(msg, addr))).start()
    
    while True:
        message = input("Enter message to broadcast: ")
        message_id = f"msg-{clock.time}"
        for address in other_addresses:
            send_message_with_id(sock, message, address, message_id)
            send_message_with_timestamp(sock, message, address, clock)
