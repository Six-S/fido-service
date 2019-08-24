import sys, json, time
import thread
import hashlib
import socket

#LETS MAKE A LOG FILE, OKAY?

HOST, PORT = '10.0.0.81', 3000
address = ''
connection = False
sig = ''

class MessageHandler():

    def __init__(self):
        print 'Starting request handler'
        #set up the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #connect the socket
        self.sock.connect((HOST, PORT))

        #save our socket object to our messagehandler class, then run connect.
        self.setSockData(self.sock)
        
        thread.start_new_thread(self.ping_pong, (self.sock, ))

    #this will handle the incoming responses from our dispatch server
    def parseMessage(self, message):
        print message
    
    def getSock(self):
        return self.sock
    
    def ping_pong(self, socket):
        print '[INFO] playing ping pong!'
        disconnected = False
        while not disconnected:
            data = 'Ping'
            time_now = time.asctime( time.localtime(time.time()))
            try:
                self.sock.sendall(data + '\n')
                recieved = self.sock.recv(1024)
            except:
                print 'Failed to ping server at ' + time_now
                disconnected = True
            
            time.sleep(60)
        

    #this checks the type of our response to make sure that we can run json.loads on it.
    #if we return false, we'll exit non-zero, so checking that first will help us handle this error.
    def typeCheck(self, to_check):
        if isinstance(to_check, basestring):
            return True
        else:
            return False

    #this logic runs on init in order to make sure the recieving end exists, and that
    #it's ready to recieve messages. We also use this function to get our connection information.
    def connect(self, socket, msg_type):
        if msg_type == 'init':
            msg = 'Request Connect'
        else:
            msg = raw_input('> ')

        self.sock.sendall(msg + '\n')

        recieved = self.sock.recv(1024)

        global connection, address, sig
        if self.typeCheck(recieved):
            data = json.loads(recieved)
            print data
            if data['type'] == 'GoodBye':
                return True
            elif data['result'] == 'Approved':
                address = data['requestingip']
                sig = data['secret']
                return False
            elif data['result'] == 'Active':
                address = data['requestingip']
                return False
            else:
                print 'an unexpected error occured. Quitting...'
                return True

    def reconnect(self):
        raise NotImplementedError

    #sets the socket object to a variable, sends a connection request to the server
    def setSockData(self, socket):
        self.connect(socket, 'init')


if __name__ in '__main__':

    try:

        #start the backbone of our service.
        #loop and send messages until we can't anymore.

        #set up our message handler
        handle = MessageHandler()
        sock = handle.getSock()
        time.sleep(10)

        disconnect = False
        while not disconnect:
            data = raw_input('> ')

            sock.sendall(data + '\n')

            recieved = sock.recv(1024)

            #send current IP and time with each message
            if handle.typeCheck(recieved):
                print recieved
                data = json.loads(recieved)
                if data['type'] == 'GoodBye':
                    disconnect = True
                    sock.close()
                else:
                    handle.parseMessage(data)
            else:
                print 'We did not get a string. We should not be here.'
                print recieved
    except Exception as e:
        print '[WARN] We encountered an error: ', e
        raise SystemExit
