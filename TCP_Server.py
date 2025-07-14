import threading
from socket import *
from room import Room # This should define a Room class with a handle_game method

class TicTacToeServer:
    def __init__(self):
        # Server initialization and socket setup
        self.server_port = 12005 # Port number for clients to connect to 
        self.server_socket = socket(AF_INET, SOCK_STREAM) # Create TCP socket
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Allow address reuse
        self.server_socket.bind(('', self.server_port)) # Bind to all available interfaces
        self.server_socket.listen(5) # Allow up to 5 pending connections
        self.waiting_players = [] # Queue of players waiting to be matched
        print(f"Server is running on port {self.server_port}...")

    def start(self):
        '''
        Starts the server: begins matchmaker thread & accepts incoming client connections
        Each client connection is handled in separate threads
        '''
        threading.Thread(target=self.matchmaker).start() # Start separatte thread for matchmaker to pair waiting players

        # Accept new client connections continuously 
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection request from {client_address}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start() # Create new thread to handle each client independently

    def recv_line(self, sock):
        '''
        Receives line of text from given socket until a newline is encountered
        Decodes bytes to UTF-8 string & strips whitespace
        '''
        data = b""
        while True:
            chunk = sock.recv(1) # Receive one byte @ a time
            if not chunk or chunk == b"\n": # Stop @ newline or connection closed
                break
            data += chunk
        return data.decode("utf-8").strip()

    def handle_client(self, client_socket):
        '''
        Handles individual client's connection:
        - Sends greeting & asks for player name
        - Adds player to waiting queue
        - Tells player they are waiting for match 
        '''
        try:
            client_socket.send(b"Connected to Tic-Tac-Toe server!\n")
            client_socket.send(b"Enter your player name:\n")
            player_name = self.recv_line(client_socket)
            print(f"Player joined: {player_name}")

            # Add this player to queue, server will match them
            self.waiting_players.append((client_socket, player_name))
            client_socket.send(b"Waiting for another player to join...\n")

        except Exception as e:
            # Handle exceptions & close the socket if needed
            print(f"Error: {e}")
            client_socket.close()

    def matchmaker(self):
        '''
        Continuously checks for 2 players in waiting queue
        When 2 players are available, start a new room for them in separate thread
        '''
        while True:
            if len(self.waiting_players) >= 2:
                # Pop 2 players from waiting queue
                player1_socket, player1_name = self.waiting_players.pop(0)
                player2_socket, player2_name = self.waiting_players.pop(0)

                # Tell both players they have matched
                player1_socket.send(
                    f"Player {player2_name} joined! Starting game...\n".encode("utf-8")
                )
                player2_socket.send(
                    f"Matched with player {player1_name}! Starting game...\n".encode("utf-8")
                )

                # Create new room to handle their game session in separate thread
                room = Room(player1_socket, player1_name, player2_socket, player2_name, self)
                threading.Thread(target=room.handle_game).start()

if __name__ == "__main__":
    # Entry point: create TicTacToe server instance & starts it 
    server = TicTacToeServer()
    server.start()
