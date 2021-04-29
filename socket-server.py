# load additional Python module
import socket
import csv
from utils import USV
import time

usv=USV()
PORT = 23456
FILE_PATH = "events.csv"

# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# retrieve local hostname
local_hostname = socket.gethostname()

# get fully qualified hostname
local_fqdn = socket.getfqdn()

# get the according IP address
ip_address = socket.gethostbyname(local_hostname)

# output hostname, domain name and IP address
print ("working on %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))

# bind the socket to the port 23456
server_address = (ip_address, PORT)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# listen for incoming connections (server mode) with one connection at a time
sock.listen(1)

while True:
    # wait for a connection
    print('waiting for a connection')
    conn, client_address = sock.accept()
    try:
        # show who connected to us
        print('connection from', client_address)
        # receive the data in small chunks and print it
        while True:
            data = conn.recv(1024)
            r,s=usv.Protocol_UnPack(data);

            if(len(r)>=2 and r[0]==1 and r[1]==0x17):
                data=[1,0x18]
                if(r[2]==1):
                    i=5;
                    data+=[0]+[r[3]]+[r[4]]
                else:
                    i=3
                    data+=[0]
                data+=r[i:]
                buffer=bytearray(usv.Protocol_Pack(data))
                print("knlnjnknknknkn",[hex(no) for no in data])
                conn.sendall(buffer)

            ri=randint(0,60);
            if (time.time()%60==ri):
                data=[]???
                buffer=bytearray(usv.Protocol_Pack(data))
                sendall(buffer)



    finally:
        # Clean up the connection
        conn.close()
