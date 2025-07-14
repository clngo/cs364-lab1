from socket import *

def start_client():
    '''
    Configure client
    '''
    serverAddress = 'localhost' # Server hostname / IP address
    serverPort = 12005 # Must match server's listening port

    # Create TCP client socket
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # Connect to server
    clientSocket.connect((serverAddress, serverPort))

    try:
        '''
        Initial interaction w/ server
        '''
        # Receive & display prompt welcome messsage from server
        welcome = clientSocket.recv(1024).decode("utf-8")
        print(welcome)

        # Receive & display prompt to enter player name
        prompt = clientSocket.recv(1024).decode("utf-8")
        print(prompt)

        # Input player name, add newline, send to server
        player_name = input().strip() + "\n"
        clientSocket.sendall(player_name.encode("utf-8"))

        '''
        Wait for server response about matchmaking 
        '''
        # Receive & display waiting messge 
        message = clientSocket.recv(1024).decode("utf-8")
        print(message)

        # If waiting, wait for server to confirm matched
        if "Waiting" in message:
            update = clientSocket.recv(1024).decode("utf-8")
            if update:
                print(update)

        '''
        Main game loop
        '''
        # Keep receiving & handling server messages until game ends or client exits
        while True:
            msg = clientSocket.recv(1024).decode("utf-8")
            if not msg:
                # If connection closed by server, exit loop
                print("Server disconnected.")
                break
            print(msg)

            # If it is the player's turn to move, prompt for input & send move
            if "Your move" in msg:
                move = input("Enter a position (1-9):\n").strip()
                clientSocket.sendall(move.encode("utf-8"))

            # If game is over & player is asked to play again, handle input
            elif "Play again?" in msg:
                choice = input("(yes/exit): ").strip().lower()
                clientSocket.sendall(choice.encode("utf-8"))
                if choice == "exit":
                    print("Bye!")
                    break

    except KeyboardInterrupt:
        # Handle Ctrl+C from user
        print("\nClosed by user.")
    finally:
        # Always close socket
        clientSocket.close()

if __name__ == "__main__":
    # Entry point: start client 
    start_client()
