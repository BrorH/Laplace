from LaplaceMirror import *

global j 
j = 0

def lightshow(pixels, *args, **kwargs):
    def wheel(pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
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
        return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)
    global j
    start_j = j 
    for j in range(start_j, 255):
        for i in range(len(pixels)):
            pixel_index = (i * 256 // len(pixels)) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        #time.sleep(wait)

    


class Wheel(Mirror):
    def run(self,speed=1):
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
                for i in range(self.n):
                    pixel_index = (i * 256 // self.n) + j
                    self[i] = get_wheel(pixel_index & 255)
                #self.print()
                self.show()
                time.sleep(0.07)
    
if __name__ == "__main__":
    Wheel().run()


