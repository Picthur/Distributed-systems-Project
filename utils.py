# utils.py

import socket

def check_available_ports(ip, port_range=range(1000, 1011)):
    available_ports = []
    for port in port_range:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            try:
                s.bind((ip, port))
                available_ports.append(port)
            except OSError:
                continue
    return available_ports
