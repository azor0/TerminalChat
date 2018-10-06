import socket
import select 
import sys 
import struct
import time

IP4_ADDR_ANY = '0.0.0.0'

class MulticastSocket(socket.socket):
    def __init__(self, multicast_group, address=IP4_ADDR_ANY):
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        self.mreq = socket.inet_aton(multicast_group) + socket.inet_aton(address)
        self.multicast_group = multicast_group
        self.address = address

        if address != IP4_ADDR_ANY:
            self.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(address))
        
    def join(self):
        self.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, self.mreq)
        print("Joined the multicast network: {} on {}".format(self.multicast_group, self.address))

class Server:
    def __init__(self, multicast_group, port):
        self.sock = MulticastSocket(multicast_group)
        self.sock.bind(('', port))
        self.sock.join()
        self.run()

    def run(self, interval=1):
        while True:
            (segment, (ip4_addr, port)) = self.sock.recvfrom(1024)
            tup = segment.split()
            (seq, time_sent, data) = tup
            delta = time.time() - time_sent
            from_s = "(%s, %d)" % (ip4_addr, port)
            
            print("{} by {} in time {}".format(data, from_s, delta))
            time.sleep(interval)

class Client:
    def __init__(self, multicast_group, address, port):
        self.sock = MulticastSocket(multicast_group, address)
        self.multicast_group = multicast_group
        self.port = port

        if address != IP4_ADDR_ANY:
            self.sock.join() 
        self.sendMessage()

    def sendMessage(self, interval=1):
        while True:
            sent = self.sock.sendto(bytes(input(""), 'utf-8'), (self.multicast_group, self.port))
            time.sleep(interval)


multicast_group = '224.3.29.71'
port = 12345
if len(sys.argv) == 1:
    server = Server(multicast_group, port)
if len(sys.argv) == 2:
    client = Client(multicast_group, str(sys.argv[1]), port)
