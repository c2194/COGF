from re import S
import threading
import time
from winreg import CloseKey, CreateKey
from twisted.internet.protocol import Factory, connectionDone
from twisted.internet import reactor, protocol
import json
import b64encode
from basciEncode import encode8

import urllib

CLIENT = {}
clientID =[]
client_loop_po =0
client_Len=0
Clientpo=[0,0]
clientClose=[]
clientLoopSec=[0]


b64 =b64encode.b64encode2()

class QuoteProtocol(protocol.Protocol):
    
    global client_Len
    MID="NO"
    key=[]
    cKey=""

    webState=0 # 本实体是否在对一个web请求，获取设备数据
    webObj=""  # 正常处理的，web请求对象
    webTime =0 # web对象，发起请求的时间，用于超时计时




    commandStep=0 # 1 已发送发送key 请求，等待结果，2 收到key , 发送了命令，等待返回0 空闲
    commandStr =""
    commandTime=0 # 超时方法：发送的时候写入时间戳，下次收到发送命令的时候，检查此时间戳与 当前时间的差，超过一定时间 视为超时，放弃命令状态，进行新发命令流程
    def __init__(self, factory):
        self.factory = factory
    def connectionMade(self):  # 建立连接后的回调函数
        self.factory.numConnections += 1
        print("host: %d" % self.factory.numConnections)

    def commandToJson(self,istr):#解析出所有的参数
        re = {}
        istrLen= len(istr)

        KV = 'K'
        
        spstr =""
        start=0
        ikey=""

        for i in istr:

            if (start==1):
                if i == '=':
                    ikey=spstr
                    spstr=""
                elif i =='&':
                    re[ikey]=spstr
                    spstr=""
                    ikey=""
                    pass
                else:
                    spstr +=i
            if i=='?': 
                start=1
        re[ikey]=spstr
        return re

    def checkcom(self,instr): #检查命令字符串的完整性，返回串的 asc ii  Σ 值
        sflag =0
        st=instr.find("$")
        en=instr.find("&")
        if st>-1 and en>-1:
            for i in range(en+1):
                sflag=sflag+ord(instr[i])
        return sflag
    
    def reWebStr(self,def_re):
        self.RX("HTTP/1.1 200 OK\r\nContent-type:text/html\r\n\r\n")
        self.RX(def_re)
        self.transport.loseConnection()
        self.webState=0

    def gTimeout(self):
        if self.webState==1:
            re="{\"RE\":\"timeout\"}"
            self.reWebStr(re)

        


    def getdevicecogi(self,comjson):
        re="{\"RE\":\"ParError\"}"
        parComplete =0

        if ("shopid" in comjson):
            parComplete+=1
        if ("deviceid" in comjson):
            parComplete+=1   
        if parComplete<2: #参数不完整 返回错误
            self.reWebStr(re)
            return 0


        else:
            if (comjson['shopid'] in CLIENT):
                pass
            else:
                self.reWebStr(re)
                return 0

            CLIENT[comjson['shopid']].webObj=self #吧本对象传给，目标对象
            CLIENT[comjson['shopid']].getcoingift_one(comjson["deviceid"])
            
            self.webState=1
            timer1 = threading.Timer(5, self.gTimeout) # 5秒超时
            timer1.start()
    
            pass
            #使用目标对象发送数据
            #等待返回，
            #产生一个定时器，并记录请求这对象，
            #若返回，发送数据给对象，关闭对象，清空定时器返回标志
            #


 




    def toshopComnad(self,comjson):

        shopid =""
        shopid_flag=0
        toshopcommand = ""
        toshopcommand_flag=0
        re=""
        if ("shopid" in comjson):
            shopid = comjson['shopid']
            shopid_flag =1
            if ("COM" in comjson):
               # toshopcommand=comjson['command']
                toshopcommand_flag=1
        
        if shopid_flag==1 and toshopcommand_flag==1:#只有包含了完整的数据

            #判断设备是否在线，是否有人在操作
            #向设备发送命令
            #向设备对象，写入本对象，等设备对象，收到结果后发送结果，和关闭链接和本对象
            clientOK=0
            if (shopid in CLIENT):#是否有该连接
                #if CLIENT[shopid]
                if self.webState==0:
                    self.webTime = int(time.time())
                    self.webState=1
                    self.webObj=self
                    clientOK=1

                    pass
                else:
                    thtime = int(time.time())
                    if thtime - self.webTime >5: # 大于5秒还没关闭，没获取到数据，就超时，覆盖
                        self.webTime = int(time.time())
                        self.webState=1
                        self.webObj=self
                        clientOK=1
                    else:
                        re="{\"RE\":\"LineBusy\"}" #返回线路忙            
            else:
                re="{\"RE\":\"NotOnline\"}"
            
            if clientOK==1:
                if ("COM" in comjson):
                    commstr = comjson["COM"]
                    commstr = commstr.replace('|','&')
                    


                    sended = CLIENT[shopid].sendCommand(commstr)
                    if sended ==1:
                        re="{\"RE\":\"SendOK\"}"
                    else:
                        re="{\"RE\":\"PassBusy\"}"

        return re

        


    def dataReceived(self, data):  # 接收到数据后的回调函数
      #  print("Number of active connections: %d"
       #       % self.factory.numConnections)
        #print("Received:%s\n Sending: %s" % (data, self.getQuote()))
      #  print("Received:%s\n " % (data))
        abc ={}
        data = urllib.parse.unquote(data)
        data = bytes(data,encoding='utf-8')
        if data[0]==ord('G') and data[1]==ord('E') and data[2]==ord('T'): #提交

            instr = data.decode('utf-8')
            ist = instr.find("HTTP")
            commandstr = instr[4:ist-1]
            print(self.MID+"-in-"+commandstr)
            comjson = {}
            comjson =self.commandToJson(commandstr)
            reDelaying=0
            def_re=""
            if ("ACT" in comjson):
                if comjson['ACT'] == "toshop": #比如：向店铺发送命令  $D[22]I<+2344>(-22345)& 此命令 修改 设备盒子发送的主板计数器初始值
                    def_re=self.toshopComnad(comjson)
                elif comjson['ACT'] == "getingf": #获取单台设备的码表数据
                    self.getdevicecogi(comjson)
                else:
                    def_re="{\"RE\":\"Error\"}"
            else:
                def_re="{\"RE\":\"Error\"}"

            if reDelaying==0:
                self.RX("HTTP/1.1 200 OK\r\nContent-type:text/html\r\n\r\n")

                self.RX(def_re)
                self.transport.loseConnection()
                return 0
        





        try:
            abc = json.loads(data.decode())
            print(self.MID+"-in$[]-"+str(data))
            if abc["COM"]=="Reg":
                CLIENT[abc["ShopID"]]=self #添加对象到字典
                noFlag=1
                for i in clientID:
                    if i == abc["ShopID"]:
                        self.MID=i
                        noFlag=0
                if noFlag:
                    clientID.append(abc["ShopID"]) #在列表中放置索引，用于定时对已连接设备进行业务逻辑
                    Clientpo[0]+=1
                    self.MID = abc["ShopID"]
            
            if abc["COM"]=="Key":
                #返回了key 就对要发送的命令进行编码方法是 先 enkey 然后累加 命令 从#  []<> 到 ）
                #  
                sigmanum = self.checkcom(self.commandStr)
                unkey=encode8(abc["KEY"])
                print(unkey)
                unkey = unkey + sigmanum
                sendstr = self.commandStr+str(unkey)+"#"
                self.RX(sendstr)
                self.commandStep=0
                print ("....."+sendstr)
            if abc["COM"]=="Cog": #如果是抄表返回
                client_unk=abc['UNK']
                unk=encode8(self.cKey)

                print("------"+str(client_unk) + " ---"+str(unk) )
            if abc["COM"]=="Qde": #如果是抄单表
                client_unk=abc['UNK']
                unk=encode8(self.cKey)
                uk = int(client_unk)
                ck = int(unk)
                if uk==ck:
                    self.webObj.reWebStr(data) #返回结果






                print("------"+str(client_unk) + " ---"+str(unk) )
            if abc["COM"]=="REM": # 一般性返回，如命令执行结果
                restr = "{\"ACT\":\"reingi\",\"RJN\":"+data+"}"
                try:
                    self.webObj.reWebStr(restr)
                except:
                    pass
        except:
            pass

            


            
       # self.transport.write(self.getQuote())
        #self.updateQuote(data)
    def connectionLost(self, reason=connectionDone):  # 断开连接后的反应
        self.factory.numConnections -= 1
        if self.MID != "NO":
            clientClose.append(self.MID) #断开连接 向删除列表中添加
    def getQuote(self):
        return self.factory.quote
    def updateQuote(self, quote):
        self.factory.quote = quote
    def dclick(self):
        a=0
    def RX(self,instr): #心跳，并作为命令key 请求，向目标发送一条命令要3个周期，1，请求key， 2收到 key 3，编码命令
        self.transport.write(instr.encode())
        print(self.MID+":send____:"+instr)

    def sendCommand(self,instr): #发送命令的时候会产生一个key，这个key 将发送到用户链接，用户链接以此对返回的信息进行编码

        if self.commandStep ==0:
            self.commandStep=1
            self.commandStr=instr
            self.commandTime =int(time.time())
            self.RX("$K[]<>()#")
            return 1
        else:
            if int(time.time())-self.commandTime > 3: # 发送命令后 3秒还没返回数据，则视为超时，发送新命令
                self.commandStep=1
                self.commandStr=instr
                self.commandTime =int(time.time())
                self.RX("$K[]<>()#")
                return 1
            else:
                return 0


    def getcoingift(self):#获取所有抄表结果  发送一个key，返回的数据需对该key 进行 unkey
        self.cKey = b64.createrand() #产生一个key 并保存起来
        sendstr = "$P[0]<>()&"+str(self.cKey)+"#"
        self.RX(sendstr)
        #print(sendstr)

    #AA03013032DD

    def getcoingift_one(self,deviceid):#获取单台抄表结果发送一个key，返回的数据需对该key 进行 unkey
        self.cKey = b64.createrand() #产生一个key 并保存起来
        sendstr = "$D["+str(deviceid)+"]Q<>()&"+str(self.cKey)+"#"
        self.RX(sendstr)
        #print(sendstr)


    def setdata(self,data):
        self.data = data





class QuoteFactory(Factory):
    numConnections = 0
    def __init__(self, quote=None):  # 数据接收后放在在quote中
        self.quote = quote or str("Test").encode("utf8")
    def buildProtocol(self, addr):
        return QuoteProtocol(self)

def loop():

    #print(" - ")
    clientLoopSec[0]+=1 # 定时发送心跳等
    if clientLoopSec[0]>5:
        clientLoopSec[0]=0
    if clientLoopSec[0]<len(clientID): # 
        #CLIENT[clientID[clientLoopSec[0]]].sendCommand("$D[19]L<1>()&")
      #  CLIENT[clientID[clientLoopSec[0]]].getcoingift()
      pass




    if (len(clientClose)):
        try:
            print("close:"+clientClose[0])
            CLIENT.pop(clientClose[0])
            clientID.remove(clientClose[0])
            clientClose.pop(0)
        except:
            pass


    timer1 = threading.Timer(1, loop)
    timer1.start()

    
def init():
    timer1 = threading.Timer(0.1, loop)
    timer1.start()

loop()
reactor.listenTCP(8000, QuoteFactory())
reactor.run()
