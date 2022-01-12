

"""
Made by Bror Hjemgaard 2021 for Laplace, UiO
Bror.hjemgaard@gmail.com
"""

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

import time
import board
import neopixel
import subprocess

pixel_pin = board.D18 # BCM ID for data out pin connected to the neopixels
button_pin = 15 # BCM ID for pin connected to the button
power_switch_pin = 3
num_pixels = 240 # The number of NeoPixels


global mode
mode = 1 # the initial mode which is incremented by a button press



def GPIO_init():
    GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # for interrupts
      
    GPIO.setup(power_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(power_switch_pin, GPIO.BOTH, callback=power_off)
    ORDER = neopixel.GRB #GRB

    pixels = neopixel.NeoPixel(
        pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
    )
    #pixels = list(range(240))
    return pixels

def power_off():
    GPIO.cleanup()
    subprocess.call(['shutdown', '-h', 'now'], shell=False)


def increment_mode():
    global mode 
    mode += 1
    mode = mode % 2
    print(mode)

def check_for_button_press(prev_val):
    btn_input = GPIO.input(button_pin)
    if (btn_input == GPIO.HIGH) and (btn_input != prev_val):
        return True, btn_input
    else:
        return False, btn_input
    

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

def rainbow_cycle(pixels, prev_val):
    for j in range(255):
        is_pressed, prev_val = check_for_button_press(prev_val)
        if is_pressed:
            increment_mode()
            return
        for i in range(len(pixels)):
            pixel_index = (i * 256 // len(pixels)) + j
            pixels[i] = wheel(pixel_index & 255)
            #print(" ", i)
        pixels.show()
        time.sleep(0.05)
        
def mono(pixels, prev_val):
    #if _mode != mode: # if the mode has been changed by a button press
    #    return
    
    #is_pressed, prev_val = check_for_button_press(prev_val)
    #if is_pressed:
    #    increment_mode()
    #    return
    pixels.fill((255, 255, 255))
    pixels.show()
    #time.sleep(0.05)



if __name__ == "__main__":
    pixels = GPIO_init()

    # wait for button press to change mode
    modes = [rainbow_cycle, mono]
    prev_val = GPIO.input(button_pin)
    while True:
        is_pressed, prev_val = check_for_button_press(prev_val)
        if is_pressed:
            increment_mode()
            time.sleep(0.01)
        #btn_input = GPIO.input(button_pin)
        #if (btn_input == GPIO.HIGH) and (btn_input != prev_val):
        #    increment_mode()
        #prev_val = btn_input
        modes[mode](pixels, prev_val)
        time.sleep(0.08) # change this to get a more responsive button
      


# already_pressing = False
# while True:
#     try:
#         if GPIO.input(15) == GPIO.HIGH:
#             if not already_pressing:
#                 mode += 1
#                 mode = mode % 4
#                 already_pressing = not already_pressing
#         if GPIO.input(15) == GPIO.LOW:
#             if already_pressing:
#                 already_pressing = not already_pressing
#     except Exception as e:
#         with open("err.out", "w+") as outfile:
#             outfile.write(e)
#         pass
    
#     if mode == 0:
#         print("rainbow", mode)
#         try:
#             for j in range(255):
#                 for i in range(num_pixels):
#                     assert mode == 0 and GPIO.input(15) == GPIO.HIGH, "oops"
#                     pixel_index = (i * 256 // num_pixels) + j
#                     pixels[i] = wheel(pixel_index & 255)
#                 pixels.show()
#                 if mode == 0 and GPIO.input(15) != GPIO.HIGH:
#                     time.sleep(0.005)
#                 else:
#                     break
#         except AssertionError:
#             continue
#             #rainbow_cycle(0.005)
            
#         #time.sleep(0.1)
#     elif mode == 1:
#         print("color 1")
#         pixels.fill((255, 0, 0))
#         pixels.show()
#         time.sleep(0.1)
#     elif mode == 2:
#         print("color 2")
#         pixels.fill((0, 255, 0))
#         pixels.show()
#         time.sleep(0.1)
#     elif mode == 3:
#         print("color 3")
#         pixels.fill((0, 0, 255))
#         pixels.show()
#         time.sleep(0.1)
#     continue
#     # Comment this line out if you have RGBW/GRBW NeoPixels
#     pixels.fill((255, 255, 255))
    
#     # Uncomment this line if you have RGBW/GRBW NeoPixels
#     # pixels.fill((255, 0, 0, 0))
#     pixels.show()
#     time.sleep(0.5)

#     # Comment this line out if you have RGBW/GRBW NeoPixels
#     pixels.fill((0, 255, 0))
#     # Uncomment this line if you have RGBW/GRBW NeoPixels
#     # pixels.fill((0, 255, 0, 0))
#     pixels.show()
#     time.sleep(0.5)

#     # Comment this line out if you have RGBW/GRBW NeoPixels
#     pixels.fill((0, 0, 255))
#     # Uncomment this line if you have RGBW/GRBW NeoPixels
#     # pixels.fill((0, 0, 255, 0))
#     pixels.show()
#     time.sleep(0.5)

#     #rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step
