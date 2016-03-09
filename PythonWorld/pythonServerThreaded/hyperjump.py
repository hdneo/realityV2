import struct 


class HyperJump:
    
    def __init__(self):
        self.jumpID=[]
        self.jumpID.append(4625)
        self.jumpID.append(4881)
        self.currentID=0
        
    
    def processHyperJump(self,x,y,z,destX,destY,destZ):
        
        hyperjumpP=[]
        hyperjumpP.append("\x82\x89\xf3\x25\x49\x03\x02\x00\x03\x08<x><y><z>\x00\x00\x83\x28\xff\x01\x64\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x41\x6e\x64\x65\x72\x73\x6f\x6e\x06\x54\x68\x6f\x6d\x61\x73\xff\xe0\x18\x40\x0c\x41\x05\xe0\x02\x04\x00\xcd\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x8f\x01\x00\x02\x00\x2a\x03\x02\xff\x28\x0a\x32\x00\xf0\x20\x46\x04\x00<lastJumpID>\x84\x28<xDest><yDest><zDest>\x00\xff\x00\x00\x00\x00\x00\xf7\x00\x00\x00\xe7\x00\x00\x00\x00\x00\x28\x0a\xff\x00\x31\x5e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x3f\x11\x00\x00\x00\x4b\xb1\x00\x00\x71\x02\x00\x00\x3f\x00\x00\x00\x00\x22\x00\x00\x00\x00\x00\x00\x00\x05\x00\x01\x00\x04<x><y><z>\x00\x00")
        
        hyperjumpP.append("\x82\x9a\xf3\x25\x49\x03\x02\x00\x03\x08<x><y><z>\x00\x00\x83\x28\xff\x01\x64\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x41\x6e\x64\x65\x72\x73\x6f\x6e\x06\x54\x68\x6f\x6d\x61\x73\xff\xe0\x18\x40\x0c\x41\x05\xe0\x02\x04\x00\xcd\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x8f\x01\x00\x02\x00\x2a\x03\x02\xff\x28\x0a\x32\x00\xf0\x20\x46\x04\x00<lastJumpID>\x84\x28<xDest><yDest><zDest>\x00\xff\x00\x00\x00\x00\x00\xf7\x00\x00\x00\xeb\x00\x00\x00\x00\x00\x28\x0a\xff\x00\x31\x5e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x3f\x11\x00\x00\x00\x4b\xb1\x00\x00\x71\x02\x00\x00\x3f\x00\x00\x00\x00\x22\x00\x00\x00\x00\x00\x00\x00\x05\x00\x01\x00\x04<x><y><z>\x00\x00")
        
        hyperjumpP.append("\x82\xbf\xf3\x25\x49\x03\x02\x00\x03\x08<x><y><z>\x00\x00\x84\x28\xff\x01\x64\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x41\x6e\x64\x65\x72\x73\x6f\x6e\x06\x54\x68\x6f\x6d\x61\x73\xff\xe0\x18\x40\x0c\x41\x05\xe0\x02\x04\x00\xcd\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x8f\x01\x00\x02\x00\x2a\x03\x02\xff\x28\x0a\x32\x00\xf0\x20\x46\x04\x00<lastJumpID>\x84\x28<xDest><yDest><zDest>\x00\xff\x00\x00\x00\x00\x00\xf7\x00\x00\x00\xf2\x00\x00\x00\x00\x00\x28\x0a\xff\x00\x31\x5e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x3f\x11\x00\x00\x00\x4b\xb1\x00\x00\x71\x02\x00\x00\x3f\x00\x00\x00\x00\x22\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x04<x><y><z>\x00\x00")
       
        
        for i in range(0,len(hyperjumpP)):
            hyperjumpP[i] = hyperjumpP[i].replace("<x>",struct.pack("f",x))
            hyperjumpP[i] = hyperjumpP[i].replace("<y>",struct.pack("f",y))
            hyperjumpP[i] = hyperjumpP[i].replace("<z>",struct.pack("f",z))
                    
            hyperjumpP[i] = hyperjumpP[i].replace("<xDest>",destX)
            hyperjumpP[i] = hyperjumpP[i].replace("<yDest>",destY)
            hyperjumpP[i] = hyperjumpP[i].replace("<zDest>",destZ)
            hyperjumpP[i] = hyperjumpP[i].replace("<lastJumpID>",struct.pack("h",self.jumpID[self.currentID]))
            self.currentID = 1 - self.currentID
            
        return (hyperjumpP ,struct.unpack("d",destX)[0],struct.unpack("d",destY)[0],struct.unpack("d",destZ)[0])