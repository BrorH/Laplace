import math, time


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
        return (r, g, b)

def show(lightshow, id):
    while (not lightshow.kill_all_threads):# and (not sw):
        print("circus")
        j = 0
        L = 30
        for i in range(120):
            newcolor = wheel(int((4*i+0*j*120)/240/2*255))
            for k in range(L):
                newERcolor = tuple([ int(a*(1-math.sqrt((k-L/2)**2)/(L/2))) for a in newcolor])
                lightshow.pixels[(i+k)%120] = newERcolor
                # pixels[(i+k)%120].brightness = (k-9)**2/81
                lightshow.pixels[239-(i+6+k)%120] = newERcolor
            lightshow.pixels[(i-1)%120] = (0,0,0)

            # pixels[239-(i+6+1)%120] = newcolor
            # pixels[239-(i+6+2)%120] = newcolor
            lightshow.pixels[239-((i-1)+6)%120] = (0,0,0)

            lightshow.pixels.show()
            if lightshow.current_lightshow_id == id: # check if button has been pressed
                time.sleep(0.01)
            else:
                return
        j = (j+1)%2
