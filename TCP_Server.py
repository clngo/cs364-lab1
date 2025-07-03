from socket import *

serverPort = 12005
serverSocket = socket(AF_INET, SOCK_STREAM) # change from SOCK_DGRAM 
serverSocket.bind(('', serverPort))
# new
serverSocket.listen(1)
print("Server is running, waiting for requests...")

while True:
    # first check if there's a connection
    clientSocket, clientAddress = serverSocket.accept()
    print(f"Connection requst from: {clientSocket}, address is: {clientAddress}")
    
    message = clientSocket.recv(2048)
    print(f"Received: {message} from: {clientSocket}")

    modifiedMessage = message.decode().upper()
    clientSocket.send(modifiedMessage.encode())