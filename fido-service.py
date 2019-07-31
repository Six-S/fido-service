import sys, json
import socket

HOST, PORT = '10.0.0.81', 3000
localIP = ''
#data = 'Request Connect'

class MessageHandler():

    def __init__(self):
        print 'Starting request handler'

    def parseMessage(self, message):
        print message

if __name__ in '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))

        handle = MessageHandler()
        disconnect = False
        while not disconnect:
            data = raw_input('> ')
            sock.sendall(data + '\n')

            recieved = sock.recv(1024)

            data = json.loads(recieved)
            if data['type'] == 'GoodBye':
                disconnect = True
            else:
                handle.parseMessage(data)

    finally:
        #print 'An error occured, and the socket either could not be opened, or a message could not be sent.'
        sock.close()
        #raise SystemExit

    #finally:
        #sock.close()

    print 'Sent: {}'.format(data)
    print 'Recieved: {}'.format(recieved)
