import socket
import threading

def server():

    serverSocket = socket.socket()

    serverSocket.bind(('', 1234))

    serverSocket.listen(5)

    print("[*] Initializing sockets..........Done!")
    print("[*] Sockets bound successfully........!")

    while True: 

        #accept connections from client/browser
        clientSocket, addr = serverSocket.accept()
        print(f'[*] Receiving connection from {addr}')

        #collect the data of the client
        data = clientSocket.recv(1024).decode('utf-8')

        t = threading.Thread(target=client_data, args=(clientSocket, data))
        t.start()

        #close the socket
        serverSocket.close()

def client_data(clientSocket, data):

    request = data.split('\n')[1]

    port = 80

    http_pos = request.find("://")

    if (http_pos == -1):

        req = request.find(":")
        
        host = (request[(req+1):]).strip()

    else:

        host = (request[(http_pos+3):]).strip()




    # request = data.split('\n')[0]

    # req = request.split('')[1]

    # http_pos = req.find("://")

    # if(http_pos == -1):
    #     url = req
    # else:
    #     url = req[(http_pos+3):]
    
    # port_pos = url.find(':')

    # webserver_pos = url.find('/')

    # if webserver_pos == -1:
    #     webserver_pos = len(url)

    # host = ""

    # port = -1

    # if (port_pos == -1 or webserver_pos < port_pos):
    #     port = 80
    #     host = url[:webserver_pos]
    # else:
    #     port = int((url[(port_pos+1):])[:webserver_pos - port_pos - 1])
    #     host = url[:port_pos]

    proxy(clientSocket, host, port, data)

def proxy(clientSocket, host, port, data):

    c = socket.socket()

    #connecting to the remote server
    c.connect((host, port))


    #send the request to the remote server
    c.send(data).encode()
    print('[*] Data sent to server.....!')

    while True:

        #Receiving data from remote server
        msg = c.recv(1024).decode('utf-8')

        #sending data to the client/browser
        clientSocket.send(msg)
    
        #close socket
        c.close()
