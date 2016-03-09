#Python classes
import string
import time
from ctypes import *

#Custom classes

from utilities import Utilities as UT

class clientObject: 
        
    def __init__(self,dll):
        self.sseq=c_int(0) 
        self.cseq= c_int(0)
        self.psetup=c_int(0)
        
        self.sseqP = pointer(self.sseq)
        self.cseqP = pointer(self.cseq)
        self.psetupP = pointer(self.psetup)
        self.status = 0
        self.dataBuffer=("\x00"*2048)
        self.dll = dll
        self.data=""
        self.ut = UT()
        
        self.playerData=dict()
        self.playerData["x"]=0.0
        self.playerData["y"]=0.0
        self.playerData["z"]=0.0
        self.playerData["rotation"]=0
                
        self.playerData["healthC"]=0
        self.playerData["healthM"]=0
        self.playerData["innerC"]=0
        self.playerData["innerM"]=0
        
        self.playerData["level"]=1
        self.playerData["profession"]=1
        self.playerData["pvpFlag"]=0
        self.playerData["alignment"]=0

        self.aloneTime = 0
        self.alive=0
        self.queue=[]
    
    def awake(self,addr,UDPsock,myOwnID,printToServer,finishMe,sendToClient):
        self.UDPsock = UDPsock
        self.addr = addr
        self.printToServer = printToServer
        self.finishMe = finishMe
        self.sendToClient = sendToClient
        self.myOwnID = myOwnID

        response= "\x00\x00\x00\x00\x00\x00\x05"  
        for i in range(0,5):
            self.sendToClient(response,addr)
            time.sleep(0.1)

        self.sendToClient(self.processPacket("\x00"),self.addr)
        time.sleep(0.2)
        self.alive=1
        self.printToServer("%s_I'm awake now, father" % self.myOwnID)
        self.workWhileSession()

    def addToQueue(self,data):
        self.queue.append(data)

    def workWhileSession(self):
        
        while(self.alive):
            while(len(self.queue)!=0):
                tempData = self.queue[0]
                del self.queue[0]
                response = self.processPacket(tempData)
                self.sendToClient(response,self.addr)
                self.aloneTime=0
                
            time.sleep(0.1)
            self.aloneTime=self.aloneTime+0.1
            if(self.aloneTime>=90): #if no packets from 1 min:30sec ... finish
                self.alive=0
        self.finishMe("%s:%d" % (self.addr[0],self.addr[1]))
    
    def formatData(self,data):
        output=""
        if(data[0]!='\x00'):
                
                result = self.dll.decryptThePacket(data,self.dataBuffer,self.cseqP,len(data))
                #print decoded data:
    
                for i in range(0,result):
                    value=hex(ord(self.dataBuffer[i])).split("0x")[1]
                    if(len(value)<2):
                        value="0"+value
                    output=output+ value+" "
        else:
                for i in range(0,len(data)):
                    value=hex(ord(data[i])).split("0x")[1]
                    if(len(value)<2):
                        value="0"+value
                    output=output+ value+" "
        return output
 

    def encodePacket(self,data):
        
        encLength = self.dll.encryptThePacket(data,len(data),self.dataBuffer,self.sseqP,self.cseqP,self.psetupP)
        return self.dataBuffer[0:encLength]
    

    def processInitPacket(self):
        
        self.data = self.ut.loadFilePacket(0)
        response = self.encodePacket(self.data)
        return response
     
    def processAckPacket(self,packet):
        response = self.encodePacket("\x02")
        return response
    
    def processPacket(self,packet):
        if(packet[0]=="\x00" and self.status!=0): 
            return packet #If packet is unencrypted, we echo it (if not first!)

        data = self.formatData(packet) # Put that in human readable form plz.        
                
        if (data.startswith("02 04 01 00") and self.status>3):
            splittedData=data.split(" ")
            if (splittedData[5:9]==["01","29","80","c2"]): #It's a jump of any kind
                print "Jump packet"
                (response,newX,newY,newZ)= self.ut.processJump(splittedData,self.playerData["x"],self.playerData["y"],self.playerData["z"])
                if(response!=[]):
                    self.playerData["x"]=newX
                    self.playerData["y"]=newY
                    self.playerData["z"]=newZ
                    for i in range(0,len(response)):
                        response[i]=self.encodePacket(response[i])
                    return response
            else: #it could be a mood/animation/emote yet
                moodAnimationEmote = self.ut.processEmoteMoodAnimation(data,self.playerData["x"],self.playerData["y"],self.playerData["z"])
                if (moodAnimationEmote!=""):
                    return self.encodePacket(moodAnimationEmote)
        
        elif (data.startswith("02 03 02 00 01 08")): #that's a update coord packet
            (movement,x,y,z) = self.ut.processMovement(data) # yes, we will return 4 values, cool
            if (movement!=""):
                self.playerData["x"]=x
                self.playerData["y"]=y
                self.playerData["z"]=z
                return self.processAckPacket(packet)            
        elif (data.startswith("02 03 02 00 01 06") or data.startswith("02 03 02 00 01 04")): # rotation end or rotation update
            self.playerData["rotation"]=self.ut.processRotation(data)
            return self.processAckPacket(packet)
        
        elif ("63 6f 6d 62 61 74" in data):
            response = data = self.ut.replay("combat.log")
            for i in range(0,len(response)):
                response[i]=self.encodePacket(response[i])
            return response
            
        #packet unknown or status not loaded 100% yet
        if (self.status==0):
            self.status = self.status+1
            return self.processInitPacket()

        print "%s ### %s\n"% (self.myOwnID,data)
        
        
        if(self.status==1):
            self.psetup=c_int(1)
            self.psetupP = pointer(self.psetup)
        
        if(self.status==3):
            self.psetup=c_int(15)
            self.psetupP = pointer(self.psetup)
            
        if(self.status==4):
            self.psetup=c_int(127)
            self.psetupP = pointer(self.psetup)
        
      
        if (self.status >=len(self.ut.worldPackets)): #if we dont know what else to answer... say "OK"
            self.status = self.status+1
            return self.processAckPacket(packet)
        
        response = self.encodePacket(self.ut.loadFilePacket(self.status))
        self.status = self.status+1
        time.sleep(0.2)
        return response

    def send(self,data):
        self.UDPSock.sendto(data, (self.addr[0],self.addr[1]))
