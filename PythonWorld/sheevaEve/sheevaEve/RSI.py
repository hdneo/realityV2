import string

class RSIHandler:

    unknown1 ="0"
    unknown2 ="00"
    rsiData = {}
    

    def bin(self,x,bits):
        binString=""
        d = {0:'000', 1:'001', 2:'010', 3:'011', 4:'100', 5:'101', 6:'110', 7:'111'}
        binString = ''.join([d[int(dig)] for dig in oct(x)])
        while len(binString)<bits:
            binString ="0%s" % binString

        if len(binString)>bits:
            binString = binString[-bits:]
            
        return binString

    def __init__(self):
        
        self.setSex(0)
        self.setBody(0)
        self.setHat(0)
        self.setFace(0)
        self.setShirt(0)
        self.setCoat(0)
        self.setPants(0)
        self.setShoes(0)
        self.setGloves(0)
        self.setGlasses(0)
        self.setHair(0)
        self.setFacialdetail(0)
        self.setShirtcolor(0)
        self.setPantscolor(0)
        self.setCoatcolor(0)
        self.setShoecolor(0)
        self.setGlassescolor(0)
        self.setHaircolor(0)
        self.setSkintone(0)
        self.setTattoo(0)
        self.setFacialdetailcolor(0)
        self.setLeggins(0)
        
    def setSex(self,sex):
        self.rsiData["sex"]=sex

    def setBody(self,body):
        self.rsiData["body"] = body

    def setHat(self,hat):
        self.rsiData["hat"] = hat

    def setFace (self,face):
        self.rsiData["face"] = face

    def setShirt (self,shirt):
        self.rsiData["shirt"] = shirt

    def setCoat(self,coat):
        self.rsiData["coat"] = coat
        
    def setPants(self,pants):
        self.rsiData["pants"]=pants
        
    def setShoes(self,shoes):
        self.rsiData["shoes"]=shoes

    def setGloves(self,gloves):
        self.rsiData["gloves"]=gloves

    def setGlasses(self,glasses):
        self.rsiData["glasses"]=glasses

    def setHair(self,hair):
        self.rsiData["hair"]=hair

    def setFacialdetail(self,facialdetail):
        self.rsiData["facialdetail"]=facialdetail

    def setShirtcolor(self,shirtcolor):
        self.rsiData["shirtcolor"]=shirtcolor

    def setPantscolor(self,pantscolor):
        self.rsiData["pantscolor"]=pantscolor

    def setCoatcolor(self,coatcolor):
        self.rsiData["coatcolor"]=coatcolor

    def setShoecolor(self,shoecolor):
        self.rsiData["shoecolor"]=shoecolor

    def setGlassescolor(self,glassescolor):
        self.rsiData["glassescolor"]=glassescolor

    def setHaircolor(self,haircolor):
        self.rsiData["haircolor"]=haircolor

    def setSkintone(self,skintone):
        self.rsiData["skintone"]=skintone

    def setTattoo(self,tattoo):
        self.rsiData["tattoo"]=tattoo

    def setFacialdetailcolor(self,facialdetailcolor):
        self.rsiData["facialdetailcolor"]=facialdetailcolor

    def setLeggins(self,leggins):
        self.rsiData["leggins"] =leggins

    def generateRSI(self):

        rsiList=[]
        #Operations bitwise coming
       
        rsiList.append(self.bin(self.rsiData["sex"],1))
        rsiList.append(self.bin(self.rsiData["body"],2))
        rsiList.append(self.bin(self.rsiData["hat"],6))
        rsiList.append(self.bin(self.rsiData["face"],5))
        rsiList.append(self.unknown1)
        rsiList.append(self.bin(self.rsiData["shirt"],5))

        if(self.rsiData["sex"]==0): #is male
            rsiList.append(self.bin(self.rsiData["coat"],6))
            rsiList.append(self.bin(self.rsiData["pants"],5))
            rsiList.append(self.bin(self.rsiData["shoes"],6))
            rsiList.append(self.bin(self.rsiData["gloves"],5))
            rsiList.append(self.bin(self.rsiData["glasses"],5))
            rsiList.append(self.bin(self.rsiData["hair"],5))
            rsiList.append(self.bin(self.rsiData["facialdetail"],4))
            rsiList.append(self.bin(self.rsiData["shirtcolor"],6))
            rsiList.append(self.bin(self.rsiData["pantscolor"],5))
            rsiList.append(self.bin(self.rsiData["coatcolor"],5))
            rsiList.append(self.bin(self.rsiData["shoecolor"],4))
            rsiList.append(self.bin(self.rsiData["glassescolor"],4))
            rsiList.append(self.bin(self.rsiData["haircolor"],5))
            rsiList.append(self.bin(self.rsiData["skintone"],5))
            rsiList.append(self.unknown2)
            rsiList.append(self.bin(self.rsiData["tattoo"],3))
            rsiList.append(self.bin(self.rsiData["facialdetailcolor"],3))
            rsiList.append("000000") #to fill 13 bytes
        else: #is female
            rsiList.append(self.bin(self.rsiData["coat"],5))
            rsiList.append(self.bin(self.rsiData["pants"],5))
            rsiList.append(self.bin(self.rsiData["shoes"],5))
            rsiList.append(self.bin(self.rsiData["gloves"],6))
            rsiList.append(self.bin(self.rsiData["glasses"],5))
            rsiList.append(self.bin(self.rsiData["hair"],5))
            rsiList.append(self.bin(self.rsiData["leggins"],4))
            rsiList.append(self.bin(self.rsiData["shirtcolor"],6))
            rsiList.append(self.bin(self.rsiData["pantscolor"],5))
            rsiList.append(self.bin(self.rsiData["coatcolor"],5))
            rsiList.append(self.bin(self.rsiData["shoecolor"],4))
            rsiList.append(self.bin(self.rsiData["glassescolor"],4))
            rsiList.append(self.bin(self.rsiData["haircolor"],5))
            rsiList.append(self.bin(self.rsiData["skintone"],5))
            rsiList.append(self.unknown2)
            rsiList.append(self.bin(self.rsiData["tattoo"],3))
            rsiList.append(self.bin(self.rsiData["facialdetailcolor"],3))
            rsiList.append("0000000") #to fill 13 bytes
        rsiString = string.join(rsiList,"")

        rsiGenerated = ""
        for i in range(0,len(rsiString),8):
            binToHex = rsiString[i:i+8]
            rsiGenerated ="%s%c" % (rsiGenerated,int(binToHex,2))

        return rsiGenerated
