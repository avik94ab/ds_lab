import _thread
import time
import socket
import struct
import sys

# Define a function for the thread
def receive_multicast():

    multicast_group = '224.3.29.71'
    server_address = ('', 10000)

    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind to the server address
    sock.bind(server_address)

    # Tell the operating system to add the socket to the multicast group
    # on all interfaces.
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        print(sys.stderr, '\nwaiting to receive message')
        data, address = sock.recvfrom(1024)
        print(sys.stderr,'received  bytes from ',len(data), address)
        print(sys.stderr, data)

        print (sys.stderr, 'sending acknowledgement to', address)
        sock.sendto('ack'.encode(), address)

def multicast():
    message = input('Type in the message to send')
    multicast_group = ('224.3.29.71', 10001)
    # Create the datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Set a timeout so the socket does not block indefinitely when trying
    # to receive data.
    sock.settimeout(100000)
    # Set the time-to-live for messages to 1 so they do not go past the
    # local network segment.
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    try:
        # Send data to the multicast group
        print(sys.stderr, 'sending' ,message)
        sent = sock.sendto(message.encode(), multicast_group)
        # Look for responses from all recipients
        while True:
            print(sys.stderr, 'waiting to receive')
            try:
                data, server = sock.recvfrom(16)
            except socket.timeout:
                print(sys.stderr, 'timed out, no more responses')
                break
            else:
                print(sys.stderr, 'received from', (data, server))
    finally:
        print(sys.stderr, 'closing socket')
        sock.close()


# Create two threads as follows
try:
   _thread.start_new_thread(multicast,())
   _thread.start_new_thread(receive_multicast,())

except:
   print ("Error: unable to start thread")

while 1:
   pass
