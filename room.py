from board import Board 

class Room:
    def __init__(self, player1_socket, player2_socket):
        self.board = Board()
        self.players = [(player1_socket, "X"), (player2_socket, "O")]
        self.current_player = 0  # Index of current player (0 or 1)

    def send_to_player(self, player_socket, message):
        try:
            player_socket.send(message.encode("utf-8"))
        except:
            print("Failed to send to player.")

    def send_board_to_players(self):
        board_state = self.board.display()
        for player_socket, _ in self.players:
            self.send_to_player(player_socket, board_state)

    def handle_game(self):
        game_over = False
        while not game_over:
            current_socket, current_marker = self.players[self.current_player]
            opponent_socket, _ = self.players[(self.current_player + 1) % 2]

            # Send updated board to both players
            self.send_board_to_players()

            # Prompt current player for move
            self.send_to_player(current_socket, "\nYour move (1-9): ")

            try:
                move = current_socket.recv(1024).decode("utf-8").strip()
            except:
                self.send_to_player(opponent_socket, "Opponent disconnected.\n")
                current_socket.close()
                opponent_socket.close()
                return

            if move.isdigit() and int(move) in range(1, 10):
                move = int(move) - 1  # Convert 1-9 to 0-8 index
                if self.board.board[move] not in ["X", "O"]:
                    self.board.update(move, current_marker)

                    if self.board.is_winner(current_marker):
                        self.send_board_to_players()
                        self.send_to_player(current_socket, f"\nYou win!\n")
                        self.send_to_player(opponent_socket, f"\nPlayer {current_marker} wins!\n")
                        game_over = True
                    elif self.board.is_draw():
                        self.send_board_to_players()
                        for sock, _ in self.players:
                            self.send_to_player(sock, "\nIt's a draw!\n")
                        game_over = True
                    else:
                        self.current_player = (self.current_player + 1) % 2
                else:
                    self.send_to_player(current_socket, "Invalid move: spot taken. Try again.\n")
            else:
                self.send_to_player(current_socket, "Invalid input. Enter a number 1-9.\n")

        for sock, _ in self.players:
            sock.close()
