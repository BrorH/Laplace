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


lightshow_id = 0 # the initial lightshow_id which is incremented by a button press
kill_all_threads = False # when True, all threads will halt


pixel_pin = board.D18 # BCM ID for data out pin connected to the neopixels
button_pin = 15 # BCM ID for pin connected to the button
power_switch_pin = 3
num_pixels = 240 # The number of NeoPixels


# Neopixel init setup
GPIO.setmode(GPIO.BCM)
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=neopixel.GRB
)


def exit(shutdown = True, *args, **kwargs):
    global kill_all_threads

    # safely end all threads
    kill_all_threads = True
    for thread in threading.enumerate()[1:]:
        try:
            thread.join(timeout=1)
        except Exception as e:
            log_error(e)

    # turn off the pixels
    pixels.fill((0,0,0))
    pixels.show()

    GPIO.cleanup()
    if shutdown:
        print("Shutting down ... ")
        subprocess.call(['shutdown', '-h', 'now'], shell=False)
    else:
        sys.exit(0)




def change_ligthshow():
    global lightshow_id 
    lightshow_id += 1
    lightshow_id = lightshow_id % num_lightshows
    print(lightshow_id)
    

def check_for_button_press(prev_val):
    btn_input = GPIO.input(button_pin)
    if (btn_input == GPIO.HIGH) and (btn_input != prev_val):
        return True, btn_input
    else:
        return False, btn_input
    



def rainbow_cycle(id = 0):

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
    
    while True and (not kill_all_threads):
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

def blink(id = 1):
    colors = [(255,0,0), (0,255,0), (0,0,255)]
    while True and (not kill_all_threads):
        for i in range(3):
            pixels.fill(colors[i])
            pixels.show()

            if lightshow_id == id: # check if button has been pressed
                time.sleep(0.2)
            else:
                return



def base_thread_method(wait=0.08):
    # the base thread in which all non-lightshow events take place

    # setup button and power switch GPIO
    GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # for interrupts
    GPIO.setup(power_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(power_switch_pin, GPIO.BOTH, callback=exit) # make a switch flip toggle power

    prev_val = GPIO.input(button_pin)
    while True and (not kill_all_threads):
        time.sleep(wait)
        is_pressed, prev_val = check_for_button_press(prev_val)
        if is_pressed:
            change_ligthshow()
       

def log_error(err):
    print(err)
    with open("~/Laplace/err.txt", "w+") as file:
        file.writelines(err)



if __name__ == "__main__":
    # wait for button press to change lightshow_id
    lightshows = [rainbow_cycle, blink]
    num_lightshows = len(lightshows) # the number of different lightshows


    base_thread = threading.Thread(target = base_thread_method)
    base_thread.start()
    prev_val = GPIO.input(button_pin)
    
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
