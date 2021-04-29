# load additional Python module
import socket
import csv
from utils import USV
import time
import random
import threading

sem = threading.Semaphore()

usv=USV()

PORT = 23456

# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# retrieve local hostname
local_hostname = socket.gethostname()

# get the according IP address
ip_address = socket.gethostbyname(local_hostname)

# bind the socket to the port 23456
server_address = (ip_address, PORT)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# listen for incoming connections (server mode) with one connection at a time
sock.listen(1)
#sock.setblocking(0)

class ThreadMe(threading.Thread):
    def __init__(self,conn,sem):
        threading.Thread.__init__(self)
        self.conn=conn;
        self.sem=sem;

    def run(self):
        while(1):
            data=[1,0xd]
            data+=[0x40,0x36,0x75,0x46,0xc3,0x32,0xf0,0x17,0x40,0x5c,0x90,0x0c,0x49,0xba,0x5e,0x35]
            buffer=bytearray(usv.Protocol_Pack(data))
            print("fkdsjfknlnjnknknknkn",[hex(no) for no in data])
            self.sem.acquire()
            self.conn.sendall(buffer)
            self.sem.release()
            print("knklnlknlnldsif");
            time.sleep(0.5)

while True:

    print('waiting for a connection')
    conn, client_address = sock.accept()

    thread = ThreadMe(conn,sem)
    thread.start()

    try:
        # show who connected to us
        print('connection from', client_address)
        # receive the data in small chunks and print it
        while True:
            print('jhnlidskjfkdjfasj');
            #sem.acquire()
            data = conn.recv(1024)
            #sem.release()
            print('kjpijiujkjhnlidskjfkdjfasj');
            r,s=usv.Protocol_UnPack(data);
            print('dskjfkdjfasj');
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
                sem.acquire()
                conn.sendall(buffer)
                sem.release()
                print("ksadjfkdaknlnjnknknknkn")
            time.sleep(0.1);
    finally:
        # Clean up the connection
        conn.close()
