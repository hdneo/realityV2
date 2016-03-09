import string

class ReplayWorld:

    
    fileHandler = None

    def load(self,logFile):
        self.fileHandler=open(logFile,"r")

    def close(self):
        self.fileHandler.close()
        
    def replay(self,logFile):
        self.load(logFile)
        data = self.fileHandler.read()

        dataList = data.splitlines()

        print "Lines: ",len(dataList)
        
        contents = []
        stringSend =""
        status = 0
        for i in range(0,len(dataList)):
            if "Client->WORLD" in dataList[i]:
                pass
            elif "WORLD->Client" in dataList[i]:
                status = 1
            elif "." in dataList[i] and status == 1:
                status = 0
                processedString = stringSend
                stringSend=""
                processedString = string.replace(processedString,"\n"," ")
                processedString = string.replace(processedString,"  "," ")
                processedString = processedString[:-1]
                contents.append(processedString)
            elif dataList[i].startswith("PSS"):
                pass
            elif dataList[i].startswith("Not Encrypted"):
                print "Packet non encrypted"
                status=0
            elif dataList[i].startswith("\n"):
                pass
            else:
                if status==1:
                    stringSend = "%s%s" % (stringSend,dataList[i])
        self.close()

        return contents


class ReplayMargin:

    
    fileHandler = None

    def load(self,logFile):
        self.fileHandler=open(logFile,"r")

    def close(self):
        self.fileHandler.close()
        
    def replay(self,logFile):
        self.load(logFile)
        data = self.fileHandler.read()

        dataList = data.splitlines()

        print "Lines: ",len(dataList)
        
        contents = []
        stringSend =""
        status = 0
        for i in range(0,len(dataList)):
            if "Client->MARGIN" in dataList[i]:
                pass
            elif "MARGIN->Client" in dataList[i]:
                status = 1
            elif "." in dataList[i] and status == 1:
                status = 0
                processedString = stringSend
                stringSend=""
                processedString = string.replace(processedString,"\n"," ")
                processedString = string.replace(processedString,"  "," ")
                processedString = processedString[:-1]
                contents.append(processedString)
            elif dataList[i].startswith("encrypted=true"):
                pass
            elif dataList[i].startswith("Not Encrypted"):
                print "Packet non encrypted"
                status=0
            elif dataList[i].startswith("\n"):
                pass
            else:
                if status==1:
                    stringSend = "%s%s" % (stringSend,dataList[i])
        self.close()

        return contents

