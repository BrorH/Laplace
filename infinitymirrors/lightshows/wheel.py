import time
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
        print("wheel", lightshow.kill_all_threads)
        for j in range(255):
            # if (kill_all_threads): break
            for i in range(len(lightshow.pixels)):
                pixel_index = (i * 256 // len(lightshow.pixels)) + j
                lightshow.pixels[i] = wheel(pixel_index & 255)
            lightshow.pixels.show()
            
            if lightshow.current_lightshow_id == id: # check if button has been pressed
                time.sleep(0.01)
            else:
                return

