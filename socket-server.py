# load additional Python module
import socket
import csv
import event_pb2

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
    connection, client_address = sock.accept()
    try:
        # show who connected to us
        print('connection from', client_address)
        # receive the data in small chunks and print it
        while True:
            data = connection.recv(1024)
            if data:
                # output received data
                print("Data: %s" % data)
                event = event_pb2.EventProto()
                event.ParseFromString(data)
                print("Parsed event %s" % event)
                row = [event.timestamp, event.userId, event.event]
                with open(FILE_PATH, 'a') as writeFile:
                    writer = csv.writer(writeFile)
                    writer.writerow(row)
                writeFile.close()
                connection.sendall(data)
            else:
                # no more data -- quit the loop
                print("no more data.")
                break
    finally:
        # Clean up the connection
        connection.close()