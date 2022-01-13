import random, time
def show(lightshow, id):
    while (not lightshow.kill_all_threads):# and (not sw):
        print("fade")
        color = [random.randint(0,255) for i in range(3)]
        color[random.randint(0,2)] = 0
        for i in range(256):
            lightshow.pixels.fill(tuple([int(i/256 * a) for a in color]))
            lightshow.pixels.show()
            if lightshow.current_lightshow_id == id: # check if button has been pressed
                time.sleep(0.005)
            else:
                return
        for i in range(int(256/2)):
            i = 255 - i*2
            lightshow.pixels.fill(tuple([int(i/256 * a) for a in color]))
            lightshow.pixels.show()
            if lightshow.current_lightshow_id == id: # check if button has been pressed
                time.sleep(0.005)
            else:
                return
        lightshow.pixels.fill((0,0,0))
        lightshow.pixels.show()
        for i in range(10):
            if lightshow.current_lightshow_id == id: # check if button has been pressed
                time.sleep(0.01)
            else:
                return
