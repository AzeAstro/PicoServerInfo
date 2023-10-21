import struct
class Server:
    serverName:str
    serverMap:str
    gameFolder:str
    gameName:str
    appId:int
    playingPlayerCount:int
    maxPlayerCount:int
    botCount:int
    serverType:str
    serverEnviroment:str
    serverVisibilty:int
    vacStatus:int
    gameVersion:int
    edf:int
    a2s_payload=b"\xFF\xFF\xFF\xFF"+chr(0x54).encode()+"Source Engine Query\0".encode()

    def __init__(self,address,connSoc):
        self.ip=address[0]
        self.port=address[1]
        self.connSoc=connSoc
    
    def getData(self):
        self.connSoc.settimeout(5)
        self.connSoc.connect((self.ip,self.port))
        self.connSoc.sendto(self.a2s_payload,(self.ip,self.port))
        
        
        challengeBytes=bytearray(1024)
        recvedDataLen=self.connSoc.recvfrom_into(challengeBytes)[0]
        challenge=challengeBytes[:recvedDataLen][5:]
        self.connSoc.sendto(self.a2s_payload+challenge,(self.ip,self.port))
        
        dataBytes=bytearray(1024)
        recvedDataLen=self.connSoc.recvfrom_into(dataBytes)[0]
        data=dataBytes[:recvedDataLen][6:]
        data=bytes(data)
        return data

    def setData(self,data):
        firstSplit=data.split(b"\00",4)
        remainingData=firstSplit[4]
        self.serverName=firstSplit[0].decode()
        self.serverMap=firstSplit[1].decode()
        self.gameFolder=firstSplit[2].decode()
        self.gameName=firstSplit[3].decode()
        self.appId=struct.unpack("h",remainingData[:2])[0]
        self.playingPlayerCount=remainingData[2]
        self.maxPlayerCount=remainingData[3]
        self.botCount=remainingData[4]
        self.serverType=chr(remainingData[5])
        self.serverEnviroment=chr(remainingData[6])
        self.serverVisibilty=remainingData[7]
        self.vacStatus=remainingData[8]
        secondSplit=remainingData[9:].split(b"\00",1)
        self.gameVersion=int(secondSplit[0].decode())
        self.edf=secondSplit[1][0]
        lastRange=1
        if (self.edf & 0x80):
            self.portNumber=struct.unpack("h",secondSplit[1][lastRange:lastRange+2])[0]
            lastRange+=2
        if (self.edf & 0x10):
            self.gameSteamId=struct.unpack("q",secondSplit[1][lastRange:lastRange+8])[0]
            lastRange+=8
        
        if (self.edf & 0x40):
            self.sourceTvPort=struct.unpack("h",secondSplit[1][lastRange:lastRange+2])[0]
            thirdSplit=secondSplit[1][lastRange+1:].split(b"\x00",2)
            self.sourceTvSpectatorName=thirdSplit[0][1:].decode()
            lastRange=lastRange+2+len(self.sourceTvSpectatorName)

        if (self.edf & 0x20):
            fourthSplit=secondSplit[1][lastRange+1:].split(b"\x00",1)[0]
            self.serverTags=fourthSplit.decode()

    def getInfo(self):
        recvdata=self.getData()
        self.setData(recvdata)


    def dict(self):
        returnDict={}
        returnDict['serverName']=self.serverName
        returnDict['serverMap']=self.serverMap
        returnDict['gameFolder']=self.gameFolder
        returnDict['gameName']=self.gameName
        returnDict['appId']=self.appId
        returnDict['playingPlayerCount']=self.playingPlayerCount
        returnDict['maxPlayerCount']=self.maxPlayerCount
        returnDict['botCount']=self.botCount
        returnDict['serverType']=self.serverType
        returnDict['serverEnviroment']=self.serverEnviroment
        returnDict['serverVisibilty']=self.serverVisibilty
        returnDict['vacStatus']=self.vacStatus
        returnDict['gameVersion']=self.gameVersion
        returnDict['edf']=self.edf

        if self.portNumber: returnDict['portNumber']=self.portNumber
        if self.gameSteamId: returnDict['gameSteamId']=self.gameSteamId
        if self.sourceTvPort: returnDict['sourceTvPort']=self.sourceTvPort
        if self.sourceTvSpectatorName: returnDict['sourceTvSpectatorName']=self.sourceTvSpectatorName
        if self.serverTags: returnDict['serverTags']=self.serverTags

        return returnDict
