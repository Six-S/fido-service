import sys, json
import socket

HOST, PORT = '10.0.0.81', 3000
localIP = ''
data = 'Request Connect'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST, PORT))
    sock.sendall(data + '\n')

    recieved = sock.recv(1024)
finally:
    #print 'An error occured, and the socket either could not be opened, or a message could not be sent.'
    sock.close()
    #raise SystemExit

#finally:
    #sock.close()

print type(recieved)
test = json.loads(recieved)
print type(test)
print 'Sent: {}'.format(data)
print 'Recieved: {}'.format(recieved)
