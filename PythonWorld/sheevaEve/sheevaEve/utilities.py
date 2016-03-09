import string
import struct

import emoteList
from processLog import ReplayWorld as WorldLog
from hyperjump import HyperJump as HJ
#from RSI import RSIHandler as RSI

class Utilities:
    
    
    
    
    def __init__(self):
        self.hyperjMan = HJ()
        self.mood = 1
        self.moodPacket="\x02\x03\x02\x00\x01\x01<animation><mood>\x00\x00"
        self.emotePacket="\x02\x03\x02\x00\x01\x28<emoteNum>\x40\x00\x25<emoteID>\x00\x00\x10<coordX><coordY><coordZ>\x2a\x9f\x1e\x20\x00\x00"
        self.lastEmote =0
        self.world = WorldLog()
        self.worldPackets = self.world.replay("world.log")
    
    def transformPacket(self,packet):
        packet = packet.replace("\n","")
        packet = packet.replace(" ","")
        packet = packet.replace("  ","")
        tempList = packet.split(",")
           
        for i in range (0,len(tempList)):
            try:
                tempList[i] = "%c" % int(tempList[i][2:],16)
            except:
                print "Error on: ",tempList[i]
                
        packet = string.join(tempList,"")
                
        return packet
            
    def preTransform(self,packet):
        packet = packet.replace("\n","")
        packet = packet.replace(" ",",0x")
        packet = "0x%s" % packet
        return packet
         
        
    def loadFilePacket(self,num):
        localdata = self.worldPackets[num]
        localdata = self.preTransform(localdata)
        localdata = self.transformPacket(localdata)
        return localdata

    def replay(self,name):
        replayP = self.world.replay(name)
        for i in range(0,len(replayP)):
            replayP[i]=self.preTransform(replayP[i])
            replayP[i] = self.transformPacket(replayP[i])
        return replayP
    
    def processRotation(self,packet):
        packet = packet.split(" ")
        
        #Just return the integer value of byte 6 or 7, depending on condition
        # 04 rotating
        # 06 ended rotation
        if packet[5]=='04':
            return int(packet[6],16)
        return int(packet[7],16)
    
    def processMovement(self,packet,offset):
        packet = packet.split(" ")

        x = packet[6+offset:10+offset]
        
        y = packet[10+offset:14+offset]
        z = packet[14+offset:18+offset]
        
        x = string.join(x,"")
        y = string.join(y,"")
        z = string.join(z,"")
        
        x = struct.unpack("f",x.decode('hex'))[0]
        y = struct.unpack("f",y.decode('hex'))[0]
        z = struct.unpack("f",z.decode('hex'))[0]
        
        return ("ok",x,y,z)
    
    def processJump(self,data,x,y,z):
        if (data[40:44]==["00","7a","44","01"]):
            print "Hyperjump (skill)"
            
            destX = (string.join(data[9:17],"")).decode('hex')
            destY = (string.join(data[17:25],"")).decode('hex')
            destZ = (string.join(data[25:33],"")).decode('hex')
            maxHeight = (string.join(data[39:43],"")).decode('hex')
            lastBytes = (string.join(data[-4:],"")).decode('hex')
            
            (response,newX,newY,newZ) = self.hyperjMan.processHyperJump(x,y,z,destX,destY,destZ,maxHeight,lastBytes)        
            return (response,newX,newY,newZ)
        elif (data[40:44]==["f0","20","46","01"]):
            print "Hyperjump (ctrl-space)"
            return ([],0,0,0)
        elif (data[40:44]==["00","87","43","00"]):
            print "Normal Jump"
            return ([],0,0,0)
        return ([],0,0,0)
          
    def processEmoteMoodAnimation(self,packet,x,y,z):
        packet = packet.split(" ") # create a list of elements
        position = 5
        
        if (packet[position]!='01'):
            return ""
        else:
            position=position+1
            if (packet[position]=='02'): #is a Mood / Animation
                position=position+1
                response = self.moodPacket
                if (packet[position]=='33'): # is Stop animation
                    response = response.replace("<animation>","\x00")
                    response = response.replace("<mood>",struct.pack("h",self.mood)[0])
                    return response
                elif (packet[position]=='34'): # is An animation request
                    response = response.replace("<animation>",struct.pack("h",int(packet[position+1],16))[0])
                    response = response.replace("<mood>",struct.pack("h",self.mood)[0])
                    return response
                elif (packet[position]=='35'): # is A Mood request
                    self.mood = int(packet[position+1],16)
                    response = response.replace("<animation>","\x00")
                    response = response.replace("<mood>",struct.pack("h",self.mood)[0])
                    return response
            elif(packet[position]=='09'):
                # maybe its an emote
                
                position = position+1
                if (packet[position]=='30'):
                    print "xyz for emote: ",x,y,z
                    emoteKey = string.join(packet[position+1:position+5],"")
                    emoteID=emoteList.getValueForKey(emoteKey)
                    if(emoteID!=-1):
                        self.lastEmote = self.lastEmote+1
                        if(self.lastEmote==255): 
                            self.lastEmote=0                        
                        response = self.emotePacket
                        response= response.replace("<emoteNum>",struct.pack("h",self.lastEmote)[0])
                        response= response.replace("<emoteID>",struct.pack("h",emoteID)[0])
                        response= response.replace("<coordX>",struct.pack("f",x))
                        response= response.replace("<coordY>",struct.pack("f",y))
                        response= response.replace("<coordZ>",struct.pack("f",z))
                        return response

        return ""
                
                    
                    
    
    
    
