import time
import thread
import struct


class Sheeva:

    #template should include the "do talk animation" on the world Object
    #chatTemplate = "\x02\x03<clientID>\x01\x02\x73\x00\x00\x04\x01<chatLine>\x01<packetLength>\x2e\x10\x00<clientWorldID>\x24\x00\x00\x00\x2f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00<handleLength><handle>\x00<messageLenght><message>\x00"
    chatTemplate = "\x02\x04\x01<chatLine>\x01<packetLength>\x2e\x10\x00<clientWorldID>\x24\x00\x00\x00\x2f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00<handleLength><handle>\x00<messageLength><message>"
    def __init__(self, clientsConnected):
        print "Sheeva . Chat server created"
        self.alive=1
        self.clientsConnected = clientsConnected
        self.ready = 0

    def start(self):
        print "Sheeva - Chat server started"
        self.workTillDead()

    def die (self):
        self.alive=0

    def getReadyStatus(self):
        return self.ready

    def workTillDead(self):
        self.ready = 1
        while(self.alive==1):
            time.sleep(0.05) # for now, do nothing but send-to-all received packets

    def receiveChatPacket(self,message,emitterAddr, clientID, clientWorldID, clientHandle):
        print "Processing message: ",message
        thread.start_new_thread(self.broadcastMessage,(message, emitterAddr,clientID, clientWorldID, clientHandle))


    def broadcastMessage(self,message,emitterAddr, clientID, clientWorldID, clientHandle):

        localTemplate = self.chatTemplate
        localTemplate = localTemplate.replace("<clientID>",clientID)
        localTemplate = localTemplate.replace("<clientWorldID>",clientWorldID)
        localTemplate = localTemplate.replace("<message>",message)
        localTemplate = localTemplate.replace("<messageLength>",struct.pack("h",len(message)+1))
        localTemplate = localTemplate.replace("<handle>",clientHandle)
        localTemplate = localTemplate.replace("<handleLength>",struct.pack("h",len(clientHandle)+1))

        packetStart = localTemplate.find(">\x2e")+1
        localTemplate = localTemplate.replace("<packetLength>",struct.pack("h",len(localTemplate[packetStart:]))[0])

        #here create a local list of keys without emitter to do dict[key].process...
        allClientsButEmitter = self.clientsConnected.keys()
        allClientsButEmitter.remove(emitterAddr)
        print len(allClientsButEmitter)
        for client in allClientsButEmitter:
            self.clientsConnected[client].processIncomingChat(localTemplate)
