from socket import *
from ctypes import *
from clientObject import clientObject
from sheeva import Sheeva
import time
import string
import thread


clientByAddr=dict()
dll= cdll.LoadLibrary('worldcrypto.dll')
clientAvailableID=7999


###########################################

def outPutFromClient(messageFromClient):
    print "Client sent: ",messageFromClient

def finishClientObject(clientObjectAddr):
    del clientByAddr[clientObjectAddr]
    print "Client %s finished" % clientObjectAddr


def sendToGameClient(response,addr):
    if (len(response[0])==1): #a single packet (so 1 byte)
        UDPSock.sendto(response, (addr[0],addr[1]))
    else:
        print "Subpackets, more than one ;)"
        for subpacket in response: # yeah, just send it in a bunch
            UDPSock.sendto(subpacket, (addr[0],addr[1]))


################

# we want to bind on all possible IP addresses


print "\n"
print "-" * 42
print "World Server - Python version. By Morpheus"
print "Codename \"Scatman\""
print "-" * 42
print "\n"
print "Starting UDP server for world."

host = "0.0.0.0"
port = 10000
buffer = 102400
UDPSock = socket(AF_INET,SOCK_DGRAM)
UDPSock.bind((host,port))


print "\nInitializing services\n"

sheeva = Sheeva(clientByAddr)
thread.start_new_thread(sheeva.start,())


while (sheeva.getReadyStatus()==0):
    time.sleep(0.1)

print "\n\nReady and waiting for data..."

while 1:
    data,addr = UDPSock.recvfrom(buffer)
    key = "%s:%d" % (addr[0],addr[1])
    if clientByAddr.has_key(key):
        (clientByAddr[key]).addToQueue(data)

    else:
        clientByAddr[key]=clientObject(dll)
        clientAvailableID = clientAvailableID+1
        thread.start_new_thread(clientByAddr[key].awake,(addr,UDPSock,sheeva,clientAvailableID,outPutFromClient,finishClientObject,sendToGameClient))

UDPSock.close()
