格式：
 ?ACT=toshop&shopid=564885&COM=$D[19]L<2>()|<br>
 ACT : 操作命令<br>
 toshop 向店铺的设备发送 $[] 命令<br>
 getingi 获取单台设备的即时码表数据<br>
        参数: shopid  店铺id<br>
              deviceid 设备编号<br>
<br>
 setingi 设置 码表基础值，用于更换娃娃机主板后数据与实际相符<br>
        参数: shopid  店铺id<br>
              coin  当前设备当前值=coin值<br>
              gift  当前设备当前值=gift值<br>
              deviceid 设备编号<br>

         算法是：获取当前设备的值，然后 用 设置值 - 当前值 = 差值 并在数据库中保存差值
         之后获取到抄表数据 都是 加上差值 就等于 目标值  
         例： 换主板前 coin值为8829  新换的主板后，值为 2939
         从数据库中找到换表前数据 8829  - 2939 = 5890
         将5890 存储到 差值数据表中
         获取到新抄表信息为 3011 则用 差值表 5890 + 3011 = 8901
         将8910 存储到 抄表数据
<br>

\

web服务端发起一个抄单台设备码表指令，获取数据 <br>

web端 <br>
API接口- GET /ACT=getingo&shopid=xxx&deviceid=xxxx  // 收到了一个GET请求<br>
    ▼<br>
   [S]dataReceived()<br> 
   ▼<br>
   [S]getdevicecogi()<br>
   ▼<br>
   [S]CLIENT[目标].webobj=self // 传递本对象标志给目标对象
   [S]CLIENT[目标]..getcoingift_one()    // 从目标对象发送消息给外网设备<br>
      self.cKey = b64.createrand() #产生一个key 并保存起来
      "$Q["+str(deviceid)+"]Q<>()&"+str(self.cKey)+"#"
      self.RX(sendstr)

联网设备<br>
   [2]loop -> client.available()  //<br>
   ▼<br>
   [2]loop ->  client.available() ▶ Serial.print(host_char); 透传到串口0<br>

主机<br>
   [1]loop ▶ Serial1.available() -> getdevice()
   [1] 
``` String sendstr ="$D["+String(deviceid)+"]Q<>()&0#"; 
```
   [1]command_D(sendstr) -> sendToDown()->esp_now_send()<br>
分机<br>
   [0]OnDataRecv()<br>
   [0]command_D()-> if (command == 'Q') -> Serial.write(buf,6) //16进制方式写入串口<br>

#等待设备返回<br>
### 设备收到了来自串口命令，返回到串口
   [0]loop()->if(Serial.available()>0)-> 收到串口消息<br>
      if(inCommand=='Q') -> sendToUp(umsg) //根据收到的命令类型返回消息<br>
         umsg=$U[MID]q<123>(567)&# <br>
   
   [0]sendToUp() -> esp_now_send()
#### 主、中继设备收到消息
   [0]OnDataRecv()->command_U()->sendToUp()->
```C
   if (SUNM1.MAIN){ //主设备：生成json 并发送到串口1
    if (command == 'q'){  // 
      String outstr ="{\"COM\":\"Qde\",\"COIN\":"+reStr(sdata,'<','>')+",";
      Serial1.println(outstr);
    }

   }else{ // 中继设备继续向上传递
      esp_now_send()
   }
```

#### 联网设备
   [2]loop()->
```C
if (SUNM1.MAIN==2){//直接发送给 S 服务器
   String outr = String(uartbuf,uartpo);
   client.print(outr);
}
```
#### 服务端

   [S]dataReceived()->if abc["COM"]=="Cog":<br>
         self.webObj.reWebStr(data) #返回结果给api调用端<br>


   解码UNK


   














