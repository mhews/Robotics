import socket
import sys

#HOST = '192.168.1.119' #this is your localhost
#PORT = 8888

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket.socket: must use to create a socket.
#socket.AF_INET: Address Format, Internet = IP Addresses.
#socket.SOCK_STREAM: two-way, connection-based byte streams.
#print 'socket created'

#Bind socket to Host and Port
#try:
#    s.bind((HOST, PORT))
#except socket.error as err:
#    print 'Bind Failed, Error Code: ' + str(err[0]) + ', Message: ' + err[1]
#    sys.exit()

#print 'Socket Bind Success!'


#listen(): This method sets up and start TCP listener.
#s.listen(10)
#print 'Socket is now listening'
#
#
# while 1:
#     conn, addr = s.accept()
#     print 'Connect with ' + addr[0] + ':' + str(addr[1])
#     buf = conn.recv(64)
#     print buf
# s.close()

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('192.168.1.119', 8888))
s.listen(1)

while True:
        # Wait for a connection
        print 'waiting for a connection'
        connection, client_address = s.accept()
        try:
                print 'connection from', client_address

                # Receive the data
                while True:
                        data = connection.recv(1024)
                        if data.lower() != 'q':
                                print "<-- client: ", data
                        else:
                                print "Quit from Client"
                                connection.close()
                                break
                        data = raw_input("--> server: ")
                        if data.lower() != 'q':
                                connection.sendall(data)
                        else:
                                print "Quit from Server"
                                connection.close()
                                break

        finally:
                # Clean up the connection
                print "Connection close"
                connection.close()
