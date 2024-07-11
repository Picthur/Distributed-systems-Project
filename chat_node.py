import socket
from threading import Thread
from logical_clock import LogicalClock
from utils import *

# ANSI color escape sequences for colored console output
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def main():
    # Configuration de l'adresse IP locale
    ip_address = "localhost"
    
    # Vérification des ports disponibles sur l'adresse IP locale
    available_ports = check_available_ports(ip_address)
    if not available_ports:
        print(f"{RED}No available ports. Exiting...{RESET}")
        exit(1)

    # Choix du premier port disponible
    port = available_ports[0]
    print(f"Assigned port: {port}")

    # Initialisation du socket pour ce nœud
    sock = init_node(ip_address, port)

    # Initialisation de l'horloge logique pour ce nœud
    clock = LogicalClock()

    # Initialisation du dictionnaire des voisins connectés
    neighbors = {}

    # Démarrage du thread d'écoute des messages entrants en arrière-plan
    Thread(target=listen_for_messages, args=(sock, clock, neighbors), daemon=True).start()

    while True:
        # Lecture du message à envoyer depuis l'utilisateur
        message = input("Enter message: ")

        if message.startswith("@"):
            ############## PRIVATE MESSAGE ##############
            try:
                # Extraction du port cible du message privé
                target_port = int(message.split()[0][1:])
                # Extraction du message privé à envoyer
                private_message = " ".join(message.split()[1:])
                neighbor_addr = (ip_address, target_port)
                used_ports = get_used_ports(ip_address)
                if target_port in used_ports:
                    # Envoi du message privé avec horodatage à l'adresse du voisin cible
                    target_addr = (ip_address, target_port)
                    send_message_with_timestamp(sock, f"dm-{private_message}", target_addr, clock)
                    print(f"\n{GREEN}Sent private message '{private_message}' to {ip_address}:{target_port}{RESET}")
                else:
                    # Affichage d'une erreur si le port cible n'est pas un voisin connecté
                    print(f"{RED}Port {target_port} is not a connected neighbor.{RESET}")
            except ValueError:
                # Affichage d'une erreur si le format du port est incorrect
                print(f"{RED}Invalid port specified.{RESET}")
        else:
            ############## BROADCAST MESSAGE ############
            used_ports = get_used_ports(ip_address)
            for neighbor_port in used_ports:
                neighbor_addr = (ip_address, neighbor_port)
                try:
                    # Envoi du message broadcast avec horodatage à tous les voisins connectés
                    send_message_with_timestamp(sock, message, neighbor_addr, clock)
                except socket.error as e:
                    # Affichage d'une erreur si l'envoi du message a échoué
                    print(f"{RED}Failed to send message to {neighbor_addr}: {e}{RESET}")
            print(f"\n{GREEN}Broadcasted message '{message}' to all neighbors.{RESET}")

if __name__ == "__main__":
    main()
