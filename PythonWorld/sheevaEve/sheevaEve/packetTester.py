import struct
import string

class packetTesterClass:


        coordX=1890.4794921875
        coordXB = 1890.4794921875
        coordY=95
        coordZ=-54310.83203125
        coordZB = -54310.83203125
        lastObjectID=10
        lastDisguiseSpawn = 10
        openedDoors=2


        
                        
        
        def createDisguises(self):
                header ="\x02\x03" 
                packets=[]
                counter = 0
                bigPacket =""
                
                for j in range(13,14):
                        
                        #print "Creating: ",i
                        #print "Coords: ",self.coordX,self.coordY,self.coordZ
                        #print "ID:",int("%d" %self.lastObjectID,16)
                        counter = -1
                        value2 = struct.pack("h",j)[0]
                        for i in range(0,255):
                                counter = counter+1
                                self.lastObjectID=self.lastObjectID+1
                                packet ="\x01 \x00 \x02 \x1e \x00 \x25 \x00 \x01 \x2e \xa0 \x01 \x0c \xc0 \x00 \x10 \x89 \x00 \x94 \x00 \x00 \xaf \x99 \x44 \x82 \x46 \x00 \x80 \xf7 \x43 \x55 \x8f \xcb \x45 \x01 \x00 \x0c \x0c \x00 \x37 \xcd \xab \x23 \x9b \x7b \x00 \x7d \x00 \x00 \x00 \x48 \x75 \x6e \x74 \x65 \x72 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x12 \xf8 \x9b \x35 \x5c \x07 \x4d \x6f \x6e \x69 \x71 \x75 \x65 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x22 \x9a \x99 \x19 \x3f \x80 \xb8 \xba \x13 \x0c \x00 \x00 \x48 \x42 \xc6 \x81 \xff \x8a \x01 \x96 \xcf <value1> <value2> \x00 \x90 \x81 \xff \x4d \x6f \x72 \x70 \x68 \x65 \x75 \x73 <code> <code2> <code3> \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \x00 \xc0 \xa2 \xf0 \xc0 \x00 \x00 \x00 \x00 \x00 \xc0 \x57 \x40 \x00 \x00 \x00 \x80 \x23 \xcf \xc9 \x40 \xba \x13 \xed \xaa \x01 \x00 \x00 \x81 \xff \x2c \x3c \x02 \x00 \xa3 \x30 \xa0 \x84 \x81 \x98 \xa0 \x01 \xcd \xae \x91 \x00 \x80 \x00 \x00 \x8a \x01 \xdd <coordX> <coordY> <coordZ> \x81 \xff \x63 \x22 \x66 \x00 \x00 \x04 \x80 \xc9 \x68 \x45 \x5d \x07 \x3f \x00 \x1c \x03 \x85 \x00 \x00 \x00 \x81 \xff <id> \x00 \x00"
                                packetList = string.split(packet," ")
                                
                                value1 = struct.pack("h",i)[0]
                                    
                                packet = string.join(packetList,"")
        
                                if (counter%6!=0):
                                        self.coordZ = self.coordZ-200
                                else:
                                        self.coordZ = self.coordZB
                                        self.coordX = self.coordX-200
                                packet = string.replace(packet,"<coordX>",struct.pack("d",self.coordX))
                                packet = string.replace(packet,"<coordY>",struct.pack("d",self.coordY))
                                packet = string.replace(packet,"<coordZ>",struct.pack("d",self.coordZ))
                                
                                
                                if(counter<10):
                                        num = int(("%s" % counter)[-1])+30
                                        numHex = "%c" % int("%s" % num,16)
                                        packet = string.replace(packet,"<code3>",numHex)
                                        packet = string.replace(packet,"<code2>","\x20")
                                        packet = string.replace(packet,"<code>","\x20")
                                if(counter>10 and counter <100):
                                        num = int(("%s" % counter)[-1])+30
                                        numHex = "%c" % int("%s" % num,16)
                                        packet = string.replace(packet,"<code3>",numHex)    
                                        num2 = int(("%s" % counter)[-2])+30
                                        numHex2 = "%c" % int("%s" % num2,16)
                                        packet = string.replace(packet,"<code2>",numHex2)
                                        packet = string.replace(packet,"<code>","\x20")
                                if(counter>100):
                                        num = int(("%s" % counter)[-1])+30
                                        numHex = "%c" % int("%s" % num,16)
                                        packet = string.replace(packet,"<code3>",numHex)    
                                        num2 = int(("%s" % counter)[-2])+30
                                        numHex2 = "%c" % int("%s" % num2,16)
                                        packet = string.replace(packet,"<code2>",numHex2)
                                        num3 = int(("%s" % counter)[-3])+30
                                        numHex3 = "%c" % int("%s" % num3,16)
                                        packet = string.replace(packet,"<code>",numHex3)
                                
                                #packet = string.replace(packet,"<value1>",value1)
                                #packet = string.replace(packet,"<value2>",value2)
                                packet = string.replace(packet,"<value1>","\x72")
                                packet = string.replace(packet,"<value2>","\x09")
                                packet = string.replace(packet,"<id>",struct.pack("l",self.lastObjectID)[0:2])
                                bigPacket ="%s%s" % (header,packet)
                                
                                packets.append(bigPacket)
                return packets
