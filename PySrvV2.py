#!/usr/bin/python

            ###################################################
            ##  Home Network Chat Server (HNCS) version 0.2  ##
            ##           by John G. [Nine] 2007              ##
            ###################################################


##                          Huh?
##
## This is a little telnet chat server I've been working on while
## learning how to network program with Python. It uses the
## ThreadingTCPServer class from the SocketServer module. Each thread
## (or user) is an instance of my ClientHandler class, which is just a
## modified BaseRequestHandler.

##                          Fix Me
##
## I want this to be a telnet chat server. When telnetting to it from a
## Linux machine, there are no problems. When telnetting to it from a
## Windows machine, the telnet client sends EVERY SINGLE BLOODY
## KEYSTROKE. I'm sure this can be fixed by changing the client-side
## telnet settings, but I want it to be Windows-client friendly by
## default. Basically, I don't want the server to read input until the
## user hits <return>.


##########################################################
#               Imports, Globals, Constants
##########################################################
from time import *
from socketserver import *

HOST = ''           # "this machine"
PORT = 23           # the telnet port
userlist = []       # list to hold user connection objects (these aren't strings!)
namelist = []       # list of nicknames tied to each client handler thread
addr = (HOST, PORT)
###########################################################



###########################################################
#               Misc. functions
###########################################################
def now():          # returns the current time on the server
    return ctime(time())

def welcome():      # returns a welcome note to be sent to new connections and to the server terminal on start
    return """\r\n---------------------------------------------------\r\n
\tChat version 0.2 - Copyleft 2015 Callum M.\r\n
\t\tPowered by Python!\r\n
---------------------------------------------------\r\n

Local time is %s. %i user(s) online:\r\n
%s
""" % (now(), len(userlist), repr(namelist))
#############################################################



##############################################################
# The client handler class (instances will be threads)
##############################################################
class ClientHandler(BaseRequestHandler):                            # i'm thinking of renaming this class to 'User'

    def handle(self):

        userlist.append(self.request)                               # add the socket object to the userlist
        self.setnick()                                              # set the nickname and append it to namelist
        sleep(3)                                                    # display 'Welcome, <user>' for 3 sec.
        print(self.connection())                                    # print connection log at server
        self.request.send((welcome()).encode(encoding="ASCII", errors="strict"))                               # send a welcome to just the user

        self.broadcast(self.connection())                           # broadcast your logon

        print('\t\t[%i users online]\n' % len(userlist))             # print number of users to server terminal

        while True:                                                 # Infinite loop that stops when client disconnects
            try:
                data = self.request.recv(1024)  # try to get data from client
                data = data.decode(encoding="ASCII", errors="strict")
                print('%s: "%s"' % (self.client_address[0], data))   # print the data to the server terminal
                outgoing = '\r\n%s: %s\r\n' % (self.nickname, data) # format the message
                self.broadcast(outgoing)                            # broadcast the message to all users

            except:                                                 # if no data...
                print(self.disconnection())                         # print disconnection to server terminal

                userlist.remove(self.request)                       # remove the socket object from userlist
                namelist.remove(self.nickname)                      # remove nickname from namelist
                self.broadcast(self.disconnection())                # broadcast your disconnection
                self.request.close()                                # close the connection

                print('\t\t[%i user(s) online]\r\n' % len(userlist))  # print number of users to server terminal

                return                                              # kill this particular thread

    def broadcast(self, data):                                      # send data to all users in userlist
        for user in userlist:
            user.send(data.encode(encoding="ASCII", errors="strict"))

    def disconnection(self):                                        # return a formatted disconnect message
        return '\r\n(%s)%s disconnected at %s' % (self.nickname, self.client_address[0], now())

    def connection(self):                                           # return a formatted connect message
        return '\r\n(%s) %s connected at %s' % (self.client_address[0], self.nickname, now())

    def setnick(self):                                              # acquire and assign a nickname for this thread
        self.request.send(('\r\nNickname: ').encode(encoding="ASCII", errors="strict"))
        self.nickname = self.request.recv(1024)
        self.request.send(('\r\nWelcome, %s!\n' % self.nickname).encode(encoding="ASCII", errors="strict"))
        namelist.append(self.nickname)
###################################################################

                                                    # server is going to be a ThreadingTCPServer, bound to
server = ThreadingTCPServer(addr, ClientHandler)    # 'addr' and each thread will be a 'ClientHandler'
                                                    # class instance.

if __name__ == '__main__':
    print(welcome())                                                # print welcome note to server terminal
    print('\nServer started. Listening for connections on port %i...\n' % PORT)
    server.serve_forever()                                          # run until program is closed