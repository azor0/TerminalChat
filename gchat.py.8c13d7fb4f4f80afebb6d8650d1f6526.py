import socket
import sys
import threading

IP4_ADDR = '0.0.0.0'
port = 12345


class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []

    def __init__(self, port):
        self.sock.bind((IP4_ADDR, port))
        self.sock.listen(1)

    def handler(self, c, a):
        while True:
            data = c.recv(2048)
            (adress, port) = a
            for connection in self.connections:
                if connection != c:
                    try:
                        message = str.encode("{} by {}, {}".format(
                            data.decode("utf-8"), adress, port))
                        print(message)
                        connection.send(message)
                    except:
                        connection.close()
                        self.remove(c)
            if not data:
                break

    def run(self):
        while True:
            conn, adressInfo = self.sock.accept()
            cThread = threading.Thread(
                target=self.handler, args=(conn, adressInfo))
            cThread.daemon = True
            cThread.start()
            self.connections.append(conn)
            print(self.connections)

    def remove(self, connection):
        if connection in self.connections:
            self.connections.remove(connection)


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, address, port):
        self.sock.connect((address, port))
        iThread = threading.Thread(target=self.sendMessage)
        iThread.daemon = True
        iThread.start()

        while True:
            data = self.sock.recv(2048)
            if not data:
                break
            print(data.decode())

    def sendMessage(self):
        while True:
            self.sock.send(
                bytes(input(""), 'utf-8'))


if len(sys.argv) == 1:
    server = Server(port)
    server.run()
if len(sys.argv) == 2:
    client = Client(str(sys.argv[1]), port)
