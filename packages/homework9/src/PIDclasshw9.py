#!/usr/bin/env python3

import time
from std_msgs.msg import Float32

class PID:
    def __init__(self, firstError, firstvelocity):
        self.velocity = firstvelocity
        self.KP = 1.0
        self.KI = 0.1
        self.KD = 1.0
        
        global t1
        t1 = time.time()
        global lastError
        lastError = firstError
        
    def changeGainz(self, KPc, KIc, KDc):
        self.KP = KPc
        self.KI = KIc
        self.KD = KDc
    
    def calc(self, error):
        alphaT = time.time()-t1
        
        self.signal = (self.KP*error) + (self.KI * alphaT) + (self.KD *((error-lastError)/alphaT))
        self.lastError = error
        
        return self.signal
