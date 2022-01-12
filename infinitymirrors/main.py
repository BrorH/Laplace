#!/usr/bin/python


"""
Made by Bror Hjemgaard 2021 for Laplace, UiO
Bror.hjemgaard@gmail.com
"""

import RPi.GPIO as GPIO
import time
import board
import neopixel
import subprocess
import threading
import sys
import random 
import math
import serial

global analog, btn, sw
sw = False

port = serial.Serial("/dev/ttyUSB0", 115200)


# startup time
time.sleep(3)


lightshow_id = 0 # the initial lightshow_id which is incremented by a button press
kill_all_threads = False # when True, all threads will halt


num_pixels = 240 # The number of NeoPixels
pixel_pin = board.D18 # BCM ID for data out pin connected to the neopixels


# Neopixel init setup

GPIO.setmode(GPIO.BCM)
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=neopixel.GRB
)


def exit(shutdown = True, *args, **kwargs):
    global kill_all_threads

    # safely end all threads
    kill_all_threads = True
    for thread in threading.enumerate():
        try:
            print(thread)
            thread.join(timeout=1)
        except Exception as e:
            log_error(e)
            #print(e)

    # turn off the pixels
    pixels.fill((0,0,0))
    pixels.show()
    
    #adc.close()
    GPIO.cleanup()
    if shutdown:
        print("Shutting down ... ")
        subprocess.call(['shutdown', '-h', 'now'], shell=False)
        sys.exit(1)
    else:
        sys.exit(0)




def change_ligthshow():
    global lightshow_id 
    lightshow_id += 1
    lightshow_id = lightshow_id % num_lightshows
    print(lightshow_id)
    


def read_serial():
    # Reads the controll board input via arduino USB

    global analog, btn, sw
    while True:
        line = port.readline().decode()
        tmpanalog, tmpbtn, tmpsw, tmpswChg = line.split(',')[:4]

        analog = int(tmpanalog)
        btn = bool(int(tmpbtn))
        sw = bool(int(tmpsw))
        swChg = bool(int(tmpswChg))

        if btn and sw:
            change_ligthshow()

        pixels.brightness = analog/1023 if sw else 0
        

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




def rainbow_cycle(id = 0):

    
    while (not kill_all_threads):# and (not sw):
        for j in range(255):
            if (kill_all_threads): break
            for i in range(len(pixels)):
                pixel_index = (i * 256 // len(pixels)) + j
                pixels[i] = wheel(pixel_index & 255)
            pixels.show()
            
            if lightshow_id == id: # check if button has been pressed
                time.sleep(0.01)
            else:
                return



def fade(id = 1):
    while (not kill_all_threads):# and (not sw):
        color = [random.randint(0,255) for i in range(3)]
        color[random.randint(0,2)] = 0
        for i in range(256):
            pixels.fill(tuple([int(i/256 * a) for a in color]))
            pixels.show()
            if lightshow_id == id: # check if button has been pressed
                time.sleep(0.005)
            else:
                return
        for i in range(int(256/2)):
            i = 255 - i*2
            pixels.fill(tuple([int(i/256 * a) for a in color]))
            pixels.show()
            if lightshow_id == id: # check if button has been pressed
                time.sleep(0.005)
            else:
                return
        pixels.fill((0,0,0))
        pixels.show()
        for i in range(10):
            if lightshow_id == id: # check if button has been pressed
                time.sleep(0.01)
            else:
                return



def circus(id = 2):
    while (not kill_all_threads):# and (not sw):
        j = 0
        L = 30
        for i in range(120):
            newcolor = wheel(int((4*i+0*j*120)/240/2*255))
            for k in range(L):
                newERcolor = tuple([ int(a*(1-math.sqrt((k-L/2)**2)/(L/2))) for a in newcolor])
                pixels[(i+k)%120] = newERcolor
                # pixels[(i+k)%120].brightness = (k-9)**2/81
                pixels[239-(i+6+k)%120] = newERcolor
            pixels[(i-1)%120] = (0,0,0)

            # pixels[239-(i+6+1)%120] = newcolor
            # pixels[239-(i+6+2)%120] = newcolor
            pixels[239-((i-1)+6)%120] = (0,0,0)

            pixels.show()
            if lightshow_id == id: # check if button has been pressed
                time.sleep(0.01)
            else:
                return
        j = (j+1)%2

    
    
       

def log_error(err):
    print("got error:")
    print(err)
    print("===================")
    with open("home/pi/Laplace/err.txt", "w+") as file:
        file.writelines(err)



if __name__ == "__main__":
    # wait for button press to change lightshow_id
    lightshows = [rainbow_cycle,fade, circus]
    num_lightshows = len(lightshows) # the number of different lightshows


    base_thread = threading.Thread(target = read_serial)
    base_thread.start()
    prev_val = 1#GPIO.input(button_pin)
    
    while True:
        pixels.fill((0,0,0))
        pixels.show()
        lightshow_thread = threading.Thread(target = lightshows[lightshow_id])
        lightshow_thread.start()
        try:
            lightshow_thread.join()
        except KeyboardInterrupt:
            exit(shutdown=False)
        except Exception as e:
            log_error(e)
            exit(shutdown=False)
            

        time.sleep(0.08)
