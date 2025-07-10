import threading
from socket import *
from room import Room  # This should define a Room class with a handle_game method

class TicTacToeServer:
    def __init__(self):
        # Server initialization and socket setup
        self.server_port = 12005
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(('', self.server_port))  # Bind to all available interfaces
        self.server_socket.listen(5)  # Allow up to 5 pending connections
        self.waiting_player = None  # Keep track of a player waiting for a match

        print(f"Server is running, waiting for requests on port {self.server_port}...")

    def start(self):
        # Main server loop: accepts connections and creates threads
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection request from: {client_socket}, address: {client_address}")

            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        # Send welcome message
        client_socket.send(b"Connected to Tic-Tac-Toe server.\n")

        # Match or wait
        if self.waiting_player is None:
            self.waiting_player = client_socket
            client_socket.send(b"Waiting for another player to join...\n")
        else:
            # Pair with the waiting player
            player1_socket = self.waiting_player
            player2_socket = client_socket
            self.waiting_player = None

            player1_socket.send(b"Another player joined! Starting game...\n")
            player2_socket.send(b"Game found! Starting game...\n")

            game_room = Room(player1_socket, player2_socket)
            game_thread = threading.Thread(target=game_room.handle_game)
            game_thread.start()

# Entry point
if __name__ == "__main__":
    server = TicTacToeServer()
    server.start()
