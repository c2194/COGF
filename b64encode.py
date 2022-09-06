import random


class b64encode2:
    b64dict = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5,"6": 6, "7": 7, "8": 8, "9": 9,"A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15, "G": 16,"H": 17, "I": 18, "J": 19, "K": 20, "L": 21, "M": 22, "N": 23,"O": 24, "P": 25, "Q": 26, "R": 27, "S": 28, "T": 29, "U": 30,"V": 31, "W": 32, "X": 33, "Y": 34, "Z": 35,"a": 36, "b": 37, "c": 38, "d": 39, "e": 40, "f": 41, "g": 42,"h": 43, "i": 44, "j": 45, "k": 46, "l": 47, "m": 48, "n": 49,"o": 50, "p": 51, "q": 52, "r": 53, "s": 54, "t": 55, "u": 56,"v": 57, "w": 58, "x": 59, "y": 60, "z": 61,"-": 62, "_": 63}
    b64str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    codearr = [131,255,69,213,67,233,63,41,200,182,249,175,64,84,206,167,58,191,194,241,151,240,13,86,174,72,111,199,253,225,78,69,73,52,106,237,197,29,235,33,247,37,178,201,142,57,8,84,123,5,74,163,16,153,114,253,3,96,168,33,147,93,144,244,121,234,22,11,233,6,149,192,59,63,133,227,86,25,174,57,36,3,207,199,209,86,72,221,201,100,21,159,61,215,238,252,183,53,220,235,31,82,86,104,179,35,32,211,71,29,214,248,214,207,108,48,164,170,162,168,245,206,141,81,32,235,101,96]
    key=[]
    def createCode(self): #产生一个128字符的key
        aaa=0
        ostr = ""
        while aaa<128:
            ostr = ostr +","+str(random.randint(1,255))
            aaa +=1
        print (ostr)

    def createrand(self): # 创建一个10位的随机字符串，
        aaa=0
        ostr=""
        while aaa<10:
            ostr = ostr +self.b64str[random.randint(0,62)]
            aaa+=1
        return ostr


    def createkey(self,instr): # 对字符串进行不可逆演算，并返回字符串结果，
        strlen = len(instr)

        '''
        算法：提取：第一位从0开始，到位置提取，把提取位的下一位作为0 ，超128环形计位

        '''    
        po=0
        sigmanum=0
        encodenum=0
        spo=0
        for char_f in instr:
            spo = spo + self.b64dict[char_f]

            if spo > 127:
                spo = spo -128 
            sigmanum = sigmanum+ self.codearr[spo] *   1234567 +1000000000
            encodenum = encodenum+ self.codearr[spo] * 1375937 +1000000000

        rstr = [str(sigmanum)[2:12],str(encodenum)[0:12]]
        self.key=rstr


        return rstr
    
    def commandencode(self,comstr,ened2): #生成校验码 ，规则是不可逆码+命令的ascii 的sigma Σ
        comlen = len(comstr)
        aa=0
        oadd = 0
        for char_f in comstr:
            oadd = oadd + ord(char_f)
        
        reint = int(ened2)+oadd
        return str(reint)





#bencode =b64encode()

#bb=0
#while bb<10:
#    astr = bencode.createrand() #产生一个10位的字符串

 #   ened = bencode.encode8(astr)

  #  print(astr +":"+ened[0]+" - " +ened[1])
   # bb+=1
