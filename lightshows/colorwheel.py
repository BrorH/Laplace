from LaplaceMirror import *

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


