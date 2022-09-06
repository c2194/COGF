import threading
import time
import datetime



class ccc:
    mid =""
    tim =1
    def d1(self):
        print(self.mid) 
        timer1 = threading.Timer(self.tim, self.d1)
        timer1.start()







cc=ccc()
cc.mid="11"
cc.d1()

cc2=ccc()
cc2.tim=3
cc2.mid="22"
cc2.d1()

while(1):
    pass


'''"CREATE TABLE IF NOT EXISTS `coininit` (
  `ci_id` int(11) NOT NULL AUTO_INCREMENT,
  `ci_shopid` int(11) NOT NULL,
  `ci_c1` int(11) NOT NULL DEFAULT '0',
  `ci_c2` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ci_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;'''