from sty import  bg
import time, sys, random, colorsys, subprocess
import numpy as np



class Mirror:
    def __init__(self,length, height):
        assert isinstance(length,int) and isinstance(height, int)
        self.l = length 
        self.h = height 
        self.n = self.l*2+self.h*2 
        self.leds = np.zeros((self.n,3), dtype=np.int32)
       
    def add(self,idx,color, ignore_zero = True):
        if ignore_zero:
            if np.sum(self[idx]) < 20:
                self[idx] = color 
                return
        r1,g1,b1 = tuple(self[idx])
        r2,g2,b2 = tuple(color)
        d1 = 5

        self[idx] = ((r1/d1+r2*(1-1/d1) ), (g1/d1+g2*(1-1/d1)), (b1/d1+b2*(1-1/d1))) 
    
    def clear(self):
        self.leds = np.zeros((self.n,3), dtype=np.int32)

    def fade(self,amount, idx=None):
        if idx is None:
            self.leds = np.floor_divide(self.leds,amount).astype(np.int32)
        else:
            self[idx] = np.floor_divide(self[idx],amount).astype(np.int32)
        

    def __setitem__(self, idx, val):
        self.leds[idx%self.n] = np.array(val)

    
    def __getitem__(self, idx):
        return self.leds[idx%self.n]

    def __str__(self):
        res = ""
        for i in range(self.l):
            res += bg(*self[self.l-i]) +" " + bg.rs 
        for i in range(self.h):
            res += "\n"+bg(*self[self.l+i]) +"  "+bg.rs 
            res += " "*(self.l-4)
            res += bg(*self[-i]) +"  "+bg.rs 
        res += "\n"
        for i in range(self.l):
            res += bg(*self[self.l+self.h+i]) +" " + bg.rs 
        return res


    def __repr__(self):
        return self.__str__() 
    
    def print(self):
        subprocess.run(["clear"])
        print(self, flush=True,end="\n")
        print()



def random_color():
    rgbl=[255,0,0]
    random.shuffle(rgbl)
    return tuple(rgbl)


def dots(m,speed=2, num=1, size=5):
    n = random.randint(0,m.n)
    i = -1
    while True:
        i = (i+1)%5
        if i == 0:
            while abs( (new_n:= random.randint(0,m.n)) -n ) < size +4: pass
            n = new_n
            h,s,l = random.random(), 0.5 + random.random()/2.0, 0.4 + random.random()/5.0
            r,g,b = [int(256*i) for i in colorsys.hls_to_rgb(h,l,s)]
            for enum,n_ in enumerate(range(n-size, n+size+1)):
                m.add(n_, (r,g,b))
                m.fade(1+abs(enum-size)*0.5, n_)

        m.fade(1.1)
        m.print()
        time.sleep(0.1)



def wheel(m,speed=1):
    def get_wheel(pos):
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b)

    while True:
        for j in range(0,255,speed):
            for i in range(m.n):
                pixel_index = (i * 256 // A.n) + j

                m[i] = get_wheel(pixel_index & 255)
            m.print()
            time.sleep(0.07)


      
  





A = Mirror(50,5)
wheel(A,10)

 
 

 