from socket import *

def start_client():
    serverAddress = 'localhost'  # Server IP (localhost here)
    serverPort = 12005           # Server port

    clientSocket = socket(AF_INET, SOCK_STREAM)  # TCP socket
    clientSocket.connect((serverAddress, serverPort))

    try:
        while True:
            # Receive message from server (board state, prompts, results)
            modifiedMessage = clientSocket.recv(1024).decode("utf-8")

            if not modifiedMessage:
                print("Disconnected from server.")
                break  # Exit loop if server closes connection

            print(modifiedMessage)  # Display the server message

            # If game over or disconnected, close and exit
            if ("wins" in modifiedMessage or
                "draw" in modifiedMessage or
                "disconnected" in modifiedMessage):
                break

            # Prompt player for move only if it's their turn
            if "Your move" in modifiedMessage:
                message = input("Enter a position (1-9):\n").strip()
                clientSocket.send(message.encode())

    except KeyboardInterrupt:
        print("\nClient exited by user.")

    finally:
        clientSocket.close()

if __name__ == "__main__":
    start_client()
