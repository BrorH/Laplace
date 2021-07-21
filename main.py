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




#subprocess.call(["touch", "/home/pi/started.yes.nad"])

pixel_pin = board.D18 # BCM ID for data out pin connected to the neopixels
button_pin = 15 # BCM ID for pin connected to the button
power_switch_pin = 3
num_pixels = 240 # The number of NeoPixels


global mode, kill_all_threads

mode = 0 # the initial mode which is incremented by a button press
num_modes = 2 # the number of different light modes
kill_all_threads = False # when True, all threads will halt



GPIO.setmode(GPIO.BCM)

GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # for interrupts
    


ORDER = neopixel.GRB # green-red-blue

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER
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

    pixels.fill((0,0,0))
    pixels.show()

    GPIO.cleanup()
    if shutdown:
        print("poweroff")
        subprocess.call(['shutdown', '-h', 'now'], shell=False)
    else:
        sys.exit(0)




def increment_mode():
    global mode 
    mode += 1
    mode = mode % num_modes
    print(mode)
    

def check_for_button_press(prev_val):
    btn_input = GPIO.input(button_pin)
    if (btn_input == GPIO.HIGH) and (btn_input != prev_val):
        return True, btn_input
    else:
        return False, btn_input
    



def rainbow_cycle( _mode = 0):

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
            
            if mode == _mode: # check if button has been pressed
                time.sleep(0.01)
            else:
                return

def blink(_mode = 1):
    colors = [(255,0,0), (0,255,0), (0,0,255)]
    while True and (not kill_all_threads):
        for i in range(3):
            pixels.fill(colors[i])
            pixels.show()

            if mode == _mode: # check if button has been pressed
                time.sleep(0.2)
            else:
                return



def poll_button(wait=0.08):
    GPIO.setup(power_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(power_switch_pin, GPIO.BOTH, callback=exit)
    prev_val = GPIO.input(button_pin)
    while True and (not kill_all_threads):
        time.sleep(wait)
        is_pressed, prev_val = check_for_button_press(prev_val)
        if is_pressed:
            increment_mode()
       

def log_error(err):
    print(err)
    with open("~/Laplace/err.txt", "w+") as file:
        file.writelines(err)



if __name__ == "__main__":
    

    # wait for button press to change mode
    modes = [rainbow_cycle, blink]
    prev_val = GPIO.input(button_pin)

    btn_listener = threading.Thread(target = poll_button)
    btn_listener.start()
    
    while True:
        pixels.fill((0,0,0))
        pixels.show()
        lightshow_thread = threading.Thread(target = modes[mode])
        lightshow_thread.start()
        try:
            lightshow_thread.join()
        except KeyboardInterrupt:
            exit(shutdown=False)
        except Exception as e:
            log_error(e)
            exit(shutdown=False)
            

        time.sleep(0.08)

    
      

