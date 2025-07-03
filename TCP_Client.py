

from socket import * 
serverAddress = 'localhost' #127.0.0.0
serverPort = 12005

clientSocket = socket(AF_INET, SOCK_STREAM) #AF_INET is IP; SOCK_STREAM is TCP
clientSocket.connect((serverAddress, serverPort))
message = input("Enter a position (0-8)\n")

clientSocket.send(message.encode())
modifiedMessage, address = clientSocket.recvfrom(2048)

print(modifiedMessage.decode())


def tictactoe():
    