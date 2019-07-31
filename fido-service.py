import sys, json
import socket

#LETS MAKE A LOG FILE, OKAY?

HOST, PORT = '10.0.0.81', 3000
address = ''
connection = ''
#data = 'Request Connect'

class MessageHandler():

    def __init__(self):
        print 'Starting request handler'

    #this will handle the incoming responses from our dispatch server
    def parseMessage(self, message):
        print message

    #this checks the type of our response to make sure that we can run json.loads on it.
    #if we return false, we'll exit non-zero, so checking that first will help us handle this error.
    def typeCheck(self, to_check):
        if isinstance(to_check, basestring):
            return True
        else:
            return False

    #this logic runs on init in order to make sure the recieving end exists, and that
    #it's ready to recieve messages. We also use this function to get our connection information.
    def connect(self, socket):
        data = 'Request Connect'
        sock.sendall(data + '\n')

        recieved = sock.recv(1024)

        global connection, address
        if self.typeCheck(data):
            data = json.loads(recieved)
            print data
            if data['type'] == 'GoodBye':
                return True
            elif data['result'] == 'Approved':
                address = data['requestingip']
                return False
            elif data['result'] == 'Active':
                address = data['requestingip']
                return False
            else:
                print 'an unexpected error occured. Quitting...'
                return True

    #sets the socket object to a variable, sends a connection request to the server
    def setSockData(self, socket):
        self.socket = socket
        self.connect(socket)


if __name__ in '__main__':

    #set up the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        #connect the socket
        sock.connect((HOST, PORT))

        #set up our message handler
        handle = MessageHandler()

        #save our socket object to our messagehandler class, then run connect.
        #handle.setSockData(sock)

        #start the backbone of our service.
        #loop and send messages until we can't anymore.
        disconnect = False
        while not disconnect:
            data = raw_input('> ')
            sock.sendall(data + '\n')

            recieved = sock.recv(1024)

            #send current IP and time with each message

            if handle.typeCheck(recieved) and recieved != '':
                print recieved
                data = json.loads(recieved)
                if data['type'] == 'GoodBye':
                    disconnect = True
                else:
                    handle.parseMessage(data)
            else:
                print 'We did not get a string. We should not be here.'
                print recieved

    finally:
        #we should also try and send a goodbye from here if we can.
        sock.close()
