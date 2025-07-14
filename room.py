from board import Board 
from scoreboard import update_scoreboard, get_scoreboard

class Room:
    '''
    Represents single TicTacToe game room for 2 players
    Handles game state, player turns, win/draw detection, score updates
    '''
    def __init__(self, player1_socket, player1_name, player2_socket, player2_name, server):
        # Initializes fresh board for game
        self.board = Board()

        # Store player info as tuples: (socket, name, marker)
        self.players = [
            (player1_socket, player1_name, "X"),
            (player2_socket, player2_name, "O")
        ]

        # Keep track of whose turn it is
        self.current_player = 0

        # Reference server to re-add players to waiting list if needed
        self.server = server  

    def send_to_player(self, sock, message):
        '''
        Sends string message to specific player socket
        Uses UTF-8 encoding
        '''
        try:
            sock.send(message.encode("utf-8"))
        except:
            pass # If sending fails, ignore to keep server stable

    def send_board(self):
        '''
        Sends current state of board to both players
        Uses board's display()
        '''
        state = self.board.display()
        for sock, _, _ in self.players:
            self.send_to_player(sock, state)

    def handle_game(self):
        '''
        Core game loop:
        Alternates player turns, validates moves, check for win/draw, updates scoreboard, handles replay logic
        '''
        game_over = False

        while not game_over:
            # Get current player & opponent
            csock, cname, marker = self.players[self.current_player]
            osock, oname, _ = self.players[(self.current_player + 1) % 2]

            # Show board to both players
            self.send_board()

            # Prompt current player ot make move, tell opponent to wait
            self.send_to_player(csock, f"\nYour move, {cname} ({marker}): ")
            self.send_to_player(osock, f"\nWaiting for {cname} to make a move...\n")

            # Receive move from player 
            try:
                move = csock.recv(1024).decode("utf-8").strip()
            except:
                # If player disconnects mid-game, tell opponent & close connections
                self.send_to_player(osock, "Opponent disconnected.\n")
                csock.close()
                osock.close()
                return

            # Validate move: must be 1-9 & empty spot
            if move.isdigit() and int(move) in range(1, 10):
                idx = int(move) - 1
                if self.board.board[idx] not in ["X", "O"]:
                    # Valid move: update board
                    self.board.update(idx, marker)

                    # Check if current player won
                    if self.board.is_winner(marker):
                        self.send_board()
                        self.send_to_player(csock, f"\nYou win, {cname}!\n")
                        self.send_to_player(osock, f"\n{cname} wins!\n")
                        update_scoreboard(winner_name=cname, player_names=[cname, oname])
                        self.print_server_scores()
                        game_over = True
                    
                    # Check if game is a draw
                    elif self.board.is_draw():
                        self.send_board()
                        for sock, _, _ in self.players:
                            self.send_to_player(sock, "\nIt's a draw!\n")
                        update_scoreboard(draw=True, player_names=[cname, oname])
                        self.print_server_scores()
                        game_over = True
                    
                    # Switch to next player
                    else:
                        self.current_player = (self.current_player + 1) % 2
                else:
                    self.send_to_player(csock, "Invalid move: spot taken.\n")
            else:
                self.send_to_player(csock, "Invalid input. Use 1-9.\n")

        # Game is over: show final score
        scores = get_scoreboard()
        for sock, name, _ in self.players:
            self.send_to_player(sock, f"Your total score: {scores.get(name, 0)}\n")

        # Ask both players if they want to play again
        for sock, _, _ in self.players:
            self.send_to_player(sock, "Play again? (yes/exit): ")

        for sock, name, _ in self.players:
            answer = sock.recv(1024).decode("utf-8").strip().lower()
            if answer == "yes":
                print(f"{name} wants to play again.")
                try:
                    sock.send(b"Waiting for another player to join...\n")
                except:
                    pass
                # Add player back to server's waiting queue
                self.server.waiting_players.append((sock, name))
            else:
                print(f"{name} exited.")
                sock.close()

    def print_server_scores(self):
        '''
        Prints current scoreboard to server
        Sorted by score in descending order
        '''
        scores = get_scoreboard()
        print("\n=== Scoreboard ===")
        for name, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            print(f"{name}: {score}")
        print("==========================\n")
