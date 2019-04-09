import _thread
import time
import socket
import struct
import sys
import random

VC = [0,0,0,0]
hold_back = []
# Define a function for the thread
def receive_multicast(port):
    global VC
    global hold_back
    multicast_group = '224.3.29.71'
    server_address = ('', port) #listening port

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
        print( '\nwaiting to receive message')
        data, address = sock.recvfrom(1024)
        data = data.decode("utf-8")
        txt = data.split(":")
        data = ":".join(txt[2:])
        s = txt[1]
        s = s[1:-1]
        s = s.split(",")
        for i in range(len(s)):
            s[i] = int(s[i])
        p = int(txt[0])
        for i in range(4):
            if s[i] > VC[i]:
                VC[i] = s[i]
        print("VC:",VC)
        print("s:",s)
        #print( data)
        hold_back.append((s,p,data))
        hold_back = sorted (hold_back, key = lambda x:x[0])
        for i in hold_back:
            flag = 0
            k = [10001,10002,10003,10004]
            k.remove(i[1])
            for j in k:
                if i[0][j-10001] > VC[j-10001]:
                    flag = 1
            if (i[0][i[1]-10001] == VC[i[1]-10001]+1) and flag == 0:
                print ('received  bytes from ',i[2],address)
                VC[i[1]-10001]= VC[i[1]-10001]+1

        '''
        if (s == R[p]+1):
            print('received  bytes from ',data, address)
            R[p] += 1
            #print ( 'sending acknowledgement to', address)
            hold_back = sorted (hold_back, key = lambda x:x[0])
            #print ("-------->",hold_back)
            counter = R[p] +1
            list = []
            for i in hold_back:
                if i[0] == counter:
                    print('received  bytes from ',i[1],address)
                    list.append(i)
                    R[p] += 1
                    counter += 1
            for j in list:
                hold_back.remove(j)

            sock.sendto('ack'.encode(), address)
        elif s <= R[p]:
            print("message is discarded!")
        elif s > R[p] +1:
            hold_back.append((s,data))
            #print ("loook at this!:",hold_back)
'''


def delay_multicast(sock,message, multicast_group):
    print('Sleep start')
    v = random.randint(2,10)
    print(v)
    time.sleep(v)
    sent = sock.sendto(message.encode(), multicast_group)


def multicast(port):
    global VC
    #s = [0,0,0,0]
    # Create the datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Set a timeout so the socket does not block indefinitely when trying
    # to receive data.
    sock.settimeout(0.2)
    # Set the time-to-live for messages to 1 so they do not go past the
    # local network segment.
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    try:
        while True:
            message = input('Type in the message to send')
            #s[port - 10001]+=1
            VC[port-10001] +=1
            for p in [10001,10002,10003,10004]:
                if p !=port:
                    multicast_group = ('224.3.29.71', p)
                    # Send data to the multicast group
                    print( 'sending' ,message)
                    _thread.start_new_thread(delay_multicast,(sock,str(port)+":"+str(VC)+":"+message,multicast_group))


            print('The sequence no. is:',VC[port-10001])
            # Look for responses from all recipients
            while True:
                print( 'waiting to receive')
                try:
                    data, server = sock.recvfrom(16)
                except socket.timeout:
                    print('timed out, no more responses')
                    break
                else:
                    print( 'received from', (data, server))
    finally:
        print( 'closing socket')
        sock.close()

if __name__== "__main__":

    port = int(sys.argv[1]) # listening port

    # Create two threads as follows
    _thread.start_new_thread(multicast,(port,))
    receive_multicast(port)




    while 1:
       pass
