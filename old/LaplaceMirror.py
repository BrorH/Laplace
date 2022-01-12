from sty import  bg
import time, sys, random, colorsys, subprocess
import numpy as np



class Mirror:
    height = 6 # depth of mirror in leds
    length = None
    led_count = 240
    def __init__(self, mode="merge"):
        
        assert mode.lower() in ["merge", "split"], f"mode must be 'merge' or 'split'. Please read the docs"
        self.mode = mode.lower()
        if self.mode == "merge":
            self.length = 108 # num. of leds along bar disk in merged mode
        elif self.mode == "split":
            print("SPLIT NOT YET IMPLEMENTED")
            import sys 
            sys.exit()
            # for now the two irrors in split mode will be equal
            self.length = 54 # num. of leds along a single mirror in split mode
      
        self.n = self.length*2+self.height*2 # number of leds in sequence (not the acutal number of leds in the physical mirror)
        self.led_arr = np.zeros((self.n,3), dtype=np.int32) # to be filled with rgb vals
       
    def add(self,idx,color, ignore_zero = True):
        idx = self.get_correct_idx(idx)
        if ignore_zero:
            if np.sum(self[idx]) < 20:
                self[idx] = color 
                return
        r1,g1,b1 = tuple(self[idx])
        r2,g2,b2 = tuple(color)
        d1 = 5

        self[idx] = ((r1/d1+r2*(1-1/d1) ), (g1/d1+g2*(1-1/d1)), (b1/d1+b2*(1-1/d1))) 
    
    def clear(self):
        # turn off leds
        self.led_arr = np.zeros((self.n,3), dtype=np.int32)

    def fade(self,amount, idx=None):
        # fades the light of the mirror at given idx. if idx is None, fades entire mirror
        if idx is None:
            self.led_arr = np.floor_divide(self.led_arr,amount).astype(np.int32)
        else:
            idx = self.get_correct_idx(idx)
            self[idx] = np.floor_divide(self[idx],amount).astype(np.int32)
        
    def get_correct_idx(self, idx):
        if  self.mode == "merge" and idx >= 115:
            idx += 12 # in merge mode, we skip the two sections in the middle 
        return idx


    def __setitem__(self, idx, val):
        idx = self.get_correct_idx(idx)
        self.led_arr[idx%self.n] = np.array(val)

    
    def __getitem__(self, idx):
        idx = self.get_correct_idx(idx)
        return self.led_arr[idx%self.n]

    def __str__(self):
        res = ""
        for i in range(self.length):
            res += bg(*self[self.length-i]) +" " + bg.rs 
        for i in range(self.height):
            res += "\n"+bg(*self[self.length+i]) +"  "+bg.rs 
            res += " "*(self.length-4)
            res += bg(*self[-i]) +"  "+bg.rs 
        res += "\n"
        for i in range(self.length):
            res += bg(*self[self.length+self.height+i]) +" " + bg.rs 
        return res


    def __repr__(self):
        return self.__str__() 
    
    def print(self):
        subprocess.run(["clear"])
        print(self, flush=True,end="\n")
        print()
    
    def show(self):
        # Calls the pi-led script to actually display and update the leds
        if self.mode == "merge":
            for idx, val in enumerate(self.led_arr):
                pass
       


