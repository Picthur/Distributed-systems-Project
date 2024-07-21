# UDP-based Chat Project

This project implements a distributed chat system using the User Datagram Protocol (UDP). It allows up to 10 users to connect and exchange messages efficiently and quickly over a local network.

## Features

- **Connection and Disconnection:**
  Users can join the chat using one of the available ports between 1000 and 1010 on `localhost`.

- **Sending Messages:**
  - **Broadcast:**
    A user can send a message that will be received by all other connected users.
  - **Private Messages:**
    Users can send private messages to another user by specifying the destination port in the message (format: `@<port> <message>`).

- **Logical Clock Management:**
  Each message is accompanied by a timestamp based on a logical clock, allowing for causal message ordering.

- **Console Interface:**
  Interaction with the chat is primarily through a command-line interface.

## Installation

1. **Prerequisites:**
   - Python 3.x installed on your system.

2. **Cloning the Repository:**
   ```
   git clone https://github.com/Picthur/Distributed-systems-Project.git
   ```


## Usage

1. **Starting the Server:**
   - Launch the server by running `python chat_node.py` in a terminal. It will automatically choose an available port and start listening for incoming messages.

2. **Connecting Clients:**
   - Execute `python chat_node.py` in other terminals to simulate different clients connecting to the server.

3. **Sending Messages:**
   - In each client terminal, enter a message and press Enter to send it.
   - Use `@<port> <message>` to send a private message to another user.
